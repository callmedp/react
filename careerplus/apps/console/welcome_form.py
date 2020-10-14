from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()


class WelcomeCallActionForm(forms.Form):
    ACTION_STATUS = (
        (0, "Select Action"),
        (1, "Welcome Call Done"),
    )

    action = forms.ChoiceField(
        choices=ACTION_STATUS, initial=0, required=True, widget=forms.Select(attrs={
            'class': 'form-control col-md-7 col-xs-12',
            'required': True}))


class WelcomeCallAssignedForm(forms.Form):
    action = forms.ModelChoiceField(
        queryset=User.objects.none(),
        empty_label="Select User",
        to_field_name='pk',
        required=True, widget=forms.Select())

    def __init__(self, *args, **kwargs):
        super(WelcomeCallAssignedForm, self).__init__(*args, **kwargs)
        users = User.objects.filter(
            groups__name__in=settings.WELCOMECALL_GROUP_LIST)
        users = users.filter(is_active=True)
        self.fields['action'].required = True
        self.fields['action'].widget.attrs['class'] = 'form-control col-md-7 col-xs-12'
        self.fields['action'].queryset = users