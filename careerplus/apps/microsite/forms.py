from django import forms

from resume_builder.forms import ResumeBuilderForm

class RoundoneRegisterForm(ResumeBuilderForm):
    marks_1 = forms.CharField(max_length=3, required=False)
    marks_2 = forms.CharField(max_length=2, required=False)
    resume_file = forms.FileField()

