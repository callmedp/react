from django import forms
from geolocation.models import Country


class StateForm(forms.Form):
    state_choices = [(-1, "Please select your state")]
    try:
        india_obj = Country.objects.filter(name='India', phone='91')[0]
        states = india_obj.state_set.all().order_by('name')
        for st in states:
            state_choices.append((st.id, st.name))
    except:
        pass

    state = forms.ChoiceField(required=True, choices=state_choices, initial=-1,
        widget=forms.Select(attrs={'class': 'form-control'}))
    
    def __init__(self, *args, **kwargs):
        super(StateForm, self).__init__(*args, **kwargs)

    def clean_state(self):
        state = self.cleaned_data.get('state')
        try:
            india_obj = Country.objects.filter(name='India', phone='91')[0]
            india_obj.state_set.get(id=state)
        except:
            raise forms.ValidationError(
                "Please select valid state")
        return state


class PayByCheckForm(forms.Form):

    check_no = forms.CharField(max_length=100, required=True,
        widget=forms.Select(attrs={'class': 'form-control'}))
    drawn_bank = forms.CharField(max_length=255, required=True,
        widget=forms.Select(attrs={'class': 'form-control'}))
    diposit_date = forms.CharField(max_length=50, required=True,
        widget=forms.Select(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super(PayByCheckForm, self).__init__(*args, **kwargs)

    def clean_check_no(self):
        check_no = self.cleaned_data.get('check_no').strip()
        if not check_no:
            raise forms.ValidationError(
                "This value is required.")
        elif not check_no.isdigit():
            raise forms.ValidationError(
                "Only digits required.")
        elif len(check_no) != 6:
            raise forms.ValidationError(
                "Length must be 6 digits.")
        return check_no

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