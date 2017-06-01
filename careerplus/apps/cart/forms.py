from django import forms

from .models import ShippingDetail, Cart


class ShippingDetailUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ShippingDetailUpdateForm, self).__init__(*args, **kwargs)
        form_class = 'form-control'
        self.fields['first_name'].required = True
        self.fields['first_name'].widget.attrs['placeholder'] = 'First name'
        self.fields['first_name'].widget.attrs['class'] = form_class

        self.fields['last_name'].required = True
        self.fields['last_name'].widget.attrs['placeholder'] = 'Last name'
        self.fields['last_name'].widget.attrs['class'] = form_class

        # self.fields['email'].required = True
        # self.fields['email'].widget.attrs['readonly'] = True
        # self.fields['email'].widget.attrs['placeholder'] = 'Email Id'
        # self.fields['email'].widget.attrs['class'] = form_class

        self.fields['country_code'].required = True
        self.fields['country_code'].widget.attrs['class'] = form_class

        self.fields['mobile'].required = True
        self.fields['mobile'].widget.attrs['placeholder'] = 'Mobile'
        self.fields['mobile'].widget.attrs['class'] = form_class

        self.fields['address'].required = True
        self.fields['address'].widget.attrs['placeholder'] = 'Address'
        self.fields['address'].widget.attrs['class'] = form_class

        self.fields['pincode'].required = True
        self.fields['pincode'].widget.attrs['placeholder'] = 'Pincode'
        self.fields['pincode'].widget.attrs['class'] = form_class

        self.fields['state'].required = True
        self.fields['state'].widget.attrs['placeholder'] = 'State'
        self.fields['state'].widget.attrs['class'] = form_class

        self.fields['country'].required = True
        self.fields['country'].widget.attrs['class'] = form_class

    class Meta:
        # model = ShippingDetail
        model = Cart

        fields = ['first_name', 'last_name', 'country_code', 'mobile', 'address', 'pincode', 'state', 'country']

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name', '').strip()
        if not first_name:
            raise forms.ValidationError(
                "This field is required.")
        elif not first_name.isalpha():
            raise forms.ValidationError(
                "This field should be only letters.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name', '').strip()
        if not last_name:
            raise forms.ValidationError(
                "This field is required.")
        elif not last_name.isalpha():
            raise forms.ValidationError(
                "This field should be only letters.")
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

    def clean_address(self):
        address = self.cleaned_data.get('address', '').strip()
        if not address:
            raise forms.ValidationError(
                "This field is required.")
        return address

    def clean_pincode(self):
        pincode = self.cleaned_data.get('pincode', '').strip()
        country_code = self.cleaned_data.get('country_code', None)
        if not pincode:
            raise forms.ValidationError(
                "This field is required.")
        elif not pincode.isdigit():
            raise forms.ValidationError(
                "This field required only digits.")

        elif country_code == '91' and len(pincode) != 6:
            raise forms.ValidationError(
                "pincode should be 6 digits.")

        return pincode

    def clean_state(self):
        state = self.cleaned_data.get('state', '').strip()
        if not state:
            raise forms.ValidationError(
                "This field is required.")
        return state
