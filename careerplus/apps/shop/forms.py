from django import forms
from shop.models import Keyword


class AddKeywordForm(forms.ModelForm):
    
    class Meta:
        model = Keyword
        fields = ['name', 'active']
        
    def __init__(self, *args, **kwargs):
        super(AddKeywordForm, self).__init__(*args, **kwargs)
        form_class = 'form-control col-md-7 col-xs-12'
        self.fields['name'].widget.attrs['class'] = form_class
        self.fields['name'].widget.attrs['maxlength'] = 80
        self.fields['name'].widget.attrs['placeholder'] = 'Add unique keyword'
        self.fields['name'].widget.attrs['data-parsley-trigger'] = 'change'
        self.fields['name'].widget.attrs['data-parsley-required-message'] = 'This field is required.'
        self.fields['name'].widget.attrs['data-parsley-length'] = "[4, 60]"
        self.fields['name'].widget.attrs['data-parsley-length-message'] = 'Length should be between 4-60 characters.'
        
        self.fields['active'].widget.attrs['class'] = 'js-switch'
        self.fields['active'].widget.attrs['data-switchery'] = 'true'

    def clean_name(self):
        name = self.cleaned_data.get('name', '')
        if name:
            if len(name) < 4 or len(name) > 60:
                raise forms.ValidationError(
                    "Name should be between 4-60 characters.")
        else:
            raise forms.ValidationError(
                "This field is required.")
        return name
    

    def save(self, commit=True):
        keyword = super(AddKeywordForm, self).save(commit=False)
        if commit:
            keyword.save()
        return keyword


class AddAttributeForm(forms.ModelForm):
    
    class Meta:
        model = Keyword
        fields = ['name', 'active']
        
    def __init__(self, *args, **kwargs):
        super(AddAttributeForm, self).__init__(*args, **kwargs)
        

    def clean_name(self):
        name = self.cleaned_data.get('name', '')
        if name:
            if len(name) < 4 or len(name) > 60:
                raise forms.ValidationError(
                    "Name should be between 4-60 characters.")
        else:
            raise forms.ValidationError(
                "This field is required.")
        return name
    

    def save(self, commit=True):
        keyword = super(AddAttributeForm, self).save(commit=False)
        if commit:
            keyword.save()
        return keyword


class AddAttributeOptionForm(forms.ModelForm):
    
    class Meta:
        model = Keyword
        fields = ['name', 'active']
        
    def __init__(self, *args, **kwargs):
        super(AddAttributeOptionForm, self).__init__(*args, **kwargs)
        
    def clean_name(self):
        name = self.cleaned_data.get('name', '')
        if name:
            if len(name) < 4 or len(name) > 60:
                raise forms.ValidationError(
                    "Name should be between 4-60 characters.")
        else:
            raise forms.ValidationError(
                "This field is required.")
        return name
    

    def save(self, commit=True):
        keyword = super(AddAttributeOptionForm, self).save(commit=False)
        if commit:
            keyword.save()
        return keyword
