
from django import forms

from wallet.models import Wallet
import logging

WalletAction = (
    ('addpoints', 'addpoints'),
    ('removepoints', 'removepoints'),
)





class Walletform(forms.Form):

    email_id = forms.EmailField(label='Email', max_length=255,required=False,widget=forms.EmailInput(attrs={'class': 'form-control col-md-7 col-xs-12'}))
    owner_id = forms.CharField(label='Owner id', max_length=255,required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control col-md-7 col-xs-12'}))
    notes = forms.CharField(widget=forms.Textarea(
            attrs={'class': 'form-control col-md-7 col-xs-12'}),required=False)
    point_value = forms.DecimalField(label='Points', decimal_places=2, max_digits=12,widget=forms.NumberInput(attrs={'class': 'form-control col-md-7 col-xs-12'}),required=False)
    wallet_action = forms.ChoiceField(label="Action", choices=WalletAction,required=False, widget=forms.RadioSelect(attrs={'class': 'form-control col-md-7 col-xs-12'}))
    order = forms.CharField(label='Order', max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'form-control col-md-7 col-xs-12'}))


    def clean_notes(self):

        note = self.cleaned_data.get('notes', '')

        if note == "":
            raise forms.ValidationError("notes cannot be empty")
        return note

    def clean_point_value(self):
        points = self.cleaned_data.get('point_value', '')
        if points == None:
            raise forms.ValidationError("Point value cannot be empty")
        return points

    def clean_wallet_action(self):
        action = self.cleaned_data.get('wallet_action', '')
        if action == "":
            raise forms.ValidationError("please select the action")
        return action


    def clean(self):


        cleaned_data = super().clean()
        email = self.cleaned_data.get('email_id', '')
        owner = self.cleaned_data.get('owner_id', '')
        walobj= ""

        if email == '' and owner == '':
            raise forms.ValidationError("Enter either Email id or Owner id")

        if email and owner == "":
            try:
                walobj = Wallet.objects.filter(owner_email=email).count()
            except Exception as e:
                logging.getLogger('error_log').error(str(e))
            if walobj > 1:
                raise forms.ValidationError("More than 1 wallet found, Please Check with Owner ID")
            if walobj < 1:
                raise forms.ValidationError("NO WALLET FOUND ")
            return cleaned_data

        if owner and email == "":
            try:
                walobj = Wallet.objects.get(owner=owner)
            except Exception as e:
                logging.getLogger('error_log').error(str(e))
            if not walobj:
                raise forms.ValidationError("NO WALLET FOUND ")
            return cleaned_data

        if email and owner:
            try:
                walobj = Wallet.objects.get(owner=owner)
            except Exception as e:
                logging.getLogger('error_log').error(str(e))

            if walobj:
                return cleaned_data
            else:
                walobj = Wallet.objects.filter(owner_email=email).count()
                if walobj == 1:
                    return cleaned_data
                else:
                    raise forms.ValidationError("unable to find wallet")























