from django import forms
from .models import Review


class ReviewForm(forms.Form):

    rating = forms.IntegerField(required=True, min_value=1, max_value=5)
    title = forms.CharField(required=True, max_length=100)
    review = forms.CharField(max_length=1500)
