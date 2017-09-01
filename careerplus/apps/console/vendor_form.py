from decimal import Decimal
from django import forms
from django.core import exceptions
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from django.conf import settings
from .decorators import has_group
from shop.models import (
    ProductClass,
    ProductScreen, 
    FAQProductScreen,
    VariationProductScreen,
    ScreenChapter)
from faq.models import ScreenFAQ
from partner.models import Vendor
from geolocation.models import Country
from shop.utils import ProductAttributesContainer
from faq.models import ScreenFAQ, FAQuestion
from shop.utils import ProductAttributesContainer

from shop.choices import (
    BG_CHOICES,
    PRODUCT_VENDOR_CHOICES)
from shop.utils import FIELD_FACTORIES


class AddScreenFaqForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AddScreenFaqForm, self).__init__(*args, **kwargs)
        form_class = 'form-control col-md-7 col-xs-12'
        self.fields['text'].widget.attrs['class'] = form_class
        self.fields['text'].widget.attrs['maxlength'] = 200
        self.fields['text'].widget.attrs['placeholder'] = 'Add question'
        self.fields['text'].widget.attrs['data-parsley-trigger'] = 'change'
        self.fields['text'].widget.attrs['data-parsley-required-message'] = 'This field is required.'
        self.fields['text'].widget.attrs['data-parsley-length'] = "[3, 200]"
        
        self.fields['answer'].widget.attrs['data-parsley-length-message'] = 'Length should be between 3-200 characters.'
        self.fields['answer'].widget.attrs['required'] = 'required'

        self.fields['answer'].widget.attrs['data-parsley-required-message'] = 'This field is required.'

        
    class Meta:
        model = ScreenFAQ
        fields = ('text', 'answer')

        
    def clean_text(self):
        text = self.cleaned_data.get('text', '')
        if text:
            if len(text) < 3 or len(text) > 200:
                raise forms.ValidationError(
                    "Name should be between 4-200 characters.")
        else:
            raise forms.ValidationError(
                "This field is required.")
        return text

    def clean_answer(self):
        answer = self.cleaned_data.get('answer', '')
        if answer:
            pass
        else:
            raise forms.ValidationError(
                "This field is required.")
        return answer

    def save(self, commit=True, *args, **kwargs):
        faq = super(AddScreenFaqForm, self).save(
            commit=True, *args, **kwargs)
        return faq


class ChangeScreenFaqForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ChangeScreenFaqForm, self).__init__(*args, **kwargs)
        form_class = 'form-control col-md-7 col-xs-12'
        self.fields['text'].widget.attrs['class'] = form_class
        self.fields['sort_order'].widget.attrs['class'] = form_class
        self.fields['text'].widget.attrs['maxlength'] = 200
        self.fields['text'].widget.attrs['placeholder'] = 'Add question'
        self.fields['text'].widget.attrs['data-parsley-trigger'] = 'change'
        self.fields['text'].widget.attrs['data-parsley-required-message'] = 'This field is required.'
        self.fields['text'].widget.attrs['data-parsley-length'] = "[3, 200]"
        self.fields['answer'].widget.attrs['data-parsley-length-message'] = 'Length should be between 3-200 characters.'
        self.fields['answer'].widget.attrs['required'] = 'required'
        self.fields['answer'].widget.attrs['data-parsley-required-message'] = 'This field is required.'

        
    class Meta:
        model = ScreenFAQ
        fields = ('text', 'answer', 'sort_order')

    def clean_text(self):
        text = self.cleaned_data.get('text', '')
        if text:
            if len(text) < 3 or len(text) > 200:
                raise forms.ValidationError(
                    "Name should be between 4-200 characters.")
        else:
            raise forms.ValidationError(
                "This field is required.")
        return text

    def clean_answer(self):
        answer = self.cleaned_data.get('answer', '')
        if answer:
            pass
        else:
            raise forms.ValidationError(
                "This field is required.")
        return answer

    def save(self, commit=True, *args, **kwargs):
        faq = super(ChangeScreenFaqForm, self).save(
            commit=True, *args, **kwargs)
        if not faq.status == 2:
            faq.status = 1
            faq.save()
        return faq


