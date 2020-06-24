# Django imports
from django.core.validators import RegexValidator, validate_email
from django.utils.translation import ugettext_lazy as _
from django import forms
from django.db.models import Q
from django.conf import settings
from .models import User
from .mixins import RegistrationLoginApi
import logging

from geolocation.models import Country

mobile_validators = RegexValidator(r'^[0-9]{10,15}$',
                                   'Only digits required and length should be between 10 to 15.')


def clean_password_util(password):
    min_password_length = 6
    max_password_length = 15
    if not password:
        raise forms.ValidationError("This field is required")
    if len(password) < min_password_length:
        raise forms.ValidationError("Ensure this field has at least 6 characters.")
    if len(password) > max_password_length:
        raise forms.ValidationError("Ensure this field has no more than 15 characters.")
    return password


class LoginApiForm(forms.Form):
    email = forms.CharField(max_length=50,
                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))

    password = forms.CharField(
        max_length=16, required=False, widget=forms.PasswordInput(
            attrs={'placeholder': 'Password', 'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super(LoginApiForm, self).__init__(*args, **kwargs)

    def clean_password(self):
        password = self.cleaned_data.get('password')
        password = clean_password_util(password)
        return password


class RegistrationForm(forms.Form):
    try:
        country_choices = [(m.phone, m.phone) for m in Country.objects.exclude(Q(phone__isnull=True) | Q(phone__exact=''))]
        indian_obj = Country.objects.filter(name='India', phone='91')[0].phone if Country.objects.filter(name='India', phone='91').exists() else None
    except Exception as e:
        logging.getLogger('error_log').error('unable to get country object %s' % str(e))
        country_choices, indian_obj = [], None

    email = forms.EmailField(
        max_length=60, widget=forms.TextInput(
            attrs={'placeholder': 'Email', 'class': 'form-control'}))

    raw_password = forms.CharField(
        max_length=16, widget=forms.PasswordInput(
            attrs={'placeholder': 'Password', 'class': 'form-control'}))

    country_code = forms.ChoiceField(label=("Country:"),
        widget=forms.Select(attrs={'class': 'form-control'}))

    cell_phone = forms.CharField(validators=[mobile_validators], widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Mobile'}), max_length=15)

    # vendor_id = forms.CharField(
    #     max_length=30, required=True, initial=settings.CP_VENDOR_ID, widget=forms.HiddenInput(
    #         attrs={'class': 'form-control'}))

    is_job_seeker = forms.BooleanField(widget=forms.CheckboxInput(check_test=lambda x: x=='on'), initial=False)

    def clean_raw_password(self):
        password = self.cleaned_data.get('raw_password')
        password = clean_password_util(password)
        return password

    def __init__(self, *args, **kwargs):
        flavour = kwargs.pop('flavour', None)
        super(RegistrationForm, self).__init__(*args, **kwargs)

        try:
            country_choices = [(m.phone, m.phone) for m in Country.objects.exclude(Q(phone__isnull=True) | Q(phone__exact=''))]
            indian_obj = Country.objects.filter(name='India', phone='91')[0].phone if Country.objects.filter(name='India', phone='91').exists() else None
        except Exception as e:
            logging.getLogger('error_log').error('unable to get country object %s' % str(e))
            country_choices, indian_obj = [], None
        self.fields['country_code'].choices = country_choices
        self.fields['country_code'].initial = indian_obj
        self.fields['is_job_seeker'].required = False

        if flavour == 'mobile':
            self.fields['cell_phone'].widget.attrs = {
                'class': 'form-control pull-left number',
                'inputmode': 'numeric', }

            self.fields['email'].widget.attrs['inputmode'] = 'email'


class ModalLoginApiForm(LoginApiForm):
    pass


class ModalRegistrationApiForm(RegistrationForm):
    
    def __init__(self, *args, **kwargs):
        super(ModalRegistrationApiForm, self).__init__(*args, **kwargs)
        try:
            country_choices = [(m.phone, m.phone) for m in Country.objects.exclude(Q(phone__isnull=True) | Q(phone__exact=''))]
            indian_obj = Country.objects.filter(name='India', phone='91')[0].phone if Country.objects.filter(name='India', phone='91').exists() else None
        except Exception as e:
            logging.getLogger('error_log').error('unable to get country object %s' % str(e))
            country_choices, indian_obj = [], None
        self.fields['country_code'].choices = country_choices
        self.fields['country_code'].initial = indian_obj

        self.fields['cell_phone'].widget.attrs['class'] = 'form-control modal-form-control'


class PasswordResetRequestForm(forms.Form):
    email = forms.CharField(max_length=50, validators=[validate_email],widget=forms.TextInput(
        attrs={"placeholder":"Email ID", 'class': 'form-control'}))


class SetConfirmPasswordForm(forms.Form):
    """
    A form that lets a user change set their password without entering the old
    password
    """
    min_password_length = 6
    max_password_length = 15
    error_messages = {
        'password_mismatch': ("The two password fields didn't match."),
        }
    new_password1 = forms.CharField(max_length=15,
        widget=forms.PasswordInput(attrs={'placeholder': 'New password', 'class': 'form-control',}))
    new_password2 = forms.CharField(max_length=15,
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password', 'class': 'form-control'}))

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
