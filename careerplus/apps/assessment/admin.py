#python imports
import json

from django.contrib import admin
from .models import *
from shop.models import Category,Product
from django import forms

# Register your models here.


class TestForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(TestForm,self).__init__(*args,**kwargs)
        form_class = 'form-control col-md-7 col-xs-12'
        queryset = Category.objects.filter(type_level=3).only('id','name')
        # pqueryset = Product.selected.all().only('id','name')
        self.fields['category'].queryset = queryset
        self.fields['categories'].queryset = queryset
        # self.fields['product'].queryset = pqueryset
        # self.fields['course'].queryset = pqueryset
        # self.fields['category'].widget.attrs['class'] = form_class
        #

    def clean(self):
        super(TestForm, self).clean()
        if not self.cleaned_data.get('category'):
            raise forms.ValidationError("Category cannot be empty ")
        if self.cleaned_data.get('category') in self.cleaned_data.get('categories'):
            return
        raise forms.ValidationError("Category should be in Categories")

    class Meta:
        model = Test
        fields = '__all__'


class test(admin.ModelAdmin):
    form = TestForm
    raw_id_fields = ('product','course','vendor')
    list_display = ['id','slug','title','category','product']


class QuestionForm(forms.ModelForm):

    def __init__(self,*args,**kwargs):
        super(QuestionForm,self).__init__(*args,**kwargs)
        self.fields['question_options'].help_text = '[{"is_correct": "0", ' \
'"option_id": "1157a", "option_image": "", "option": "horizontal pod autoscaler"}]'


    def clean_question_options(self):
        if not self.cleaned_data.get('question_options'):
            raise forms.ValidationError('Options cannot be empty')
        value = self.cleaned_data.get('question_options')
        try:
            value = json.loads(value)
        except Exception as e:
            value = None

        if not isinstance(value,list):
            raise forms.ValidationError('[{"is_correct": "0", "option_id": "1157a",'
                                        ' "option_image": "", '
                                        '"option": "horizontal pod '
                                        'autoscaler"}]')
        if not all(isinstance(option, dict) for option in value):
            raise forms.ValidationError('[{"is_correct": "0", "option_id": "1157a",'
                                        ' "option_image": "", '
                                        '"option": "horizontal pod '
                                        'autoscaler"}]')
        return value

    class Meta:
        fields = '__all__'

class QuestionAdmin(admin.ModelAdmin):
    form = QuestionForm
admin.site.register(Test,test)
admin.site.register(Question,QuestionAdmin)