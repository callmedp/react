from django import forms
from django.forms.widgets import Select

from .choices import AREA_WITH_LABEL, SKILL_WITH_LABEL


class SearchForm(forms.Form):
    """
    Product Search Form
    """
    q = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'cls_input_validate cls_local_autocomplete search3 ',
                'data-rulesid':"01",'data-selecttype':'multiple','maxlength':'150','placeholder':'Type Job Title, Skills etc.','holder':'Type Job Title, Skills etc.'}),initial='')


class SearchRecommendedForm(forms.Form):
    """
    Product Recommendation Form
    """
    farea = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'data-rulesid': "01",
                'data-selecttype': 'multiple',
                'maxlength': '150',
                'placeholder': 'Functional Area',
                'holder': 'Functional Area'}),
        initial='',
        choices=AREA_WITH_LABEL)
    skill = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'maxlength':'150',
                'placeholder':'Skill',
                'holder':'skill'
            }
        ),
        initial='',
        choices=SKILL_WITH_LABEL)