class AddScreenProductForm(forms.ModelForm):

    class Meta:
        model = ProductScreen
        fields = [
            'name', 'product_class',
            'type_product', 'upc', 'inr_price']


    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(AddScreenProductForm, self).__init__(*args, **kwargs)
        form_class = 'form-control col-md-7 col-xs-12'
        vendor = self.user.get_vendor()
        self.fields['product_class'].widget.attrs['class'] = form_class
        self.fields['product_class'].empty_label = 'Select Product Class'
        self.fields['product_class'].required = True
        self.fields['type_product'].widget.attrs['class'] = form_class
        if has_group(user=self.user, grp_list=settings.PRODUCT_GROUP_LIST):
            self.fields['type_product'].choices = PRODUCT_VENDOR_CHOICES + ((3, 'Combo'),
                (4, 'No-Direct-Sell/Virtual'),
                (5, 'Downloadable'),)
        else:
            self.fields['type_product'].choices = PRODUCT_VENDOR_CHOICES
        
        if not vendor:
            if has_group(user=self.user, grp_list=settings.PRODUCT_GROUP_LIST):
                pass
            else:
                self.fields['product_class'].queryset = ProductClass.objects.none()
        else:
            self.fields['product_class'].queryset = vendor.prd_add_class.all()
                       
        self.fields['inr_price'].widget.attrs['class'] = form_class
        self.fields['inr_price'].required = False
        
        self.fields['name'].widget.attrs['class'] = form_class
        self.fields['name'].widget.attrs['maxlength'] = 80
        self.fields['name'].widget.attrs['placeholder'] = 'Add Product Name'
        self.fields['name'].widget.attrs['data-parsley-trigger'] = 'change'
        self.fields['name'].widget.attrs['data-parsley-required-message'] = 'This field is required.'
        self.fields['name'].widget.attrs['data-parsley-length'] = "[3, 60]"
        self.fields['name'].widget.attrs['data-parsley-length-message'] = 'Length should be between 3-60 characters.'
        
        self.fields['upc'].widget.attrs['class'] = form_class
        self.fields['upc'].widget.attrs['maxlength'] = 80
        self.fields['upc'].widget.attrs['placeholder'] = 'Add Universal Product Code'
        self.fields['upc'].widget.attrs['data-parsley-trigger'] = 'change'
        self.fields['upc'].widget.attrs['data-parsley-required-message'] = 'This field is required.'
        self.fields['upc'].widget.attrs['data-parsley-length'] = "[3, 60]"
        self.fields['upc'].widget.attrs['data-parsley-length-message'] = 'Length should be between 3-60 characters.'

    def clean_name(self):
        name = self.cleaned_data.get('name', '')
        if name:
            if len(name) < 3 or len(name) > 60:
                raise forms.ValidationError(
                    "Name should be between 4-60 characters.")
        else:
            raise forms.ValidationError(
                "This field is required.")
        return name

    def clean_product_class(self):
        prd_class = self.cleaned_data.get('product_class', '')
        if prd_class:
            vendor = self.user.get_vendor()
            if not vendor:
                raise forms.ValidationError(
                    "You are not associated to vendor.")
            else:
                if not prd_class in vendor.prd_add_class.all():
                    raise forms.ValidationError(
                    "The value is Invalid.")
        else:
            raise forms.ValidationError(
                "This field is required.")
        return prd_class
    
    def clean_upc(self):
        upc = self.cleaned_data.get('upc', '')
        if upc:
            if len(upc) < 3 or len(upc) > 60:
                raise forms.ValidationError(
                    "Name should be between 4-60 characters.")
        else:
            raise forms.ValidationError(
                "This field is required.")
        return upc

    def clean_inr_price(self):
        inr_price = self.cleaned_data.get('inr_price', '')
        if inr_price:
            if inr_price < Decimal(0):
                raise forms.ValidationError(
                    "This value cannot be negative.")
        return inr_price
    
    def save(self, commit=True, *args, **kwargs):
        productscreen = super(AddScreenProductForm, self).save(
            commit=True, *args, **kwargs)
        return productscreen


