from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import FAQuestion, Chapter

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

        
    class Meta:
        model = FAQuestion
        fields = ('text', 'answer')

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

        
    class Meta:
        model = FAQuestion
        fields = ('text', 'answer', 'status', 'sort_order')

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


class AddChapterForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AddChapterForm, self).__init__(*args, **kwargs)
        form_class = 'form-control col-md-7 col-xs-12'
        self.fields['heading'].widget.attrs['class'] = form_class
        self.fields['heading'].widget.attrs['maxlength'] = 200
        self.fields['heading'].widget.attrs['placeholder'] = 'Add question'
        self.fields['heading'].widget.attrs['data-parsley-trigger'] = 'change'
        self.fields['heading'].widget.attrs['data-parsley-required-message'] = 'This field is required.'
        self.fields['heading'].widget.attrs['data-parsley-length'] = "[4, 200]"
        
        self.fields['answer'].widget.attrs['data-parsley-length-message'] = 'Length should be between 4-200 characters.'
        self.fields['answer'].widget.attrs['required'] = 'required'

        self.fields['answer'].widget.attrs['data-parsley-required-message'] = 'This field is required.'

        
    class Meta:
        model = Chapter
        fields = ('heading', 'answer')

    def clean_heading(self):
        heading = self.cleaned_data.get('heading', '')
        if heading:
            if len(heading) < 4 or len(heading) > 200:
                raise forms.ValidationError(
                    "Name should be between 4-200 characters.")
        else:
            raise forms.ValidationError(
                "This field is required.")
        return heading

    def clean_answer(self):
        answer = self.cleaned_data.get('answer', '')
        if answer:
            pass
        else:
            raise forms.ValidationError(
                "This field is required.")
        return answer
    
    def save(self, commit=True, *args, **kwargs):
        chapter = super(AddChapterForm, self).save(
            commit=True, *args, **kwargs)
        return chapter


# class AddTopicForm(forms.ModelForm):

#     def __init__(self, *args, **kwargs):
#         super(AddTopicForm, self).__init__(*args, **kwargs)
#         form_class = 'form-control col-md-7 col-xs-12'
#         self.fields['name'].widget.attrs['class'] = form_class
#         self.fields['name'].widget.attrs['maxlength'] = 200
#         self.fields['name'].widget.attrs['placeholder'] = 'Add question'
#         self.fields['name'].widget.attrs['data-parsley-trigger'] = 'change'
#         self.fields['name'].widget.attrs['data-parsley-required-message'] = 'This field is required.'
#         self.fields['name'].widget.attrs['data-parsley-length'] = "[4, 200]"
        
#     class Meta:
#         model = Topic
#         fields = ('name', 'description')

#     def clean_name(self):
#         name = self.cleaned_data.get('name', '')
#         if name:
#             if len(name) < 4 or len(name) > 200:
#                 raise forms.ValidationError(
#                     "Name should be between 4-200 characters.")
#         else:
#             raise forms.ValidationError(
#                 "This field is required.")
#         return name

#     def save(self, commit=True, *args, **kwargs):
#         chapter = super(AddTopicForm, self).save(
#             commit=True, *args, **kwargs)
#         return chapter
