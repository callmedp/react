from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _
from django.core.validators import validate_email
from django import forms
from geolocation.models import Country
from django.db.models import Q

from .models import User
from .mixins import RegistrationLoginApi

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
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=100, required=True, widget=forms.TextInput(
            attrs={'placeholder': 'Username', 'class': 'form-control'}))

    password = forms.CharField(
        max_length=16, required=True, widget=forms.PasswordInput(
            attrs={'placeholder': 'Password', 'class': 'form-control'}))


class LoginApiForm(forms.Form):
    email = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))

    password = forms.CharField(
        max_length=16, required=True, widget=forms.PasswordInput(
            attrs={'placeholder': 'Password', 'class': 'form-control'}))


class RegistrationForm(forms.Form):
    try:
        country_choices = [(m.pk, m.phone) for m in Country.objects.exclude(Q(phone__isnull=True) | Q(phone__exact=''))]
        indian_obj = Country.objects.filter(name='India', phone='91')[0].pk if Country.objects.filter(name='India', phone='91').exists() else None
    except:
        country_choices, indian_obj = [], None

    email = forms.EmailField(
        max_length=30, required=True, widget=forms.TextInput(
            attrs={'placeholder': 'Email', 'class': 'form-control'}))

    raw_password = forms.CharField(
        max_length=16, required=True, widget=forms.PasswordInput(
            attrs={'placeholder': 'Password', 'class': 'form-control'}))

    country_code = forms.ChoiceField(label=("Country:"), required=True,
        choices=country_choices, widget=forms.Select(attrs={'class': 'form-control'}), initial=indian_obj)

    cell_phone = forms.CharField(validators=[mobile_validators], widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Mobile No.'}), max_length=10)

    vendor_id = forms.CharField(
        max_length=30, required=True,
        widget=forms.TextInput(
            attrs={'placeholder': 'Vendor Id', 'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['vendor_id'].initial = '12345'
        self.fields['vendor_id'].widget = forms.HiddenInput()
        # self.fields['country_code'].initial = [(self.indian_obj.pk,self.indian_obj.phone)]

    def clean_raw_password(self):
        min_password_length = 6
        max_password_length = 15
        password1 = self.cleaned_data.get('raw_password')
        if len(password1) < min_password_length:
            raise forms.ValidationError("Ensure this field has at least 6 characters.")
        if len(password1) > max_password_length:
            raise forms.ValidationError("Ensure this field has no more than 15 characters.")
        return password1


class ModalLoginApiForm(forms.Form):
    email = forms.EmailField(max_length=100, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))

    password = forms.CharField(
        max_length=16, required=True, widget=forms.PasswordInput(
            attrs={'placeholder': 'Password', 'class': 'form-control'}))


class ModalRegistrationApiForm(forms.Form):
    try:
        country_choices = [(m.pk, m.phone) for m in Country.objects.exclude(Q(phone__isnull=True) | Q(phone__exact=''))]
        indian_obj = Country.objects.filter(name='India', phone='91')[0].pk if Country.objects.filter(name='India', phone='91').exists() else None
    except:
        country_choices, indian_obj = [], None

    email = forms.EmailField(
        max_length=30, required=True, widget=forms.EmailInput(
            attrs={'placeholder': 'Email', 'class': 'form-control'}))

    raw_password = forms.CharField(
        max_length=16, required=True, widget=forms.PasswordInput(
            attrs={'placeholder': 'Password', 'class': 'form-control'}))

    country_code = forms.ChoiceField(label=("Country:"), required=True,
        choices=country_choices, widget=forms.Select(attrs={'class': 'form-control'}), initial=indian_obj)

    cell_phone = forms.CharField(validators=[mobile_validators], widget=forms.TextInput(
        attrs={'class': 'form-control modal-form-control', 'placeholder': 'Mobile No.'}), max_length=10)

    vendor_id = forms.CharField(
        max_length=30, required=True,
        widget=forms.TextInput(
            attrs={'placeholder': 'Vendor Id', 'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super(ModalRegistrationApiForm, self).__init__(*args, **kwargs)
        self.fields['vendor_id'].initial = '12345'
        self.fields['vendor_id'].widget = forms.HiddenInput()
        # self.fields['country_code'].initial = [(self.indian_obj.pk,self.indian_obj.phone)]

    def clean_raw_password(self):
        min_password_length = 6
        max_password_length = 15
        password1 = self.cleaned_data.get('raw_password')
        if len(password1) < min_password_length:
            raise forms.ValidationError("Ensure this field has at least 6 characters.")
        if len(password1) > max_password_length:
            raise forms.ValidationError("Ensure this field has no more than 15 characters.")
        return password1
