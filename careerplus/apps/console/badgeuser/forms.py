from django import forms
from partner.models import Vendor


class UploadCertificateForm(forms.Form):
    file = forms.FileField(
        label=("File:"),
        max_length=200, required=True,
        widget=forms.FileInput(attrs={
            'class': 'form-control'}))
    user = forms.ModelChoiceField(
        label=("Vendor:"),
        queryset=Vendor.objects.exclude(email__exact='').order_by('name'),
        empty_label="", required=True,
        to_field_name='', widget=forms.Select(
            attrs={'class': 'form-control'}))

    def __init__(self, requestuser=None, *args, **kwargs):
        super(UploadCertificateForm, self).__init__(*args, **kwargs)
        # self.fields['file'].widget.attrs['data-parsley-filemimetypes'] = 'text/csv'
        try:
            vobj = Vendor.objects.get(email=requestuser.user.email)
            self.fields['user'].empty_label = vobj.name
        except:
            self.fields['user'].empty_label = "select vendor"

    def clean_file(self):
        file = self.files.get('file', '')
        if not file:
            raise forms.ValidationError(
                "file is required.")
        elif file:
            name = file.name
            extn = name.split('.')[-1]
            if extn not in ['csv', ]:
                raise forms.ValidationError(
                    "only csv formats are allowed.")
            elif file.size > 5 * 1024 * 1024:
                raise forms.ValidationError(
                    "file is too large ( > 5mb ).")
        return file