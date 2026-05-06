from django import forms

from .models import SignRequest


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
        self.fields["suggested_category"].queryset = organisation.categories.all()
        self.fields["suggested_category"].required = False
        if staff_profile:
            self.fields["requester_name"].required = False
            self.fields["requester_email"].required = False
            self.fields["requester_name"].widget = forms.HiddenInput()
            self.fields["requester_email"].widget = forms.HiddenInput()
        else:
            self.fields["requester_name"].required = True
            self.fields["requester_email"].required = True


class SignRequestReviewForm(forms.ModelForm):
    class Meta:
        model = SignRequest
        fields = ["status", "admin_notes"]
        widgets = {
            "admin_notes": forms.Textarea(attrs={"rows": 3}),
        }
