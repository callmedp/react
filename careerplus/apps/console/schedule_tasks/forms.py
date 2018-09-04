from django import forms


class LoginTokenGenerateForm(forms.Form):
    file = forms.FileField(
        label=("File"),
        max_length=200, required=True,
        widget=forms.FileInput(attrs={
            'class': 'form-control'}))

    next_url = forms.CharField(
        label=("Next Url(relative)"),
        required=False,
        max_length=255, initial='',
        widget=forms.TextInput(attrs={
            'class': 'form-control'}))

    expiry = forms.IntegerField(
        label=("Token Expiry (in days.)"), required=False,
        initial=0,
        min_value=0,
        max_value=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super(LoginTokenGenerateForm, self).__init__(*args, **kwargs)
        # self.fields['file'].widget.attrs['data-parsley-filemimetypes'] = 'text/csv'
        self.fields['expiry'].widget.attrs['data-parsley-type'] = 'number'
        self.fields['expiry'].widget.attrs['min'] = 0
        self.fields['expiry'].widget.attrs['max'] = 100

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


class EncryptedURLSGenerateForm(forms.Form):
    file = forms.FileField(
        label=("File"),
        max_length=200, required=True,
        widget=forms.FileInput(attrs={
            'class': 'form-control'}))

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



