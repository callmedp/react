from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import FAQuestion
from partner.models import Vendor

class AddFaqForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AddFaqForm, self).__init__(*args, **kwargs)
        form_class = 'form-control col-md-7 col-xs-12'
        self.fields['text'].widget.attrs['class'] = form_class
        self.fields['text'].widget.attrs['maxlength'] = 200
        self.fields['text'].widget.attrs['placeholder'] = 'Add question'
        self.fields['text'].widget.attrs['data-parsley-trigger'] = 'change'
        self.fields['text'].widget.attrs['data-parsley-required-message'] = 'This field is required.'
        self.fields['text'].widget.attrs['data-parsley-length'] = "[4, 200]"
        
        self.fields['answer'].widget.attrs['data-parsley-length-message'] = 'Length should be between 4-200 characters.'
        self.fields['answer'].widget.attrs['required'] = 'required'
        self.fields['answer'].widget.attrs['data-parsley-required-message'] = 'This field is required.'
        self.fields['vendor'].widget.attrs['class'] = form_class
        self.fields['vendor'].required=True        
        
        
    class Meta:
        model = FAQuestion
        fields = ('text', 'answer', 'vendor')

        
    def clean_text(self):
        text = self.cleaned_data.get('text', '')
        if text:
            if len(text) < 4 or len(text) > 200:
                raise forms.ValidationError(
                    "Name should be between 4-200 characters.")
        else:
            raise forms.ValidationError(
                "This field is required.")
        return text

    def clean_answer(self):
        answer = self.cleaned_data.get('answer', '')
        if answer:
            pass
        else:
            raise forms.ValidationError(
                "This field is required.")
        return answer

    def save(self, commit=True, *args, **kwargs):
        faq = super(AddFaqForm, self).save(
            commit=True, *args, **kwargs)
        return faq


class ChangeFaqForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ChangeFaqForm, self).__init__(*args, **kwargs)
        form_class = 'form-control col-md-7 col-xs-12'
        self.fields['text'].widget.attrs['class'] = form_class
        self.fields['sort_order'].widget.attrs['class'] = form_class
        self.fields['status'].widget.attrs['class'] = form_class
        self.fields['text'].widget.attrs['maxlength'] = 200
        self.fields['text'].widget.attrs['placeholder'] = 'Add question'
        self.fields['text'].widget.attrs['data-parsley-trigger'] = 'change'
        self.fields['text'].widget.attrs['data-parsley-required-message'] = 'This field is required.'
        self.fields['text'].widget.attrs['data-parsley-length'] = "[4, 200]"
        self.fields['answer'].widget.attrs['data-parsley-length-message'] = 'Length should be between 4-200 characters.'
        self.fields['answer'].widget.attrs['required'] = 'required'
        self.fields['answer'].widget.attrs['data-parsley-required-message'] = 'This field is required.'
        self.fields['vendor'].widget.attrs['class'] = form_class
        self.fields['vendor'].required=True        
        
        
    class Meta:
        model = FAQuestion
        fields = ('text', 'answer', 'status', 'sort_order',
            'vendor')

    def clean_text(self):
        text = self.cleaned_data.get('text', '')
        if text:
            if len(text) < 4 or len(text) > 200:
                raise forms.ValidationError(
                    "Name should be between 4-200 characters.")
        else:
            raise forms.ValidationError(
                "This field is required.")
        return text

    def clean_answer(self):
        answer = self.cleaned_data.get('answer', '')
        if answer:
            pass
        else:
            raise forms.ValidationError(
                "This field is required.")
        return answer

    def save(self, commit=True, *args, **kwargs):
        faq = super(ChangeFaqForm, self).save(
            commit=True, *args, **kwargs)
        return faq



class ChangePublicFaqForm(forms.ModelForm):

    public_vendor = forms.ModelMultipleChoiceField(
        queryset=Vendor.objects.all(),
        to_field_name='pk',
        widget=forms.SelectMultiple(
            attrs={'class': 'form-control col-md-7 col-xs-12'}))

    def __init__(self, *args, **kwargs):
        super(ChangePublicFaqForm, self).__init__(*args, **kwargs)

    class Meta:
        model = FAQuestion
        fields = (
            'public_vendor',)

    def clean(self):
        super(ChangePublicFaqForm, self).clean()

    