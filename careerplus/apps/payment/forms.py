from django import forms
from geolocation.models import Country
import logging


class StateForm(forms.Form):
    state = forms.ChoiceField(
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super(StateForm, self).__init__(*args, **kwargs)

        state_choices = [(-1, "Please select your state")]
        try:
            india_obj = Country.objects.filter(phone='91')[0]
            states = india_obj.state_set.all().order_by('name')
            for st in states:
                state_choices.append((st.id, st.name))
        except:
            logging.getLogger('error_log').error('unable to set states')
            pass
        self.fields['state'].choices = state_choices
        self.fields['state'].initial = -1

    def clean_state(self):
        state = self.cleaned_data.get('state')
        try:
            india_obj = Country.objects.filter(phone='91')[0]
            india_obj.state_set.get(id=state)
        except:
            raise forms.ValidationError(
                "Please select valid state")
        return state


class PayByCheckForm(forms.Form):

    cheque_no = forms.CharField(
        max_length=100, required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    drawn_bank = forms.CharField(
        max_length=255, required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    deposit_date = forms.CharField(
        max_length=50, required=True,
        widget=forms.TextInput(attrs={'class': 'form-control datepicker'}))

    def __init__(self, *args, **kwargs):
        super(PayByCheckForm, self).__init__(*args, **kwargs)
        self.fields['cheque_no'].widget.attrs['placeholder'] = 'Check no.*'
        self.fields['drawn_bank'].widget.attrs['placeholder'] = 'Drawn On Bank*'
        self.fields['deposit_date'].widget.attrs['placeholder'] = 'Date of Deposit*'
        self.fields['deposit_date'].widget.attrs['data-date-format'] = 'MM/DD/YYYY'

    def clean_cheque_no(self):
        cheque_no = self.cleaned_data.get('cheque_no').strip()
        if not cheque_no:
            raise forms.ValidationError(
                "This value is required.")
        elif not cheque_no.isdigit():
            raise forms.ValidationError(
                "Only digits required.")
        elif len(cheque_no) != 6:
            raise forms.ValidationError(
                "Length must be 6 digits.")
        return cheque_no

    def clean_drawn_bank(self):
        drawn_bank = self.cleaned_data.get('drawn_bank').strip()
        if not drawn_bank:
            raise forms.ValidationError(
                "This value is required.")
        return drawn_bank

    def clean_diposit_date(self):
        diposit_date = self.cleaned_data.get('diposit_date').strip()
        if not diposit_date:
            raise forms.ValidationError(
                "This value is required.")
        return diposit_date