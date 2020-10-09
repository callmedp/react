from django import forms
from .models import Country


class CountryUpdateForm(forms.ModelForm):

    class Meta:
        model = Country
        fields = ['name', 'code2', 'code3', 'phone']

    def __init__(self, *args, **kwargs):
        super(CountryUpdateForm, self).__init__(*args, **kwargs)
        form_class = 'form-control col-md-7 col-xs-12'
        self.fields['name'].widget.attrs['class'] = form_class
        self.fields['name'].widget.attrs['minlength'] = 4
        self.fields['name'].widget.attrs['maxlength'] = 60
        self.fields['name'].widget.attrs['placeholder'] = 'Add unique cuntry name'
        self.fields['name'].widget.attrs['data-parsley-trigger'] = 'change'
        self.fields['name'].widget.attrs['data-parsley-required-message'] = 'This field is required.'
        self.fields['name'].widget.attrs['data-parsley-length'] = "[4, 60]"
        self.fields['name'].widget.attrs['data-parsley-length-message'] = 'Length should be between 4-60 characters.'

        self.fields['code2'].required = True
        self.fields['code2'].widget.attrs['class'] = form_class
        self.fields['code2'].widget.attrs['minlength'] = 2
        self.fields['code2'].widget.attrs['maxlength'] = 2
        self.fields['code2'].widget.attrs['data-parsley-trigger'] = 'change'
        self.fields['code2'].widget.attrs['data-parsley-required-message'] = 'This field is required.'
        self.fields['code2'].widget.attrs['data-parsley-length'] = "[2, 2]"
        self.fields['code2'].widget.attrs['data-parsley-length-message'] = 'Length should be 2 characters.'

        self.fields['code3'].required = True
        self.fields['code3'].widget.attrs['class'] = form_class
        self.fields['code3'].widget.attrs['minlength'] = 3
        self.fields['code3'].widget.attrs['maxlength'] = 3
        self.fields['code3'].widget.attrs['data-parsley-trigger'] = 'change'
        self.fields['code3'].widget.attrs['data-parsley-required-message'] = 'This field is required.'
        self.fields['code3'].widget.attrs['data-parsley-length'] = "[3, 3]"
        self.fields['code3'].widget.attrs['data-parsley-length-message'] = 'Length should be 3 characters.'

        self.fields['phone'].widget.attrs['class'] = form_class
        self.fields['code3'].widget.attrs['maxlength'] = 15
        self.fields['code3'].widget.attrs['data-parsley-trigger'] = 'change'
        self.fields['code3'].widget.attrs['data-parsley-required-message'] = 'This field is required.'
        self.fields['code3'].widget.attrs['data-parsley-length'] = "[0, 15]"
        self.fields['code3'].widget.attrs['data-parsley-length-message'] = 'Length should be between 0 - 15 characters.'

    def clean(self):
        fields_to_clean = ['name', 'code2', 'code3', 'phone']
        for field in fields_to_clean:
            try:
                value = self.cleaned_data.get(field).strip()
                self.cleaned_data[field] = value
            except Exception as e:
                raise forms.ValidationError(
                "%s" % (str(e)))

        return super(CountryUpdateForm, self).clean()