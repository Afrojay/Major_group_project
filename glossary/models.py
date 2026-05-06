from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse


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
    theme_colour = models.CharField(max_length=20, default="#2563eb")

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

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
    description = models.TextField(blank=True)
    usage_context = models.TextField(blank=True)
    tags = models.CharField(max_length=300, blank=True)
    is_quick_reference = models.BooleanField(default=False)

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
    is_organisation_admin = models.BooleanField(default=False)

    class Meta:
        ordering = ["organisation__name", "user__username"]

    def __str__(self):
        return f"{self.user.get_username()} - {self.organisation.name}"


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
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"
        NEEDS_CLARIFICATION = "needs_clarification", "Needs clarification"

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
    suggested_category = models.ForeignKey(
        Category,
        related_name="sign_requests",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    status = models.CharField(
        max_length=30,
        choices=Status.choices,
        default=Status.PENDING,
    )
    admin_notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.term} request ({self.get_status_display()})"

    def clean(self):
        errors = {}
        if self.requested_by_id and self.organisation_id:
            if self.requested_by.organisation_id != self.organisation_id:
                errors["requested_by"] = "The requester must belong to the same organisation."
        if self.suggested_category_id and self.organisation_id:
            if self.suggested_category.organisation_id != self.organisation_id:
                errors["suggested_category"] = "The suggested category must belong to the same organisation."
        if errors:
            raise ValidationError(errors)
