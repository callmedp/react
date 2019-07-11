from decimal import Decimal
from django import forms
from django.core import exceptions
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from django.conf import settings
from django.forms.fields import MultipleChoiceField
from dal import autocomplete

from .decorators import has_group
from shop.models import (
    ProductClass,
    ProductScreen,
    FAQProductScreen,
    VariationProductScreen,
    ScreenChapter,
    Skill, ScreenProductSkill,
    UniversityCourseDetailScreen,
    UniversityCoursePaymentScreen)
from faq.models import ScreenFAQ
from partner.models import Vendor
from geolocation.models import Country
from shop.utils import ProductAttributesContainer
from faq.models import ScreenFAQ, FAQuestion
from shop.utils import ProductAttributesContainer
from shop.choices import (
    APPLICATION_PROCESS_CHOICES, APPLICATION_PROCESS,
    BENEFITS_CHOICES, BENEFITS, SUB_FLOWS
)
from shop.choices import (
    BG_CHOICES,
    PRODUCT_VENDOR_CHOICES)
from shop.utils import FIELD_FACTORIES, PRODUCT_TYPE_FLOW_FIELD_ATTRS


class AddScreenFaqForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(AddScreenFaqForm, self).__init__(*args, **kwargs)
        form_class = 'form-control col-md-7 col-xs-12'
        self.fields['text'].widget.attrs['class'] = form_class
        self.fields['text'].widget.attrs['maxlength'] = 200
        self.fields['text'].widget.attrs['placeholder'] = 'Add question'
        self.fields['text'].widget.attrs['data-parsley-trigger'] = 'change'
        self.fields['text'].widget.attrs['data-parsley-required-message'] = 'This field is required.'
        self.fields['text'].widget.attrs['data-parsley-length'] = "[2, 200]"
        
        self.fields['answer'].widget.attrs['data-parsley-length-message'] = 'Length should be between 2-200 characters.'
        self.fields['answer'].widget.attrs['required'] = 'required'

        self.fields['answer'].widget.attrs['data-parsley-required-message'] = 'This field is required.'

        self.fields['vendor'].widget.attrs['class'] = form_class
        self.fields['vendor'].queryset = user.vendor_set.all()
        self.fields['vendor'].initial = user.vendor_set.first()
        self.fields['vendor'].required = True
        
    class Meta:
        model = ScreenFAQ
        fields = ('text', 'answer','vendor')


    def clean_vendor(self):
        vendor = self.cleaned_data.get('vendor','')
        if not vendor:
            raise forms.ValidationError("Select the Vendor")
        return vendor

        
    def clean_text(self):
        text = self.cleaned_data.get('text', '')
        if text:
            if len(text) < 2 or len(text) > 200:
                raise forms.ValidationError(
                    "Name should be between 2-200 characters.")
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
        self.fields['text'].widget.attrs['data-parsley-length'] = "[2, 200]"
        self.fields['answer'].widget.attrs['data-parsley-length-message'] = 'Length should be between 2-200 characters.'
        self.fields['answer'].widget.attrs['required'] = 'required'
        self.fields['answer'].widget.attrs['data-parsley-required-message'] = 'This field is required.'

        
    class Meta:
        model = ScreenFAQ
        fields = ('text', 'answer', 'sort_order')

    def clean_text(self):
        text = self.cleaned_data.get('text', '')
        if text:
            if len(text) < 2 or len(text) > 200:
                raise forms.ValidationError(
                    "Name should be between 2-200 characters.")
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
            'type_product', 'upc', 'inr_price', 'type_flow','vendor', 'sub_type_flow']

    def __init__(self, *args, **kwargs):

        self.user = kwargs.pop('user', None)
        super(AddScreenProductForm, self).__init__(*args, **kwargs)
        form_class = 'form-control col-md-7 col-xs-12'
        associated_vendor = self.user.vendor_set.all()
        vendor = self.user.get_vendor()
        self.fields['product_class'].widget.attrs['class'] = form_class
        self.fields['product_class'].empty_label = 'Select Product Class'
        self.fields['product_class'].required = True
        self.fields['type_product'].widget.attrs['class'] = form_class
        self.fields['type_flow'].widget.attrs['class'] = form_class
        self.fields['sub_type_flow'].widget.attrs['class'] = form_class
        if has_group(user=self.user, grp_list=settings.PRODUCT_GROUP_LIST):
            self.fields['type_product'].choices = PRODUCT_VENDOR_CHOICES + ((3, 'Combo'),
                (4, 'No-Direct-Sell/Virtual'),
                (5, 'Downloadable'),)
            self.fields['type_flow'].widget.attrs['class'] = form_class

        else:
            self.fields['type_product'].choices = PRODUCT_VENDOR_CHOICES
            self.fields['type_flow'].choices = (
                (0, 'Default'), (14, 'University Courses')
            )

        if not vendor:
            if has_group(user=self.user, grp_list=settings.PRODUCT_GROUP_LIST):
                pass
            else:
                self.fields['product_class'].queryset = ProductClass.objects.none()
        else:
            self.fields['product_class'].queryset = vendor.prd_add_class.all()
                       
        self.fields['inr_price'].widget.attrs['class'] = form_class
        self.fields['inr_price'].required = True
        
        self.fields['name'].widget.attrs['class'] = form_class
        self.fields['name'].widget.attrs['maxlength'] = 100
        self.fields['name'].widget.attrs['placeholder'] = 'Add Product Name'
        self.fields['name'].widget.attrs['data-parsley-trigger'] = 'change'
        self.fields['name'].widget.attrs['data-parsley-required-message'] = 'This field is required.'
        self.fields['name'].widget.attrs['data-parsley-length'] = "[2, 100]"
        self.fields['name'].widget.attrs['data-parsley-length-message'] = 'Length should be between 2-100 characters.'

        self.fields['upc'].widget.attrs['class'] = form_class
        self.fields['upc'].widget.attrs['maxlength'] = 100
        self.fields['upc'].widget.attrs['placeholder'] = 'Add Universal Product Code'
        self.fields['upc'].widget.attrs['data-parsley-trigger'] = 'change'
        self.fields['upc'].widget.attrs['data-parsley-required-message'] = 'This field is required.'
        self.fields['upc'].widget.attrs['data-parsley-length'] = "[2, 100]"
        self.fields['upc'].widget.attrs['data-parsley-length-message'] = 'Length should be between 2-100 characters.'

        self.fields['vendor'].widget.attrs['class'] = form_class
        self.fields['vendor'].required = True

        if len(associated_vendor) > 1:
            self.fields['vendor'].queryset = associated_vendor
        elif len(associated_vendor) == 1:
            self.fields['vendor'].widget.attrs['class'] ='vendor_hidden'
        self.fields['vendor'].initial = vendor
        if self.data and int(self.data['type_flow']) not in list(SUB_FLOWS.keys()):
            self.fields.pop('sub_type_flow')


    def clean_vendor(self):
        vendor = self.cleaned_data.get('vendor','')

        if not vendor:
            raise forms.ValidationError("Please Select the Vendor")

        return vendor


    def clean_name(self):
        name = self.cleaned_data.get('name', '')
        if name:
            if len(name) < 2 or len(name) > 100:
                raise forms.ValidationError(
                    "Name should be between 2-100 characters.")
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
            if len(upc) < 2 or len(upc) > 100:
                raise forms.ValidationError(
                    "Name should be between 2-100 characters.")
        else:
            raise forms.ValidationError(
                "This field is required.")
        return upc

    def clean_inr_price(self):
        inr_price = self.cleaned_data.get('inr_price', '')
        if inr_price is None:
            raise forms.ValidationError(
                "This field is required.")
        elif inr_price < Decimal(0):
            raise forms.ValidationError(
                "This value cannot be negative.")
        return inr_price

    def clean_sub_type_flow(self):
        sub_type_flow = self.cleaned_data.get('sub_type_flow', '')
        flow = self.cleaned_data.get('type_flow', '')
        if flow in list(SUB_FLOWS.keys()):
            if not sub_type_flow:
                raise forms.ValidationError(
                    "This field is required.")
            elif int(sub_type_flow) not in [st_flow[0] for st_flow in SUB_FLOWS[flow]]:
                    raise forms.ValidationError("Invalid Type flow")
        else:
            sub_type_flow = None
        return sub_type_flow

    def save(self, commit=True, *args, **kwargs):
        productscreen = super(AddScreenProductForm, self).save(
            commit=True, *args, **kwargs)
        if productscreen.type_flow == 14:
            UniversityCourseDetailScreen.objects.create(productscreen=productscreen)
        return productscreen