class ChangeScreenProductForm(forms.ModelForm):

    class Meta:
        model = ProductScreen
        fields = [
            'name', 
            'upc', 
            'about', 'description',
            'buy_shine','prg_structure' ]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ChangeScreenProductForm, self).__init__(*args, **kwargs)
        form_class = 'form-control col-md-7 col-xs-12'
                       
        self.fields['name'].widget.attrs['class'] = form_class
        self.fields['name'].widget.attrs['maxlength'] = 80
        self.fields['name'].widget.attrs['placeholder'] = 'Add Product Name'
        self.fields['name'].widget.attrs['data-parsley-trigger'] = 'change'
        self.fields['name'].widget.attrs['data-parsley-required-message'] = 'This field is required.'
        self.fields['name'].widget.attrs['data-parsley-length'] = "[3, 60]"
        self.fields['name'].widget.attrs['data-parsley-length-message'] = 'Length should be between 4-60 characters.'
        
        self.fields['upc'].widget.attrs['class'] = form_class
        self.fields['upc'].widget.attrs['maxlength'] = 80
        self.fields['upc'].widget.attrs['placeholder'] = 'Add Universal Product Code'
        self.fields['upc'].widget.attrs['data-parsley-trigger'] = 'change'
        self.fields['upc'].widget.attrs['data-parsley-required-message'] = 'This field is required.'
        self.fields['upc'].widget.attrs['data-parsley-length'] = "[3, 60]"
        self.fields['upc'].widget.attrs['data-parsley-length-message'] = 'Length should be between 4-60 characters.'
    

    def clean_name(self):
        name = self.cleaned_data.get('name', '')
        if name:
            if len(name) < 3 or len(name) > 60:
                raise forms.ValidationError(
                    "Name should be between 4-60 characters.")
        else:
            raise forms.ValidationError(
                "This field is required.")
        return name

    
    def clean_upc(self):
        upc = self.cleaned_data.get('upc', '')
        if upc:
            if len(upc) < 3 or len(upc) > 60:
                raise forms.ValidationError(
                    "Name should be between 4-60 characters.")
        else:
            raise forms.ValidationError(
                "This field is required.")
        return upc

    
    def clean_description(self):
        desc = self.cleaned_data.get('description', '')
        if desc:
            pass
        else:
            raise forms.ValidationError(
                "This field is required.")
        return desc

    def clean_about(self):
        about = self.cleaned_data.get('about', '')
        if about:
            pass
        else:
            raise forms.ValidationError(
                "This field is required.")
        return about

    def clean_prg_structure(self):
        about = self.cleaned_data.get('prg_structure', '')
        if about:
            pass
        else:
            raise forms.ValidationError(
                "This field is required.")
        return about

    def clean_buy_shine(self):
        buy_shine = self.cleaned_data.get('buy_shine', '')
        if buy_shine:
            pass
        else:
            raise forms.ValidationError(
                "This field is required.")
        return buy_shine

    
    def save(self, commit=True, *args, **kwargs):
        productscreen = super(ChangeScreenProductForm, self).save(
            commit=True, *args, **kwargs)
        productscreen.status = 1
        productscreen.save()
        return productscreen


