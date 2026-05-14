from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse


hex_colour_validator = RegexValidator(
    regex=r"^#[0-9A-Fa-f]{6}$",
    message="Enter a valid six-digit hex colour, for example #0d6efd.",
)


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Organisation(TimeStampedModel):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    contact_email = models.EmailField(blank=True)
    theme_colour = models.CharField(
        max_length=20,
        default="#0d6efd",
        validators=[hex_colour_validator],
    )
    logo_url = models.URLField(blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    @property
    def safe_theme_colour(self):
        try:
            hex_colour_validator(self.theme_colour)
        except ValidationError:
            return "#0d6efd"
        return self.theme_colour

    def get_absolute_url(self):
        return reverse("organisation_home", kwargs={"organisation_slug": self.slug})


class Category(TimeStampedModel):
    organisation = models.ForeignKey(
        Organisation,
        related_name="categories",
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["organisation__name", "name"]
        constraints = [
            models.UniqueConstraint(
                fields=["organisation", "slug"],
                name="unique_category_slug_per_organisation",
            )
        ]
        verbose_name_plural = "categories"

    def __str__(self):
        return f"{self.name} ({self.organisation.name})"

    def get_absolute_url(self):
        return reverse(
            "category_detail",
            kwargs={
                "organisation_slug": self.organisation.slug,
                "category_slug": self.slug,
            },
        )


class SignEntry(TimeStampedModel):
    class PublicationStatus(models.TextChoices):
        DRAFT = "draft", "Draft"
        NEEDS_VIDEO = "needs_video", "Needs video"
        NEEDS_REVIEW = "needs_review", "Needs review"
        PUBLISHED = "published", "Published"
        ARCHIVED = "archived", "Archived"

    class VideoReviewStatus(models.TextChoices):
        UNCHECKED = "unchecked", "Unchecked"
        CANDIDATE_VIDEO = "candidate_video", "Candidate video"
        APPROVED_FOR_PROTOTYPE = "approved_for_prototype", "Approved for prototype"
        BROKEN_LINK = "broken_link", "Broken link"
        NEEDS_REPLACEMENT = "needs_replacement", "Needs replacement"

    organisation = models.ForeignKey(
        Organisation,
        related_name="signs",
        on_delete=models.CASCADE,
    )
    category = models.ForeignKey(
        Category,
        related_name="signs",
        on_delete=models.CASCADE,
    )
    term = models.CharField(max_length=200)
    slug = models.SlugField()
    video_url = models.URLField()
    thumbnail_url = models.URLField(blank=True, help_text="URL to a thumbnail image for the sign video")
    description = models.TextField(blank=True)
    usage_context = models.TextField(blank=True)
    tags = models.CharField(max_length=300, blank=True)
    is_quick_reference = models.BooleanField(default=False)
    publication_status = models.CharField(
        max_length=30,
        choices=PublicationStatus.choices,
        default=PublicationStatus.PUBLISHED,
        help_text="Workflow status controlling whether this sign appears in public/staff glossary views.",
    )
    video_review_status = models.CharField(
        max_length=30,
        choices=VideoReviewStatus.choices,
        default=VideoReviewStatus.UNCHECKED,
        help_text="Simple review status for the linked sign video.",
    )
    is_official_published = models.BooleanField(
        default=True,
        help_text="Whether this sign is approved for publication in this organisation glossary."
    )
    
    class Meta:
        ordering = ["term"]
        constraints = [
            models.UniqueConstraint(
                fields=["organisation", "slug"],
                name="unique_sign_slug_per_organisation",
            )
        ]

    def __str__(self):
        return f"{self.term} ({self.organisation.name})"

    def clean(self):
        if self.category_id and self.organisation_id:
            if self.category.organisation_id != self.organisation_id:
                raise ValidationError(
                    {"category": "The category must belong to the same organisation as the sign."}
                )

    def get_absolute_url(self):
        return reverse(
            "sign_detail",
            kwargs={
                "organisation_slug": self.organisation.slug,
                "sign_slug": self.slug,
            },
        )

    @property
    def is_publicly_visible(self):
        return self.publication_status == self.PublicationStatus.PUBLISHED


class SignEntryChangeLog(TimeStampedModel):
    sign = models.ForeignKey(
        SignEntry,
        related_name="change_logs",
        on_delete=models.CASCADE,
    )
    edited_by = models.ForeignKey(
        "StaffProfile",
        related_name="sign_change_logs",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    changed_fields = models.CharField(max_length=300)
    change_summary = models.TextField()

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.sign.term} edited on {self.created_at:%Y-%m-%d %H:%M}"


class Transcript(TimeStampedModel):
    """Text transcription of an ISL sign for accessibility and search."""
    sign = models.OneToOneField(
        SignEntry,
        related_name="transcript",
        on_delete=models.CASCADE,
    )
    text = models.TextField(
        help_text="Complete text transcription of the ISL sign for accessibility and search indexing."
    )
    language = models.CharField(
        max_length=10,
        default="en",
        help_text="Language code (e.g., 'en' for English, 'ga' for Irish)."
    )

    class Meta:
        ordering = ["sign__term"]

    def __str__(self):
        return f"Transcript for {self.sign.term}"


class FAQEntry(TimeStampedModel):
    organisation = models.ForeignKey(
        Organisation,
        related_name="faqs",
        on_delete=models.CASCADE,
    )
    question = models.CharField(max_length=255)
    answer = models.TextField()
    related_category = models.ForeignKey(
        Category,
        related_name="faqs",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    related_sign = models.ForeignKey(
        SignEntry,
        related_name="faqs",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    class Meta:
        ordering = ["question"]
        verbose_name = "FAQ entry"
        verbose_name_plural = "FAQ entries"

    def __str__(self):
        return self.question

    def clean(self):
        errors = {}
        if self.related_category_id and self.organisation_id:
            if self.related_category.organisation_id != self.organisation_id:
                errors["related_category"] = "The category must belong to the same organisation as the FAQ."
        if self.related_sign_id and self.organisation_id:
            if self.related_sign.organisation_id != self.organisation_id:
                errors["related_sign"] = "The sign must belong to the same organisation as the FAQ."
        if errors:
            raise ValidationError(errors)


class StaffProfile(TimeStampedModel):
    class RoleType(models.TextChoices):
        STAFF = "staff", "Staff"
        MANAGER = "manager", "Organisation manager"
        GLOSSARY_MANAGER = "glossary_manager", "Glossary editor"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name="staff_profile",
        on_delete=models.CASCADE,
    )
    organisation = models.ForeignKey(
        Organisation,
        related_name="staff_profiles",
        on_delete=models.CASCADE,
    )
    role = models.CharField(max_length=120, blank=True)
    role_type = models.CharField(
        max_length=30,
        choices=RoleType.choices,
        default=RoleType.STAFF,
    )

    class Meta:
        ordering = ["organisation__name", "user__username"]

    def __str__(self):
        return f"{self.user.get_username()} - {self.organisation.name}"

    @property
    def can_triage_requests(self):
        return self.role_type == self.RoleType.MANAGER

    @property
    def can_review_glossary_content(self):
        return self.role_type == self.RoleType.GLOSSARY_MANAGER

    @property
    def can_review_requests(self):
        return self.can_triage_requests

    @property
    def can_prepare_glossary_content(self):
        return self.can_review_glossary_content


class FavouriteSign(TimeStampedModel):
    staff_profile = models.ForeignKey(
        StaffProfile,
        related_name="favourites",
        on_delete=models.CASCADE,
    )
    sign = models.ForeignKey(
        SignEntry,
        related_name="favourited_by",
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["staff_profile", "sign"],
                name="unique_favourite_sign_per_staff_profile",
            )
        ]

    def __str__(self):
        return f"{self.staff_profile.user.get_username()} favourited {self.sign.term}"

    def clean(self):
        if self.staff_profile_id and self.sign_id:
            if self.staff_profile.organisation_id != self.sign.organisation_id:
                raise ValidationError(
                    {"sign": "Staff can only favourite signs from their own organisation."}
                )


class SignRequest(TimeStampedModel):
    class RequestType(models.TextChoices):
        MISSING_SIGN = "missing_sign", "Missing sign"
        INCORRECT_SIGN = "incorrect_sign", "Incorrect sign/video"
        UNCLEAR_DESCRIPTION = "unclear_description", "Unclear description"
        WRONG_CATEGORY = "wrong_category", "Wrong category"
        POSSIBLE_DUPLICATE = "possible_duplicate", "Possible duplicate"
        BROKEN_VIDEO_LINK = "broken_video_link", "Broken video link"
        OTHER = "other", "Other"

    class Status(models.TextChoices):
        PENDING = "pending", "Pending organisation-manager review"
        NEEDS_CLARIFICATION = "needs_clarification", "Needs clarification"
        MANAGER_APPROVED = "manager_approved", "Ready for glossary review"
        SENT_TO_INTERPRETER = "sent_to_interpreter", "In glossary review"
        COMPLETED = "completed", "Completed"
        REJECTED = "rejected", "Rejected"

    organisation = models.ForeignKey(
        Organisation,
        related_name="sign_requests",
        on_delete=models.CASCADE,
    )
    requested_by = models.ForeignKey(
        StaffProfile,
        related_name="sign_requests",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    requester_name = models.CharField(max_length=150, blank=True)
    requester_email = models.EmailField(blank=True)
    term = models.CharField(max_length=200)
    context = models.TextField(help_text="Where or why this sign is needed.")
    request_type = models.CharField(
        max_length=30,
        choices=RequestType.choices,
        default=RequestType.MISSING_SIGN,
    )
    suggested_category = models.ForeignKey(
        Category,
        related_name="sign_requests",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    related_sign = models.ForeignKey(
        SignEntry,
        related_name="reports",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text="Existing sign being reported, if this request is about a current glossary entry.",
    )
    status = models.CharField(
        max_length=30,
        choices=Status.choices,
        default=Status.PENDING,
    )
    admin_notes = models.TextField(blank=True)
    approval_notes = models.TextField(
        blank=True,
        help_text="Manager feedback on the sign request."
    )
    decision_reason = models.TextField(
        blank=True,
        help_text="Reason for the organisation manager or glossary editor decision.",
    )
    interpreter_notes = models.TextField(
        "Glossary review notes",
        blank=True,
        help_text="Notes from glossary editor or ISL/content review."
    )
    reviewed_by = models.ForeignKey(
        StaffProfile,
        related_name="reviewed_sign_requests",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    reviewed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.term} request ({self.get_status_display()})"

    def clean(self):
        errors = {}
        if self.requested_by_id and self.organisation_id:
            if self.requested_by.organisation_id != self.organisation_id:
                errors["requested_by"] = "The requester must belong to the same organisation."
        if self.requested_by_id:
            self.requester_name = self.requester_name or self.requested_by.user.get_username()
            self.requester_email = self.requester_email or self.requested_by.user.email
        elif not self.requester_email:
            errors["requester_email"] = "Visitor requests need an email address for follow-up."
        if not self.requested_by_id and not self.requester_name:
            errors["requester_name"] = "Visitor requests need a requester name."
        if self.suggested_category_id and self.organisation_id:
            if self.suggested_category.organisation_id != self.organisation_id:
                errors["suggested_category"] = "The suggested category must belong to the same organisation."
        if self.related_sign_id and self.organisation_id:
            if self.related_sign.organisation_id != self.organisation_id:
                errors["related_sign"] = "The reported sign must belong to the same organisation."
        if self.reviewed_by_id and self.organisation_id:
            if self.reviewed_by.organisation_id != self.organisation_id:
                errors["reviewed_by"] = "The reviewer must belong to the same organisation."
        if errors:
            raise ValidationError(errors)


class PortalItem(TimeStampedModel):
    class ItemType(models.TextChoices):
        TASK = "task", "Task"
        APPOINTMENT = "appointment", "Appointment"
        CALENDAR_EVENT = "calendar_event", "Calendar event"
        ACCESS_NOTE = "access_note", "Access note"
        NOTE = "note", "Note"

    organisation = models.ForeignKey(
        Organisation,
        related_name="portal_items",
        on_delete=models.CASCADE,
    )
    created_by = models.ForeignKey(
        StaffProfile,
        related_name="created_portal_items",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    assigned_to = models.ForeignKey(
        StaffProfile,
        related_name="assigned_portal_items",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    item_type = models.CharField(
        max_length=30,
        choices=ItemType.choices,
        default=ItemType.TASK,
    )
    title = models.CharField(max_length=160)
    description = models.TextField(blank=True)
    due_at = models.DateTimeField(null=True, blank=True)
    is_complete = models.BooleanField(default=False)

    class Meta:
        ordering = ["is_complete", "due_at", "-created_at"]

    def __str__(self):
        return f"{self.title} ({self.organisation.name})"

    def clean(self):
        errors = {}
        if self.created_by_id and self.organisation_id:
            if self.created_by.organisation_id != self.organisation_id:
                errors["created_by"] = "The creator must belong to the same organisation."
        if self.assigned_to_id and self.organisation_id:
            if self.assigned_to.organisation_id != self.organisation_id:
                errors["assigned_to"] = "The assigned staff member must belong to the same organisation."
        if errors:
            raise ValidationError(errors)