class ChangeScreenProductForm(forms.ModelForm):

    class Meta:
        model = ProductScreen
        fields = [
            'name', 
            'upc', 
            'about', 'description',
            'buy_shine']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ChangeScreenProductForm, self).__init__(*args, **kwargs)
        form_class = 'form-control col-md-7 col-xs-12'
                       
        self.fields['name'].widget.attrs['class'] = form_class
        self.fields['name'].widget.attrs['maxlength'] = 100
        self.fields['name'].widget.attrs['placeholder'] = 'Add Product Name'
        self.fields['name'].widget.attrs['data-parsley-trigger'] = 'change'
        self.fields['name'].widget.attrs['data-parsley-required-message'] = 'This field is required.'
        self.fields['name'].widget.attrs['data-parsley-length'] = "[2, 100]"
        self.fields['name'].widget.attrs['data-parsley-length-message'] = 'Length should be between 2-100 characters.'
        
        self.fields['upc'].widget.attrs['class'] = form_class
        self.fields['upc'].widget.attrs['maxlength'] = 100
        self.fields['upc'].widget.attrs['placeholder'] = 'Add Universal Product Code'
        self.fields['upc'].widget.attrs['data-parsley-trigger'] = 'change'
        self.fields['upc'].widget.attrs['data-parsley-required-message'] = 'This field is required.'
        self.fields['upc'].widget.attrs['data-parsley-length'] = "[2, 100]"
        self.fields['upc'].widget.attrs['data-parsley-length-message'] = 'Length should be between 2-100 characters.'
        if self.instance.type_flow == 14:
            for val in ['about', 'buy_shine']:
                self.fields.pop(val)

    def clean_name(self):
        name = self.cleaned_data.get('name', '')
        if name:
            if len(name) < 2 or len(name) > 100:
                raise forms.ValidationError(
                    "Name should be between 2-100 characters.")
        else:
            raise forms.ValidationError(
                "This field is required.")
        return name

    
    def clean_upc(self):
        upc = self.cleaned_data.get('upc', '')
        if upc:
            if len(upc) < 2 or len(upc) > 100:
                raise forms.ValidationError(
                    "Name should be between 2-100 characters.")
        else:
            raise forms.ValidationError(
                "This field is required.")
        return upc

    
    def clean_description(self):
        desc = self.cleaned_data.get('description', '')
        if desc or self.instance.type_flow == 16:
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

    # def clean_prg_structure(self):
    #     about = self.cleaned_data.get('prg_structure', '')
    #     if about:
    #         pass
    #     else:
    #         raise forms.ValidationError(
    #             "This field is required.")
    #     return about

    def clean_buy_shine(self):
        buy_shine = self.cleaned_data.get('buy_shine', '')
        if buy_shine or self.instance.type_flow == 16:
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
        if inr_price is None:
            raise forms.ValidationError(
                "This value is requred.")
        elif inr_price < Decimal(0):    
            raise forms.ValidationError(
                "This value cannot be negative.")
        return inr_price
    
    def clean_usd_price(self):
        usd_price = self.cleaned_data.get('usd_price', '')
        if usd_price is None:
            raise forms.ValidationError(
                "This value is requred.")
        elif usd_price < Decimal(0):
            raise forms.ValidationError(
                "This value cannot be negative.")
        return usd_price

    def clean_aed_price(self):
        aed_price = self.cleaned_data.get('aed_price', '')
        if aed_price is None:
            raise forms.ValidationError(
                "This value is requred.")
        elif aed_price < Decimal(0):
            raise forms.ValidationError(
                "This value cannot be negative.")
        return aed_price

    def clean_gbp_price(self):
        gbp_price = self.cleaned_data.get('gbp_price', '')
        if gbp_price is None:
            raise forms.ValidationError(
                "This value is requred.")
        elif gbp_price < Decimal(0):
            raise forms.ValidationError(
                "This value cannot be negative.")
        return gbp_price

    def clean_fake_usd_price(self):
        usd_price = self.cleaned_data.get('usd_price', '')
        fake_usd_price = self.cleaned_data.get('fake_usd_price', '')
        if fake_usd_price is None:
            raise forms.ValidationError(
                "This value is requred.")
        elif fake_usd_price < Decimal(0):
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
        if fake_inr_price is None:
            raise forms.ValidationError(
                "This value is requred.")
        elif fake_inr_price < Decimal(0):
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
        if fake_aed_price is None:
            raise forms.ValidationError(
                "This value is requred.")
        elif fake_aed_price < Decimal(0):
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
    PRODUCT_TYPE_FLOW_FIELD_ATTRS = PRODUCT_TYPE_FLOW_FIELD_ATTRS

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
            if self.instance.type_flow != 14 and attribute.name == 'Brochure':
                continue
            field = self.get_attribute_field(attribute)
            if self.instance.type_flow == 14 and attribute.name in ['course_type', 'study_mode', 'course_level']:
                field.required = False
            if field:
                self.fields['attribute_%s' % attribute.name] = field
                
    def get_attribute_field(self, attribute):

        type_flow_present_in_mapping = self.instance.type_flow \
            if self.instance.type_flow in PRODUCT_TYPE_FLOW_FIELD_ATTRS.get(attribute.type_attribute, {}).keys()\
            else -1
        attrs = self.PRODUCT_TYPE_FLOW_FIELD_ATTRS.get(attribute.type_attribute, {}).get(type_flow_present_in_mapping, {})
        return self.FIELD_FACTORIES[attribute.type_attribute](attribute, attrs)

    def save(self, commit=True, *args, **kwargs):
        self.instance.attr.initiate_attributes()
        for attribute in self.instance.attr.get_all_attributes():
            field_name = 'attribute_%s' % attribute.name
            if field_name in self.cleaned_data:
                value = self.cleaned_data[field_name]
                setattr(self.instance.attr, attribute.name, value)
        productscreen = super(ScreenProductAttributeForm, self).save(commit=False, *args, **kwargs)
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
    PRODUCT_TYPE_FLOW_FIELD_ATTRS = PRODUCT_TYPE_FLOW_FIELD_ATTRS
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
        self.fields['name'].widget.attrs['maxlength'] = 100
        self.fields['name'].widget.attrs['placeholder'] = 'Add Product Name'
        self.fields['name'].widget.attrs['data-parsley-trigger'] = 'change'
        self.fields['name'].widget.attrs['data-parsley-required-message'] = 'This field is required.'
        self.fields['name'].widget.attrs['data-parsley-length'] = "[2, 100]"
        self.fields['name'].widget.attrs['data-parsley-length-message'] = 'Length should be between 2-100 characters.'
        self.fields['upc'].widget.attrs['class'] = form_class
        self.fields['upc'].widget.attrs['maxlength'] = 100
        self.fields['upc'].widget.attrs['placeholder'] = 'Add Universal Product Code'
        self.fields['upc'].widget.attrs['data-parsley-trigger'] = 'change'
        self.fields['upc'].widget.attrs['data-parsley-required-message'] = 'This field is required.'
        self.fields['upc'].widget.attrs['data-parsley-length'] = "[2, 100]"
        self.fields['upc'].widget.attrs['data-parsley-length-message'] = 'Length should be between 2-100 characters.'
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
        if inr_price is None:
            raise forms.ValidationError(
                "This value is requred.")
        elif inr_price < Decimal(0):    
            raise forms.ValidationError(
                "This value cannot be negative.")
        return inr_price
    
    def clean_usd_price(self):
        usd_price = self.cleaned_data.get('usd_price', '')
        if usd_price is None:
            raise forms.ValidationError(
                "This value is requred.")
        elif usd_price < Decimal(0):
            raise forms.ValidationError(
                "This value cannot be negative.")
        return usd_price

    def clean_aed_price(self):
        aed_price = self.cleaned_data.get('aed_price', '')
        if aed_price is None:
            raise forms.ValidationError(
                "This value is requred.")
        elif aed_price < Decimal(0):
            raise forms.ValidationError(
                "This value cannot be negative.")
        return aed_price

    def clean_gbp_price(self):
        gbp_price = self.cleaned_data.get('gbp_price', '')
        if gbp_price is None:
            raise forms.ValidationError(
                "This value is requred.")
        elif gbp_price < Decimal(0):
            raise forms.ValidationError(
                "This value cannot be negative.")
        return gbp_price

    def clean_fake_usd_price(self):
        usd_price = self.cleaned_data.get('usd_price', '')
        fake_usd_price = self.cleaned_data.get('fake_usd_price', '')
        if fake_usd_price is None:
            raise forms.ValidationError(
                "This value is requred.")
        elif fake_usd_price < Decimal(0):
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
        if fake_inr_price is None:
            raise forms.ValidationError(
                "This value is requred.")
        elif fake_inr_price < Decimal(0):
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
        if fake_aed_price is None:
            raise forms.ValidationError(
                "This value is requred.")
        elif fake_aed_price < Decimal(0):
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
            if len(name) < 2 or len(name) > 100:
                raise forms.ValidationError(
                    "Name should be between 2-100 characters.")
        else:
            raise forms.ValidationError(
                "This field is required.")
        return name

    
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
            if self.instance.type_flow != 14 and attribute.name == 'Brochure':
                continue
            field = self.get_attribute_field(attribute)
            if field:
                self.fields['attribute_%s' % attribute.name] = field
                
    def get_attribute_field(self, attribute):
        type_flow_present_in_mapping = self.instance.type_flow \
            if self.instance.type_flow in PRODUCT_TYPE_FLOW_FIELD_ATTRS.get(attribute.type_attribute, {}).keys()\
            else -1
        attrs = self.PRODUCT_TYPE_FLOW_FIELD_ATTRS.get(attribute.type_attribute, {}).get(type_flow_present_in_mapping, {})
        return self.FIELD_FACTORIES[attribute.type_attribute](attribute, attrs)

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
        self.fields['heading'].widget.attrs['data-parsley-length'] = "[2, 200]"
        
        self.fields['answer'].widget.attrs['data-parsley-length-message'] = 'Length should be between 2-200 characters.'
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


class ScreenProductSkillForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        obj = kwargs.pop('object', None)
        super(ScreenProductSkillForm, self).__init__(*args, **kwargs)
        form_class = 'form-control col-md-7 col-xs-12'
        queryset = Skill.objects.filter(active=True)
        # if self.instance.pk:
        #     self.fields['skill'].queryset = queryset
        # else:
        #     skills = obj.screenskills.all().values_list(
        #         'skill_id', flat=True)
        #     queryset = queryset.exclude(pk__in=skills)
        self.fields['skill'].queryset = queryset
        self.fields['skill'].widget.attrs['class'] = form_class
        self.fields['skill'].required = True

        self.fields['active'].widget.attrs['class'] = 'js-switch'
        self.fields['active'].widget.attrs['data-switchery'] = 'true'
        self.fields['priority'].widget.attrs['class'] = form_class

    class Meta:
        model = ScreenProductSkill
        fields = (
            'skill', 'active', 'priority')
        widgets = {
            'skill': autocomplete.ModelSelect2(
                url='console:skill-autocomplete')
        }

    def clean(self):
        super(ScreenProductSkillForm, self).clean()

    def clean_skill(self):
        skill = self.cleaned_data.get('skill', None)
        if skill:
            pass
        else:
            raise forms.ValidationError(
                "This field is required.")
        return skill


class ScreenSkillInlineFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super(ScreenSkillInlineFormSet, self).clean()
        # if any(self.errors):
        #     return
        skills = []
        duplicates = False
        for form in self.forms:
            if form.cleaned_data:
                skill = form.cleaned_data['skill']
                if skill in skills:
                    duplicates = True
                skills.append(skill)

                if duplicates:
                    raise forms.ValidationError(
                        'Skill must be unique.',
                        code='duplicate_skill'
                    )
        return


class ScreenUniversityCoursesPaymentInlineFormset(forms.BaseInlineFormSet):
    def clean(self):
        super(UniversityCoursesPaymentInlineFormset, self).clean()
        if any(self.errors):
            return


class ScreenUniversityCourseForm(forms.ModelForm):

    batch_launch_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'class': 'form-control batch_launch_date',
                "readonly": True,
            }, format='%d-%m-%Y'
        ),
        input_formats=['%d-%m-%Y']

    )
    apply_last_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'class': 'form-control apply_last_date',
                "readonly": True,
            }, format='%d-%m-%Y'
        ),
        input_formats=['%d-%m-%Y']
    )
    payment_deadline = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'class': 'form-control payment_deadline',
                "readonly": True,
            }, format='%d-%m-%Y'
        ),
        input_formats=['%d-%m-%Y']
    )
    application_process_choices = MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=APPLICATION_PROCESS_CHOICES
    )
    selected_process_choices = MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=[]
    )
    benefits_choices = MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=BENEFITS_CHOICES
    )
    selected_benefits_choices = MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=[]
    )
    eligibility_criteria = forms.CharField(
        label=("Eligibility Criteria"),
        help_text='semi-colon(;) separated criteria, e.g. Line Managers; Decision Maker; ...', 
        max_length=500,
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control col-md-7 col-xs-12'})
    )
    benefits = forms.CharField(
        required=False
    )
    attendees_criteria_choices = MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=[]
    )

    class Meta:
        model = UniversityCourseDetailScreen
        fields = [
            'batch_launch_date', 'apply_last_date',
            'sample_certificate', 'application_process', 'assesment',
            'benefits', 'eligibility_criteria', 'attendees_criteria',
            'payment_deadline', 'highlighted_benefits'
        ]

    def __init__(self, *args, **kwargs):
        super(ScreenUniversityCourseForm, self).__init__(*args, **kwargs)
        form_class = 'form-control col-md-7 col-xs-12'
        self.fields['batch_launch_date'].widget.attrs['required'] = True
        self.fields['apply_last_date'].widget.attrs['required'] = True
        self.fields['sample_certificate'].widget.attrs['required'] = True
        self.fields['assesment'].widget.attrs['required'] = True
        self.fields['assesment'].widget.attrs['class'] = form_class
        self.fields['sample_certificate'].widget.attrs['class'] = form_class
        self.fields['eligibility_criteria'].widget.attrs['class'] = form_class + ' tagsinput tags form-control'
        self.fields['highlighted_benefits'].widget.attrs['required'] = True
        self.fields['highlighted_benefits'].widget.attrs['class'] = form_class +  ' tagsinput tags form-control'

        if self.instance.get_application_process:
            self.fields['application_process_choices'].initial = [
                int(k) for k in self.instance.get_application_process
            ]
            self.fields['selected_process_choices'].choices = [
                (int(k), APPLICATION_PROCESS.get(k)[1], APPLICATION_PROCESS.get(k)[0]) for k in self.instance.get_application_process
            ]
        attendees_criteria = self.instance.get_attendees_criteria
        if attendees_criteria and len(attendees_criteria) < 4:
            extra_form = 4 - len(attendees_criteria)
            attendees_criteria.extend([('', '')] * extra_form)
        elif attendees_criteria and len(attendees_criteria) >= 4:
            attendees_criteria.extend([('', '')])
        else:
            attendees_criteria = [('', '')] * 4
        self.fields['attendees_criteria_choices'].choices = attendees_criteria

        self.fields['application_process_choices'].widget.attrs['class'] = form_class
        self.fields['application_process_choices'].widget.attrs['required'] = True
        self.fields['application_process_choices'].widget.attrs['class'] = form_class + ' process_item'

        if self.instance.benefits:
            self.fields['benefits_choices'].initial = [
                int(k) for k in self.instance.get_benefits
            ]
            self.fields['selected_benefits_choices'].choices = [
                (int(k), BENEFITS.get(k)[1], BENEFITS.get(k)[0]) for k in self.instance.get_benefits
            ]

        self.fields['benefits_choices'].widget.attrs['class'] = form_class
        self.fields['benefits_choices'].widget.attrs['class'] = form_class + ' benefit_item'

    def clean_batch_launch_date(self):
        batch_launch_date = self.cleaned_data.get('batch_launch_date', '')
        if batch_launch_date is None:
            raise forms.ValidationError(
                "This value is requred.")
        return batch_launch_date

    def clean_apply_last_date(self):
        apply_last_date = self.cleaned_data.get('apply_last_date', '')
        if apply_last_date is None:
            raise forms.ValidationError(
                "This value is requred.")
        return apply_last_date

    def clean_sample_certificate(self):
        file = self.cleaned_data.get('sample_certificate')
        if file:
            filename = file.name
            if not (filename.endswith('.mp3') or filename.endswith('.jpg') or
                    filename.endswith('.jpeg') or filename.endswith('.pdf') or
                    filename.endswith('.png')):
                raise forms.ValidationError("File is not supported. Please upload jpg, png or pdf file only,")

        return file

    def clean_attendees_criteria(self):
        attendees_criteria = self.cleaned_data.get('attendees_criteria', '')
        if not eval(attendees_criteria):
            raise forms.ValidationError(
                "Provide atleast one 'Who should attend?'.")
        return attendees_criteria

    def clean_highlighted_benefits(self):
        highlighted_benefits = self.cleaned_data.get('highlighted_benefits', '')
        if not highlighted_benefits:
            raise forms.ValidationError(
                "Provide Highlighted benefits.")
        return highlighted_benefits


