from django import forms
from ckeditor.widgets import CKEditorWidget

from linkedin.models import Draft, Organization, Education

LEVEL = ((0, 'School'),(1,'College'),)


class DraftForm(forms.Form):
    candidate_name = forms.CharField(label=("Name*:"), max_length=85,
        widget=forms.TextInput(
        attrs={'class': 'form-control col-md-7 col-xs-12'}))

    headline = forms.CharField(label=("Headline*:"), max_length=85,
        widget=forms.TextInput(
        attrs={'class': 'form-control col-md-7 col-xs-12'}))

    summary = forms.CharField(required=True, widget=CKEditorWidget())

    profile_photo = forms.CharField(label=("Profile Photo"), max_length=85,
        widget=forms.TextInput(
        attrs={'class': 'form-control col-md-7 col-xs-12'}))

    recommendation = forms.CharField(label=("Recommendations"), max_length=85,
        widget=forms.TextInput(
        attrs={'class': 'form-control col-md-7 col-xs-12'}))
    follow_company = forms.CharField(label=("Follow companies"), max_length=85,
        widget=forms.TextInput(
        attrs={'class': 'form-control col-md-7 col-xs-12'}))
    join_group = forms.CharField(label=("Join Group"), max_length=85,
        widget=forms.TextInput(
        attrs={'class': 'form-control col-md-7 col-xs-12'}))
    public_url = forms.CharField(label=("Public Url"), max_length=85,
        widget=forms.TextInput(
        attrs={'class': 'form-control col-md-7 col-xs-12'}))
    key_skills = forms.CharField(label=("Key Skills"),
        help_text='comma separated skills, e.g. java, python; ...', 
        max_length=500,
        widget=forms.TextInput(
        attrs={'class': 'form-control col-md-7 col-xs-12'}))
    
    name = forms.CharField(label=("Company Name*:"), max_length=85,
        widget=forms.TextInput(
        attrs={'class': 'form-control col-md-7 col-xs-12'}))

    title = forms.CharField(label=("Title*:"), max_length=85,
        widget=forms.TextInput(
        attrs={'class': 'form-control col-md-7 col-xs-12'}))

    desc = forms.CharField(required=True, widget=CKEditorWidget())
    
    work_date_range = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'daterange'}))

    current = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class':'form-control col-md-7 col-xs-12'}))

    def __init__(self, *args, **kwargs):
        super(DraftForm, self).__init__(*args, **kwargs)

    
class OrganizationForm(forms.ModelForm):

    class Meta:
        model = Organization
        fields = ['name', 'title', 'desc',
        'work_from', 'work_to', 'current']
        
    def __init__(self, *args, **kwargs):
        super(OrganizationForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        draft = super(OrganizationForm, self).save(commit=False)
        if commit:
            draft.save()
        return draft


class EducationForm(forms.ModelForm):
    name = forms.CharField(label=("Name*:"), max_length=85,
        widget=forms.TextInput(
        attrs={'class': 'form-control col-md-7 col-xs-12'}))

    level = forms.ChoiceField(choices = LEVEL, 
        widget=forms.Select(attrs={'class': 'form-control col-md-7 col-xs-12'}))

    desc = forms.CharField(required=True, widget=CKEditorWidget())
    
    study_from = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'datepicker'}))

    study_to = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'datepicker'}))

    current = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class':'form-control col-md-7 col-xs-12'}))

    class Meta:
        model = Education
        fields = ['name', 'level', 'desc',
        'study_from', 'study_to', 'current']
        
    def __init__(self, *args, **kwargs):
        super(EducationForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        draft = super(EducationForm, self).save(commit=False)
        if commit:
            draft.save()
        return draft