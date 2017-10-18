from django import forms


class WelcomeCallActionForm(forms.Form):
    ACTION_STATUS = (
        (0, "Select Action"),
        (1, "Welcome Call Done"),
    )

    action = forms.ChoiceField(
        choices=ACTION_STATUS, initial=0, required=True, widget=forms.Select(attrs={
            'class': 'form-control col-md-7 col-xs-12',
            'required': True}))