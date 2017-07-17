# Django imports
from django.core.validators import RegexValidator
from django import forms
from django.db.models import Q
from django.conf import settings

from .models import User
from .mixins import RegistrationLoginApi

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
    # country_choices = [(m.pk, m.phone) for m in Country.objects.exclude(Q(phone__isnull=True) | Q(phone__exact=''))]
    # indian_obj = Country.objects.filter(name='India', phone='91')[0].pk if \
    #     Country.objects.filter(name='India', phone='91').exists() else None

    email = forms.EmailField(
        max_length=60, required=True, widget=forms.TextInput(
            attrs={'placeholder': 'Email', 'class': 'form-control'}))

    raw_password = forms.CharField(
        max_length=16, required=True, widget=forms.PasswordInput(
            attrs={'placeholder': 'Password', 'class': 'form-control'}))

    country_code = forms.ChoiceField(label=("Country:"), required=True,
        widget=forms.Select(attrs={'class': 'form-control'}))

    cell_phone = forms.CharField(validators=[mobile_validators], widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Mobile'}), max_length=15)

    vendor_id = forms.CharField(
        max_length=30, required=True, initial=settings.CP_VENDOR_ID, widget=forms.HiddenInput(
            attrs={'class': 'form-control'}))

    is_job_seeker = forms.BooleanField(widget=forms.CheckboxInput(check_test=lambda x: x=='on'), initial=False)

    def clean_raw_password(self):
        password = self.cleaned_data.get('raw_password')
        password = clean_password_util(password)
        return password

    def __init__(self, *args, **kwargs):
        flavour = kwargs.pop('flavour', None)
        super(RegistrationForm, self).__init__(*args, **kwargs)

        try:
            country_choices = [(m.pk, m.phone) for m in Country.objects.exclude(Q(phone__isnull=True) | Q(phone__exact=''))]
            indian_obj = Country.objects.filter(name='India', phone='91')[0].pk if Country.objects.filter(name='India', phone='91').exists() else None
        except:
            country_choices, indian_obj = [], None
        self.fields['country_code'].choices = country_choices
        self.fields['country_code'].initial = indian_obj

        if flavour == 'mobile':
            self.fields['cell_phone'].widget.attrs = {'class': 'form-control pull-left number'}


class ModalLoginApiForm(LoginApiForm):
    pass


class ModalRegistrationApiForm(RegistrationForm):
    
    def __init__(self, *args, **kwargs):
        super(ModalRegistrationApiForm, self).__init__(*args, **kwargs)
        try:
            country_choices = [(m.phone, m.phone) for m in Country.objects.exclude(Q(phone__isnull=True) | Q(phone__exact=''))]
            indian_obj = Country.objects.filter(name='India', phone='91')[0].phone if Country.objects.filter(name='India', phone='91').exists() else None
        except:
            country_choices, indian_obj = [], None
        self.fields['country_code'].choices = country_choices
        self.fields['country_code'].initial = indian_obj

        self.fields['cell_phone'].widget.attrs['class'] = 'form-control modal-form-control'
