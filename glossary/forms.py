from django import forms


class SignSearchForm(forms.Form):
    q = forms.CharField(
        label='Search signs',
        required=False,
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Search for a sign, for example: receipt, password, help',
            'class': 'search-input',
        }),
    )