class ScreenProductPriceForm(forms.ModelForm):

    class Meta:
        model = ProductScreen
        fields = [
            'inr_price', 'fake_inr_price',
            'usd_price', 'fake_usd_price', 
            'aed_price', 'fake_aed_price',
            'gbp_price', 'fake_gbp_price',]

    def __init__(self, *args, **kwargs):
        super(ScreenProductPriceForm, self).__init__(*args, **kwargs)
        form_class = 'form-control col-md-7 col-xs-12'
        instance = self.instance
        self.currency = instance.countries.values_list('currency__value',flat=True).distinct()
        self.currency = set(self.currency)
        self.fields['inr_price'].widget.attrs['class'] = form_class
        self.fields['inr_price'].required = True
        self.fields['usd_price'].widget.attrs['class'] = form_class
        self.fields['aed_price'].widget.attrs['class'] = form_class
        self.fields['gbp_price'].widget.attrs['class'] = form_class
        self.fields['fake_inr_price'].widget.attrs['class'] = form_class
        self.fields['fake_usd_price'].widget.attrs['class'] = form_class
        self.fields['fake_aed_price'].widget.attrs['class'] = form_class
        self.fields['fake_gbp_price'].widget.attrs['class'] = form_class

    def clean(self):
        
        super(ScreenProductPriceForm, self).clean()
        if any(self.errors):
            return
        inr_price = self.cleaned_data.get('inr_price', '')
        usd_price = self.cleaned_data.get('usd_price', '')
        aed_price = self.cleaned_data.get('aed_price', '')
        gbp_price = self.cleaned_data.get('gbp_price', '')

        if 0 in self.currency and inr_price < 0:
            raise forms.ValidationError(
                "INR Price is required as product is visible in respective country.")
        if 1 in self.currency and usd_price < 0:
            raise forms.ValidationError(
                "USD Price is required as product is visible in respective country.")
        if 2 in self.currency and aed_price < 0:
            raise forms.ValidationError(
                "AED Price is required as product is visible in respective country.")
        if 3 in self.currency and gbp_price < 0:
            raise forms.ValidationError(
                "GBP Price is required as product is visible in respective country.")

            

    def clean_inr_price(self):
        inr_price = self.cleaned_data.get('inr_price', '')
        inr_price = self.cleaned_data.get('inr_price', '')
        if inr_price:
            if inr_price < Decimal(0):
                raise forms.ValidationError(
                    "This value cannot be negative.")
        return inr_price
    def clean_usd_price(self):
        usd_price = self.cleaned_data.get('usd_price', '')
        if usd_price:
            if usd_price < Decimal(0):
                raise forms.ValidationError(
                    "This value cannot be negative.")
        return usd_price

    def clean_aed_price(self):
        aed_price = self.cleaned_data.get('aed_price', '')
        if aed_price:
            if aed_price < Decimal(0):
                raise forms.ValidationError(
                    "This value cannot be negative.")
        return aed_price

    def clean_gbp_price(self):
        gbp_price = self.cleaned_data.get('gbp_price', '')
        if gbp_price:
            if gbp_price < Decimal(0):
                raise forms.ValidationError(
                    "This value cannot be negative.")
        return gbp_price

    def clean_fake_usd_price(self):
        usd_price = self.cleaned_data.get('usd_price', '')
        fake_usd_price = self.cleaned_data.get('fake_usd_price', '')
        if fake_usd_price:
            if fake_usd_price < Decimal(0):
                raise forms.ValidationError(
                    "This value cannot be negative.")
            elif fake_usd_price > Decimal(0):
                if fake_usd_price <= usd_price:
                    raise forms.ValidationError(
                        "This value should be greater than true price.")
        return fake_usd_price

    def clean_fake_inr_price(self):
        inr_price = self.cleaned_data.get('inr_price', '')
        fake_inr_price = self.cleaned_data.get('fake_inr_price', '')
        if fake_inr_price:
            if fake_inr_price < Decimal(0):
                raise forms.ValidationError(
                    "This value cannot be negative.")
            elif fake_inr_price > Decimal(0):
                if fake_inr_price <= inr_price:
                    raise forms.ValidationError(
                        "This value should be greater than true price.")
        return fake_inr_price

    def clean_fake_aed_price(self):
        aed_price = self.cleaned_data.get('aed_price', '')
        fake_aed_price = self.cleaned_data.get('fake_aed_price', '')
        if fake_aed_price:
            if fake_aed_price < Decimal(0):
                raise forms.ValidationError(
                    "This value cannot be negative.")
            elif fake_aed_price > Decimal(0):
                if fake_aed_price <= aed_price:
                    raise forms.ValidationError(
                        "This value should be greater than true price.")
        return fake_aed_price

    def clean_fake_gbp_price(self):
        gbp_price = self.cleaned_data.get('gbp_price', '')
        fake_gbp_price = self.cleaned_data.get('fake_gbp_price', '')
        if fake_gbp_price:
            if fake_gbp_price < Decimal(0):
                raise forms.ValidationError(
                    "This value cannot be negative.")
            elif fake_gbp_price > Decimal(0):
                if fake_gbp_price <= gbp_price:
                    raise forms.ValidationError(
                        "This value should be greater than true price.")
        return fake_gbp_price

    def save(self, commit=True, *args, **kwargs):
        productscreen = super(ScreenProductPriceForm, self).save(
            commit=True, *args, **kwargs)
        productscreen.status = 1
        productscreen.save()
        return productscreen


