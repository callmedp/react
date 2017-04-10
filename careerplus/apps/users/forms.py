from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _
from django import forms
from .models import User

mobile_validators = RegexValidator(r'^[0-9]{10,15}$', 'Only numeric character required and length should be 10 and 15.')


class UserCreateForm(forms.ModelForm):

    name = forms.CharField(max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Name'}))
    email = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password1 = forms.CharField(max_length=10,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    contact_number = forms.CharField(validators=[mobile_validators], widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Mobile No.'}), max_length=10)
    
    class Meta:
        model = User
        fields = ['name', 'contact_number', 'email', 'password1']
        
    def clean_password1(self):
        min_password_length = 6
        max_password_length = 10
        password1 = self.cleaned_data.get('password1')
        if len(password1) < min_password_length:
            raise forms.ValidationError("Password must be at least 6 chars.")
        if len(password1) > max_password_length:
            raise forms.ValidationError("Password should not be greater than 10 chars.")
        return password1

    def clean_email(self):
        email = self.cleaned_data.get('email').strip()
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None
        if user:
            raise forms.ValidationError(
                'This email id already exist.'
            )
        return email

    def save(self, request, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.username = self.cleaned_data["email"]
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=100, required=True,
        widget=forms.TextInput(
            attrs={'placeholder': 'Username', 'class': 'form-control'}))

    password = forms.CharField(
        max_length=16, required=True,
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Password', 'class': 'form-control'}))