class ScreenUniversityCoursePaymentForm(forms.ModelForm):

    last_date_of_payment = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'class': 'form-control col-md-7 col-xs-12 last_date_of_payment',
                "readonly": True,
            }, format='%d-%m-%Y'
        ),
        input_formats=['%d-%m-%Y']
    )

    def __init__(self, *args, **kwargs):
        super(ScreenUniversityCoursePaymentForm, self).__init__(*args, **kwargs)
        form_class = 'form-control col-md-7 col-xs-12'

        self.fields['installment_fee'].widget.attrs['class'] = form_class
        self.fields['installment_fee'].widget.attrs['data-parsley-required-message'] = 'This field is required.'
        self.fields['installment_fee'].widget.attrs['required'] = True
        self.fields['installment_fee'].widget.attrs['data-parsley-trigger'] = 'change'
        self.fields['last_date_of_payment'].widget.attrs['data-parsley-required-message'] = 'This field is required.'
        self.fields['last_date_of_payment'].widget.attrs['required'] = True

        self.fields['active'].widget.attrs['class'] = 'js-switch'
        self.fields['active'].widget.attrs['data-switchery'] = 'true'

    class Meta:
        model = UniversityCoursePaymentScreen
        fields = (
            'installment_fee',
            'last_date_of_payment',
            'active'
        )

    def clean(self):
        super(ScreenUniversityCoursePaymentForm, self).clean()

    def clean_installment_fee(self):
        from django.db.models import Sum
        installment_fee = self.cleaned_data.get('installment_fee', '')
        sum_already_present = 0
        if getattr(self.instance.productscreen, 'screen_university_course_payment', None):
            sum_already_present = self.instance.productscreen.screen_university_course_payment.all().aggregate(Sum('installment_fee'))['installment_fee__sum']
        sum_already_present = sum_already_present if sum_already_present else 0
        if not self.instance.id and (installment_fee + sum_already_present > self.instance.productscreen.inr_price):
            raise forms.ValidationError(
                "Total installment cannot be greater than product price.")
        elif self.instance.id:
            if installment_fee + (sum_already_present - self.instance.installment_fee) > self.instance.productscreen.inr_price:
                raise forms.ValidationError(
                    "Total installment cannot be greater than product price.")

        if installment_fee is None:
            raise forms.ValidationError(
                "This value is requred.")
        return installment_fee

    def clean_last_date_of_payment(self):
        last_date_of_payment = self.cleaned_data.get('last_date_of_payment', '')
        if last_date_of_payment is None:
            raise forms.ValidationError(
                "This value is requred.")
        return last_date_of_payment
