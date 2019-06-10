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
        empty_label="", required=False,
        to_field_name='', widget=forms.Select(
            attrs={'class': 'form-control'}))

    vendor_text = forms.CharField(
        label=("Vendor Text:"),
        help_text=("Provide this if vendor is not present in above dropdown."),
        widget=forms.TextInput(
            attrs={'class': 'form-control'}),
        required=False
    )

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

    def clean_vendor_text(self):
        user = self.cleaned_data.get('user')
        vendor_text = self.cleaned_data.get('vendor_text')
        if not user and not vendor_text:
            raise forms.ValidationError("Please provide either vendor or vendor text.")
