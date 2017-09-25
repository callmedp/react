from django import forms
from django.forms.widgets import Select

from .choices import AREA_WITH_LABEL, SKILL_WITH_LABEL


class SearchForm(forms.Form):
    """
    Product Search Form
    """
    # These are the search text boxes on search page
    q = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'data-rulesid': "01",
                'data-selecttype': 'multiple',
                'maxlength': '150',
                'placeholder': 'Search for courses, services etc..',
                'holder': 'Search for courses, services etc..'}
        ),
        initial='')


class SearchRecommendedForm(forms.Form):
    """
    Product Recommendation Form
    """
    area = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control js_area',
                'data-rulesid': "01",
                'data-selecttype': 'multiple',
                'maxlength': '150',
                'placeholder': 'Functional Area',
                'holder': 'Functional Area'}),
        initial=''
    )
    skills = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control js_skill',
                'maxlength':'150',
                'placeholder':'Key Skills',
                'holder': 'Key Skills'
            }
        ),
        initial=''
    )
