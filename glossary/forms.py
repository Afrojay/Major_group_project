from django import forms

from .models import PortalItem, SignEntry, SignRequest


class SignRequestForm(forms.ModelForm):
    class Meta:
        model = SignRequest
        fields = [
            "requester_name",
            "requester_email",
            "request_type",
            "term",
            "suggested_category",
            "context",
        ]
        widgets = {
            "requester_name": forms.TextInput(attrs={"placeholder": "Your name"}),
            "requester_email": forms.EmailInput(attrs={"placeholder": "you@example.com"}),
            "term": forms.TextInput(attrs={"placeholder": "e.g. Password reset"}),
            "context": forms.Textarea(
                attrs={
                    "rows": 5,
                    "placeholder": "Describe the service situation where staff need this sign.",
                }
            ),
        }

    def __init__(self, *args, organisation, staff_profile=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.organisation = organisation
        if staff_profile:
            self.instance.requested_by = staff_profile
            self.instance.requester_name = staff_profile.user.get_full_name() or staff_profile.user.get_username()
            self.instance.requester_email = staff_profile.user.email
        self.fields["suggested_category"].queryset = organisation.categories.all()
        self.fields["suggested_category"].required = False
        if staff_profile:
            self.fields.pop("requester_name")
            self.fields.pop("requester_email")
        else:
            self.fields["requester_name"].required = True
            self.fields["requester_email"].required = True


class SignRequestReviewForm(forms.ModelForm):
    MANAGER_STATUS_CHOICES = [
        (SignRequest.Status.NEEDS_CLARIFICATION, "Needs clarification"),
        (SignRequest.Status.MANAGER_APPROVED, "Send to glossary review"),
        (SignRequest.Status.REJECTED, "Reject"),
    ]

    class Meta:
        model = SignRequest
        fields = ["status", "admin_notes", "decision_reason"]
        widgets = {
            "admin_notes": forms.Textarea(attrs={"rows": 3}),
            "decision_reason": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["status"].choices = self.MANAGER_STATUS_CHOICES


class SignReportForm(forms.ModelForm):
    REPORT_TYPE_CHOICES = [
        (SignRequest.RequestType.INCORRECT_SIGN, "Incorrect sign/video"),
        (SignRequest.RequestType.UNCLEAR_DESCRIPTION, "Unclear description"),
        (SignRequest.RequestType.WRONG_CATEGORY, "Wrong category"),
        (SignRequest.RequestType.POSSIBLE_DUPLICATE, "Possible duplicate"),
        (SignRequest.RequestType.BROKEN_VIDEO_LINK, "Broken video link"),
        (SignRequest.RequestType.OTHER, "Other"),
    ]

    class Meta:
        model = SignRequest
        fields = ["requester_name", "requester_email", "request_type", "context"]
        widgets = {
            "requester_name": forms.TextInput(attrs={"placeholder": "Your name"}),
            "requester_email": forms.EmailInput(attrs={"placeholder": "you@example.com"}),
            "context": forms.Textarea(
                attrs={
                    "rows": 5,
                    "placeholder": "Explain what seems incorrect, unclear, duplicated, or broken.",
                }
            ),
        }

    def __init__(self, *args, organisation, sign, staff_profile=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.organisation = organisation
        self.instance.related_sign = sign
        self.instance.term = sign.term
        self.instance.suggested_category = sign.category
        self.instance.status = SignRequest.Status.SENT_TO_INTERPRETER
        self.fields["request_type"].choices = self.REPORT_TYPE_CHOICES
        self.fields["context"].label = "What is wrong or unclear?"
        if staff_profile:
            self.instance.requested_by = staff_profile
            self.instance.requester_name = staff_profile.user.get_full_name() or staff_profile.user.get_username()
            self.instance.requester_email = staff_profile.user.email
            self.fields.pop("requester_name")
            self.fields.pop("requester_email")
        else:
            self.fields["requester_name"].required = True
            self.fields["requester_email"].required = True


class SignWorkflowForm(forms.ModelForm):
    class Meta:
        model = SignEntry
        fields = ["publication_status", "video_review_status"]


class SignEntryEditForm(forms.ModelForm):
    class Meta:
        model = SignEntry
        fields = [
            "category",
            "term",
            "slug",
            "description",
            "usage_context",
            "tags",
            "video_url",
            "thumbnail_url",
            "publication_status",
            "video_review_status",
            "is_quick_reference",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "usage_context": forms.Textarea(attrs={"rows": 5}),
            "tags": forms.TextInput(attrs={"placeholder": "Comma-separated tags"}),
        }

    def __init__(self, *args, organisation, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].queryset = organisation.categories.all()


class PortalItemForm(forms.ModelForm):
    class Meta:
        model = PortalItem
        fields = ["item_type", "title", "description", "due_at"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
            "due_at": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

    def __init__(self, *args, default_item_type=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].widget.attrs["placeholder"] = "Short title"
        self.fields["description"].widget.attrs["placeholder"] = "Optional detail or handover note"
        if default_item_type:
            self.fields.pop("item_type")


class AssignedTaskForm(forms.ModelForm):
    class Meta:
        model = PortalItem
        fields = ["assigned_to", "title", "description", "due_at"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
            "due_at": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

    def __init__(self, *args, organisation, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["assigned_to"].queryset = organisation.staff_profiles.select_related("user")
        self.fields["assigned_to"].label = "Assign to"
        self.fields["title"].widget.attrs["placeholder"] = "Task title"
        self.fields["description"].widget.attrs["placeholder"] = "What needs to be done?"
