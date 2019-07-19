from django import forms


class UserQueryFilterForm(forms.Form):

    created = forms.CharField(
        label=("Added On:"), required=False,
        initial='',
        widget=forms.TextInput(attrs={
            'class': 'form-control date-range-picker',
            'placeholder': "from date - to date",
            "readonly": True, }))

    def __init__(self, *args, **kwargs):
        super(UserQueryFilterForm, self).__init__(*args, **kwargs)

    class Meta:
        fields = ['created', ]


class UserQueryActionForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(UserQueryActionForm, self).__init__(*args, **kwargs)

        ACTION_CHOICES = (
            (0, "Select Action"),
            (1, "Create Lead on crm"),
            (2, "Mark In-Active")
        )

        self.fields['action'] = forms.ChoiceField(
            label=("Action:"), choices=ACTION_CHOICES,
            required=True,
            initial=0,
            widget=forms.Select(
                attrs={'class': 'form-control col-md-7 col-xs-12'}))

    class Meta:
        fields = ['action', ]
