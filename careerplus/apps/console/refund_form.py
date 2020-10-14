from django import forms
from order.choices import REFUND_OPS_STATUS


class RefundFilterForm(forms.Form):
    created = forms.CharField(
        label=("Added On:"), required=False,
        initial='',
        widget=forms.TextInput(attrs={
            'class': 'form-control date-range-picker',
            'placeholder': "from date - to date",
            "readonly": True, }))

    status = forms.ChoiceField(
        label=("Status:"), choices=[],
        required=False,
        initial=-1,
        widget=forms.Select(
            attrs={'class': 'form-control'}))

    class Meta:
        fields = ['created', 'status']

    def __init__(self, *args, **kwargs):
        super(RefundFilterForm, self).__init__(*args, **kwargs)
        NEW_STATUS = ((-1, 'Select Status'),) + REFUND_OPS_STATUS
        self.fields['status'].choices = NEW_STATUS