class ScreenProductCountryForm(forms.ModelForm):

    countries = forms.ModelMultipleChoiceField(
        queryset=Country.objects.filter(active=True),
        to_field_name='pk',
        widget=forms.SelectMultiple(
            attrs={'class': 'form-control col-md-7 col-xs-12'}))

    def __init__(self, *args, **kwargs):
        super(ScreenProductCountryForm, self).__init__(*args, **kwargs)

    class Meta:
        model = ProductScreen
        fields = (
            'countries',)

    def clean(self):
        super(ScreenProductCountryForm, self).clean()

    def clean_countries(self):
        countries = self.cleaned_data.get('countries', None)
        if countries:
            pass
        else:
            raise forms.ValidationError(
                "This field is required.")
        return countries


class ScreenProductAttributeForm(forms.ModelForm):
    FIELD_FACTORIES = FIELD_FACTORIES

    def __init__(self, *args, **kwargs):
        super(ScreenProductAttributeForm, self).__init__(*args, **kwargs)

    class Meta:
        model = ProductScreen
        fields = ('comment',)

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        if instance is None:
            return
        self.set_initial(instance.product_class, kwargs)
        super(ScreenProductAttributeForm, self).__init__(*args, **kwargs)
        self.add_attribute_fields(instance.product_class)

    def set_initial(self, product_class, kwargs):
        if 'initial' not in kwargs:
            kwargs['initial'] = {}
        self.set_initial_attribute_values(product_class, kwargs)
        
    def set_initial_attribute_values(self, product_class, kwargs):
        instance = kwargs.get('instance')
        if instance is None:
            return
        for attribute in product_class.attributes.filter(active=True):
            try:
                value = instance.screenattributes.get(
                    attribute=attribute).value
            except exceptions.ObjectDoesNotExist:
                pass
            else:
                kwargs['initial']['attribute_%s' % attribute.name] = value

    def add_attribute_fields(self, product_class):
        
        for attribute in product_class.attributes.filter(active=True):
            field = self.get_attribute_field(attribute)
            if field:
                self.fields['attribute_%s' % attribute.name] = field
                
    def get_attribute_field(self, attribute):
        
        return self.FIELD_FACTORIES[attribute.type_attribute](attribute)

    def save(self, commit=True, *args, **kwargs):
        self.instance.attr.initiate_attributes()
        for attribute in self.instance.attr.get_all_attributes():
            field_name = 'attribute_%s' % attribute.name
            if field_name in self.cleaned_data:
                value = self.cleaned_data[field_name]
                setattr(self.instance.attr, attribute.name, value)
        productscreen = super(ScreenProductAttributeForm, self).save(commit=True, *args, **kwargs)
        return productscreen

class ScreenProductFAQForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        obj = kwargs.pop('object', None)
        vendor = kwargs.pop('vendor', None)
        super(ScreenProductFAQForm, self).__init__(*args, **kwargs)
        queryset = FAQuestion.objects.filter(status=2)
        if not vendor:
            queryset = queryset.none()
        else:
            queryset = vendor.question_vendor.filter(status=2) | \
                vendor.public_question.filter(status=2) 
        queryset = queryset.distinct()
        if self.instance.pk:
            self.fields['question'].queryset = queryset
        else:
            faqs = obj.faqs.all().values_list('pk', flat=True) 
            queryset = queryset.exclude(pk__in=faqs)
            self.fields['question'].queryset = queryset
        
        self.fields['question'].queryset = queryset
        form_class = 'form-control col-md-7 col-xs-12'
        self.fields['question'].widget.attrs['class'] = form_class
        self.fields['question'].required = True        
        self.fields['question_order'].widget.attrs['class'] = form_class
        self.fields['active'].widget.attrs['class'] = 'js-switch'
        self.fields['active'].widget.attrs['data-switchery'] = 'true'
        
    class Meta:
        model = FAQProductScreen
        fields = (
            'question', 'question_order', 'active',)

    def clean(self):
        super(ScreenProductFAQForm, self).clean()


    def clean_question(self):
        question = self.cleaned_data.get('question', None)
        if question:
            pass
        else:
            raise forms.ValidationError(
                "This field is required.")
        return question

class ScreenFAQInlineFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super(ScreenFAQInlineFormSet, self).clean()
        if any(self.errors):
            return
        questions = []
        duplicates = False
        for form in self.forms:
            if form.cleaned_data:
                question = form.cleaned_data['question']
                product = form.cleaned_data['product']
                if question in questions:
                    duplicates = True
                questions.append(question)

                if duplicates:
                    raise forms.ValidationError(
                        'FAQs must be unique.',
                        code='duplicate_parent'
                    )
        return

class AddScreenProductVariantForm(forms.ModelForm):
    FIELD_FACTORIES = FIELD_FACTORIES
    
    class Meta:
        model = ProductScreen
        fields = [
            'name', 'upc',
            'inr_price', 'fake_inr_price',
            'usd_price', 'fake_usd_price', 
            'aed_price', 'fake_aed_price',
            'gbp_price', 'fake_gbp_price',
            ]

    def __init__(self, *args, **kwargs):
        parent = kwargs.pop('parent', None)
        user = kwargs.pop('user', None)
        self.set_initial(parent.product_class, kwargs)
        
        super(AddScreenProductVariantForm, self).__init__(*args, **kwargs)
        if not parent:
            return
        form_class = 'form-control col-md-7 col-xs-12'
        self.currency = parent.countries.values_list('currency__value',flat=True).distinct()
        self.currency = set(self.currency)
        self.parent = parent
        self.add_attribute_fields(parent.product_class)
        
        self.fields['name'].widget.attrs['class'] = form_class
        self.fields['name'].widget.attrs['maxlength'] = 80
        self.fields['name'].widget.attrs['placeholder'] = 'Add Product Name'
        self.fields['name'].widget.attrs['data-parsley-trigger'] = 'change'
        self.fields['name'].widget.attrs['data-parsley-required-message'] = 'This field is required.'
        self.fields['name'].widget.attrs['data-parsley-length'] = "[4, 60]"
        self.fields['name'].widget.attrs['data-parsley-length-message'] = 'Length should be between 4-60 characters.'
        self.fields['upc'].widget.attrs['class'] = form_class
        self.fields['upc'].widget.attrs['maxlength'] = 80
        self.fields['upc'].widget.attrs['placeholder'] = 'Add Universal Product Code'
        self.fields['upc'].widget.attrs['data-parsley-trigger'] = 'change'
        self.fields['upc'].widget.attrs['data-parsley-required-message'] = 'This field is required.'
        self.fields['upc'].widget.attrs['data-parsley-length'] = "[4, 60]"
        self.fields['upc'].widget.attrs['data-parsley-length-message'] = 'Length should be between 4-60 characters.'
        self.fields['inr_price'].widget.attrs['class'] = form_class
        self.fields['inr_price'].required = True
        self.fields['usd_price'].widget.attrs['class'] = form_class
        self.fields['aed_price'].widget.attrs['class'] = form_class
        self.fields['gbp_price'].widget.attrs['class'] = form_class
        self.fields['fake_inr_price'].widget.attrs['class'] = form_class
        self.fields['fake_usd_price'].widget.attrs['class'] = form_class
        self.fields['fake_aed_price'].widget.attrs['class'] = form_class
        self.fields['fake_gbp_price'].widget.attrs['class'] = form_class

    def clean(self):
        
        super(AddScreenProductVariantForm, self).clean()
        if any(self.errors):
            return
        inr_price = self.cleaned_data.get('inr_price', '')
        usd_price = self.cleaned_data.get('usd_price', '')
        aed_price = self.cleaned_data.get('aed_price', '')
        gbp_price = self.cleaned_data.get('gbp_price', '')

        if 0 in self.currency and inr_price < 0:
            raise forms.ValidationError(
                "INR Price is required as product is visible in respective country.")
        if 1 in self.currency and usd_price < 0:
            raise forms.ValidationError(
                "USD Price is required as product is visible in respective country.")
        if 2 in self.currency and aed_price < 0:
            raise forms.ValidationError(
                "AED Price is required as product is visible in respective country.")
        if 3 in self.currency and gbp_price < 0:
            raise forms.ValidationError(
                "GBP Price is required as product is visible in respective country.")

        
    def clean_inr_price(self):
        inr_price = self.cleaned_data.get('inr_price', '')
        inr_price = self.cleaned_data.get('inr_price', '')
        if inr_price:
            if inr_price < Decimal(0):
                raise forms.ValidationError(
                    "This value cannot be negative.")
        return inr_price

    def clean_usd_price(self):
        usd_price = self.cleaned_data.get('usd_price', '')
        if usd_price:
            if usd_price < Decimal(0):
                raise forms.ValidationError(
                    "This value cannot be negative.")
        return usd_price

    def clean_aed_price(self):
        aed_price = self.cleaned_data.get('aed_price', '')
        if aed_price:
            if aed_price < Decimal(0):
                raise forms.ValidationError(
                    "This value cannot be negative.")
        return aed_price

    def clean_gbp_price(self):
        gbp_price = self.cleaned_data.get('gbp_price', '')
        if gbp_price:
            if gbp_price < Decimal(0):
                raise forms.ValidationError(
                    "This value cannot be negative.")
        return gbp_price

    def clean_fake_usd_price(self):
        usd_price = self.cleaned_data.get('usd_price', '')
        fake_usd_price = self.cleaned_data.get('fake_usd_price', '')
        if fake_usd_price:
            if fake_usd_price < Decimal(0):
                raise forms.ValidationError(
                    "This value cannot be negative.")
            elif fake_usd_price > Decimal(0):
                if fake_usd_price <= usd_price:
                    raise forms.ValidationError(
                        "This value should be greater than true price.")
        return fake_usd_price

    def clean_fake_inr_price(self):
        inr_price = self.cleaned_data.get('inr_price', '')
        fake_inr_price = self.cleaned_data.get('fake_inr_price', '')
        if fake_inr_price:
            if fake_inr_price < Decimal(0):
                raise forms.ValidationError(
                    "This value cannot be negative.")
            elif fake_inr_price > Decimal(0):
                if fake_inr_price <= inr_price:
                    raise forms.ValidationError(
                        "This value should be greater than true price.")
        return fake_inr_price

    def clean_fake_aed_price(self):
        aed_price = self.cleaned_data.get('aed_price', '')
        fake_aed_price = self.cleaned_data.get('fake_aed_price', '')
        if fake_aed_price:
            if fake_aed_price < Decimal(0):
                raise forms.ValidationError(
                    "This value cannot be negative.")
            elif fake_aed_price > Decimal(0):
                if fake_aed_price <= aed_price:
                    raise forms.ValidationError(
                        "This value should be greater than true price.")
        return fake_aed_price

    def clean_fake_gbp_price(self):
        gbp_price = self.cleaned_data.get('gbp_price', '')
        fake_gbp_price = self.cleaned_data.get('fake_gbp_price', '')
        if fake_gbp_price:
            if fake_gbp_price < Decimal(0):
                raise forms.ValidationError(
                    "This value cannot be negative.")
            elif fake_gbp_price > Decimal(0):
                if fake_gbp_price <= gbp_price:
                    raise forms.ValidationError(
                        "This value should be greater than true price.")
        return fake_gbp_price

    def clean_name(self):
        name = self.cleaned_data.get('name', '')
        if name:
            if len(name) < 4 or len(name) > 60:
                raise forms.ValidationError(
                    "Name should be between 4-60 characters.")
        else:
            raise forms.ValidationError(
                "This field is required.")
        return name

    def clean_inr_price(self):
        inr_price = self.cleaned_data.get('inr_price', '')
        if inr_price:
            if inr_price < Decimal(0):
                raise forms.ValidationError(
                    "This value cannot be negative.")
        else:
            raise forms.ValidationError(
                "This field is required.")
        return inr_price
    
    def save(self, commit=True, *args, **kwargs):
        parent = self.parent
        self.instance.product_class = parent.product_class
        self.instance.attr = ProductAttributesContainer(product=self.instance)
        self.instance.attr.initiate_attributes()
        for attribute in self.instance.attr.get_all_attributes():
            field_name = 'attribute_%s' % attribute.name
            if field_name in self.cleaned_data:
                value = self.cleaned_data[field_name]
                setattr(self.instance.attr, attribute.name, value)
        productscreen = super(AddScreenProductVariantForm, self).save(
            commit=True, *args, **kwargs)
        return productscreen    

    def add_attribute_fields(self, product_class):
        for attribute in product_class.attributes.filter(active=True):
            field = self.get_attribute_field(attribute)
            if field:
                self.fields['attribute_%s' % attribute.name] = field
                
    def get_attribute_field(self, attribute):
        return self.FIELD_FACTORIES[attribute.type_attribute](attribute)

    def set_initial(self, product_class, kwargs):
        if 'initial' not in kwargs:
            kwargs['initial'] = {}
        self.set_initial_attribute_values(product_class, kwargs)
        
    def set_initial_attribute_values(self, product_class, kwargs):
        instance = kwargs.get('instance')
        if instance is None:
            return
        for attribute in product_class.attributes.filter(active=True):
            try:
                value = instance.screenattributes.get(
                    attribute=attribute).value
            except exceptions.ObjectDoesNotExist:
                pass
            else:
                kwargs['initial']['attribute_%s' % attribute.name] = value


class ScreenProductVariationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        obj = kwargs.pop('object', None)
        super(ScreenProductVariationForm, self).__init__(*args, **kwargs)
        form_class = 'form-control col-md-7 col-xs-12'
        self.fields['sort_order'].widget.attrs['class'] = form_class
        self.fields['active'].widget.attrs['class'] = 'js-switch'
        self.fields['active'].widget.attrs['data-switchery'] = 'true'

    class Meta:
        model = VariationProductScreen
        fields = (
            'sort_order', 'active', )

    def clean(self):
        super(ScreenProductVariationForm, self).clean()


class ScreenVariationInlineFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super(ScreenVariationInlineFormSet, self).clean()
        if any(self.errors):
            return
        return


class ScreenProductChapterForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        obj = kwargs.pop('object', None)
        super(ScreenProductChapterForm, self).__init__(*args, **kwargs)
        form_class = 'form-control col-md-7 col-xs-12'
        self.fields['heading'].widget.attrs['class'] = form_class
        self.fields['heading'].widget.attrs['maxlength'] = 200
        self.fields['heading'].widget.attrs['placeholder'] = 'Add heading'
        self.fields['heading'].widget.attrs['data-parsley-trigger'] = 'change'
        self.fields['heading'].widget.attrs['data-parsley-required-message'] = 'This field is required.'
        self.fields['heading'].widget.attrs['data-parsley-length'] = "[4, 200]"
        
        self.fields['answer'].widget.attrs['data-parsley-length-message'] = 'Length should be between 4-200 characters.'
        self.fields['answer'].widget.attrs['required'] = 'required'
        self.fields['answer'].widget.attrs['data-parsley-required-message'] = 'This field is required.'
        
        self.fields['ordering'].widget.attrs['class'] = form_class
        self.fields['status'].widget.attrs['class'] = 'js-switch'
        self.fields['status'].widget.attrs['data-switchery'] = 'true'
        
    class Meta:
        model = ScreenChapter
        fields = (
            'heading', 'answer', 'ordering', 'status')

    def clean(self):
        super(ScreenProductChapterForm, self).clean()


    def clean_heading(self):
        heading = self.cleaned_data.get('heading', None)
        if heading:
            pass
        else:
            raise forms.ValidationError(
                "This field is required.")
        return heading

class ScreenChapterInlineFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super(ScreenChapterInlineFormSet, self).clean()
        if any(self.errors):
            return
        