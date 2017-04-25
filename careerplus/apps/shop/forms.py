from django import forms

from shop.models import Product
from partner.models import Vendor


class ProductAddForm(forms.ModelForm):
    name = forms.CharField(label=("Name*:"), max_length=85,
        widget=forms.TextInput(
        attrs={'class': 'form-control col-md-7 col-xs-12'}))

    slug = forms.SlugField(label=("Slug:"), max_length=90,
        widget=forms.TextInput(
            attrs={'class': 'form-control col-md-7 col-xs-12'}))

    active = forms.BooleanField(label=("Active:"),
        widget=forms.CheckboxInput())

    vendor = forms.ModelChoiceField(label=("vendor"),
            queryset=Vendor.objects.all(), to_field_name='pk',
            widget=forms.Select(attrs={'class': 'form-control col-md-7 col-xs-12'}))
    
    class Meta:
        model = Product
        fields = ['name', 'slug', 'avg_rating', 'active', 'vendor']
        
    def __init__(self, *args, **kwargs):
        super(ProductAddForm, self).__init__(*args, **kwargs)
        self.fields['active'].required = False  

    def clean(self):
        fields = ['name', 'slug']
        for field in fields:
            try:
                val = self.cleaned_data.get(field).strip()
                self.cleaned_data[field] = val
            except:
                continue
        return super(ProductAddForm, self).clean()

    def save(self, commit=True):
        product = super(ProductAddForm, self).save(commit=False)
        if commit:
            product.save()
        return product