from django import forms
from django.db.models import Q
from django.utils.safestring import mark_safe
from geolocation.models import Country

from .models import Cart


class ShippingDetailUpdateForm(forms.ModelForm):
    country_code = forms.ChoiceField(
        required=True, widget=forms.Select())
    # country = forms.ChoiceField(
    #     required=True, widget=forms.Select())
    country = forms.ModelChoiceField(
        queryset=Country.objects.filter(active=True),
        empty_label='Select Country',
        required=True,
        to_field_name='pk',
        widget=forms.Select())

    class Meta:
        model = Cart

        fields = ['first_name', 'last_name', 'email', 'country_code', 'mobile', 'country']

    def __init__(self, *args, **kwargs):
        flavour = kwargs.pop('flavour', None)
        super(ShippingDetailUpdateForm, self).__init__(*args, **kwargs)
        try:
            country_choices = []
            for m in Country.objects.exclude(Q(phone__isnull=True) | Q(phone__exact='') | Q(active__exact=False)):
                choice_name = m.phone + '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -- &nbsp;&nbsp;&nbsp;&nbsp;' + m.name
                choice_name = mark_safe(choice_name)
                country_choices.append((m.phone, choice_name))

        except:
            country_choices = [('91', mark_safe('91 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -- &nbsp;&nbsp;&nbsp;&nbsp; India'))]

        form_class = 'form-control'
        self.fields['first_name'].required = True
        self.fields['first_name'].widget.attrs['placeholder'] = ''
        self.fields['first_name'].widget.attrs['class'] = form_class

        self.fields['last_name'].required = True
        self.fields['last_name'].widget.attrs['placeholder'] = ''
        self.fields['last_name'].widget.attrs['class'] = form_class

        self.fields['email'].required = True
        self.fields['email'].widget.attrs['placeholder'] = ''
        self.fields['email'].widget.attrs['class'] = form_class

        self.fields['country_code'].required = True
        self.fields['country_code'].widget.attrs['class'] = form_class
        self.fields['country_code'].choices = country_choices
        self.fields['country_code'].initial = '91'
        
        self.fields['mobile'].required = True
        self.fields['mobile'].widget.attrs['placeholder'] = ''
        self.fields['mobile'].widget.attrs['class'] = form_class

        if flavour == 'mobile':
            self.fields['mobile'].widget.attrs['class'] += ' pull-left number'

        # self.fields['address'].required = False
        # self.fields['address'].widget.attrs['placeholder'] = 'Address'
        # self.fields['address'].widget.attrs['class'] = form_class

        # self.fields['pincode'].required = False
        # self.fields['pincode'].widget.attrs['placeholder'] = 'Pincode'
        # self.fields['pincode'].widget.attrs['class'] = form_class
        # if flavour == 'mobile':
        #     self.fields['pincode'].widget.attrs['class'] += ' pull-left number'

        # self.fields['state'].required = False
        # self.fields['state'].widget.attrs['placeholder'] = 'State'
        # self.fields['state'].widget.attrs['class'] = form_class

        # if flavour == 'mobile':
        #     self.fields['state'].widget.attrs['class'] += ' pull-left w-50'

        self.fields['country'].required = True
        self.fields['country'].widget.attrs['class'] = form_class

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name', '').strip()
        if not first_name:
            raise forms.ValidationError(
                "This field is required.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name', '').strip()
        if not last_name:
            raise forms.ValidationError(
                "This field is required.")
        return last_name

    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile', '').strip()
        country_code = self.cleaned_data.get('country_code', None)

        if not mobile:
            raise forms.ValidationError(
                "This field is required.")

        elif not mobile.isdigit():
            raise forms.ValidationError(
                "This field required only digits.")

        elif country_code == '91' and len(mobile) != 10:
            raise forms.ValidationError(
                "Mobile number contains only 10 digits.")

        elif len(mobile) < 4 or len(mobile) > 15:
            raise forms.ValidationError(
                "Mobile length must be 4 to 15 digits.")
        return mobile

    # def clean_address(self):
    #     address = self.cleaned_data.get('address', '').strip()
        # if not address:
        #     raise forms.ValidationError(
        #         "This field is required.")
        # return address
    #
    # def clean_pincode(self):
    #     pincode = self.cleaned_data.get('pincode', '').strip()
        # country_code = self.cleaned_data.get('country_code', None)
        # if not pincode:
        #     raise forms.ValidationError(
        #         "This field is required.")
        # elif not pincode.isdigit():
        #     raise forms.ValidationError(
        #         "This field required only digits.")
        #
        # elif country_code == '91' and len(pincode) != 6:
        #     raise forms.ValidationError(
        #         "pincode should be 6 digits.")

        # return pincode

    # def clean_state(self):
    #     state = self.cleaned_data.get('state', '').strip()
        # if not state:
        #     raise forms.ValidationError(
        #         "This field is required.")
        # return state
