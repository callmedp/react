from django import forms
from django.core.validators import validate_email
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

User = get_user_model()


class PasswordResetRequestForm(forms.Form):
    email = forms.CharField(
        max_length=50, validators=[validate_email],
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': "Enter email"}))

    def clean_email(self):
        email = self.cleaned_data.get('email').strip()
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None
        if not user:
            raise forms.ValidationError(
                'This email does not exist.'
            )
        return email


class SetConfirmPasswordForm(forms.Form):
    """
    A form that lets a user change set their password without entering the old
    password
    """
    min_password_length = 6
    max_password_length = 10
    error_messages = {
        'password_mismatch': ("The two password fields didn't match."),
        }
    new_password1 = forms.CharField(
        label=("New password"), max_length=10, help_text=_('Password must be between 6 to 10 characters.'),
        widget=forms.PasswordInput(attrs={'class': 'form-control',}))
    new_password2 = forms.CharField(
        label=("New password confirmation"),max_length=10,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        password2 = self.cleaned_data.get('new_password2')
        if len(password2) < self.min_password_length:
            raise forms.ValidationError("Password must be at least 6 chars.")
        if len(password2) > self.max_password_length:
            raise forms.ValidationError("Password should not be greater than 10 chars.")
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                    )
        return password2

    def clean_new_password1(self):
        password1 = self.cleaned_data.get('new_password1')
        if len(password1) < self.min_password_length:
            raise forms.ValidationError("Password must be at least 6 chars.")
        if len(password1) > self.max_password_length:
            raise forms.ValidationError("Password should not be greater than 10 chars.")
        return password1