from django import forms


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
                'holder': 'Search for courses, services etc..',
                'autocomplete': 'off'}
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
                'maxlength': '150',
                'placeholder': 'Select Functional Area'}),
        initial=''
    )
    skills = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control js_skill',
                'maxlength':'150',
                'placeholder':'Choose upto 2 Skills'
            }
        ),
        initial=''
    )
