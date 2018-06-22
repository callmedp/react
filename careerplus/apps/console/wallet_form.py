
from django import forms

from wallet.models import Wallet
import logging

WalletAction = (
    ('addpoints', 'addpoints'),
    ('removepoints', 'removepoints'),
)





class Walletform(forms.Form):

    email_id = forms.EmailField(label='Email', max_length=255,help_text ="Enter the email address",required=False,)
    owner_id = forms.CharField(label='Owner id', max_length=255,help_text="Enter the owner id",required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control col-md-7 col-xs-12'}))
    notes = forms.CharField(widget=forms.Textarea(
            attrs={'class': 'form-control col-md-7 col-xs-12'}), required=True,help_text="This cannot be blank")
    point_value = forms.DecimalField(label='Points', decimal_places=2, max_digits=12)
    wallet_action = forms.ChoiceField(label="Action", choices=WalletAction, widget=forms.RadioSelect(attrs={'class': 'form-control col-md-7 col-xs-12'}))



    def clean_email_id(self):
        email = self.cleaned_data.get('email_id', '')
        if email:
            walobj = ""
            try:
                walobj = Wallet.objects.filter(owner_email=email).count()
            except Exception as e:
                logging.getLogger('error_log').error(str(e))
            if walobj > 1:
                raise forms.ValidationError("More than 1 wallet found, Please Check with Owner ID")
            if walobj < 1:
                raise forms.ValidationError("NO WALLET FOUND ")
        return email


    def clean_owner_id(self):
         owner = self.cleaned_data.get('owner_id', '')
         return owner


    def clean_notes(self):
        note = self.cleaned_data.get('notes', '')

        if note == "":
            raise forms.ValidationError("notes cannot be empty")
        return note

    def clean_point_value(self):
        points = self.cleaned_data.get('point_value', '')
        if points == "":
            raise forms.ValidationError("Point value cannot be empty")
        return points

    def clean_wallet_action(self):
        action = self.cleaned_data.get('wallet_action', '')
        if action == "":
            raise forms.ValidationError("please select the action")
        return action














