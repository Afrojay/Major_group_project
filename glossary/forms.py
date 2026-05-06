from django import forms

from .models import PortalItem, SignRequest


class SignRequestForm(forms.ModelForm):
    class Meta:
        model = SignRequest
        fields = ["requester_name", "requester_email", "term", "suggested_category", "context"]
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
        (SignRequest.Status.MANAGER_APPROVED, "Approve for interpreter review"),
        (SignRequest.Status.REJECTED, "Reject"),
    ]

    class Meta:
        model = SignRequest
        fields = ["status", "admin_notes"]
        widgets = {
            "admin_notes": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["status"].choices = self.MANAGER_STATUS_CHOICES


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
