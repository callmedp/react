from decimal import Decimal
from django.core import exceptions
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
from django.utils.html import format_html

from django import forms
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from shop.models import (
    Keyword, AttributeOptionGroup, AttributeOption,
    Attribute, Product, Category, ProductCategory,
    FAQProduct, Chapter, Skill, ProductSkill,
    ChildProduct, VariationProduct, RelatedProduct,
    UniversityCourseDetail)
from partner.models import Vendor
from geolocation.models import Country
from shop.choices import BG_CHOICES, SUB_FLOWS
from shop.utils import FIELD_FACTORIES, PRODUCT_TYPE_FLOW_FIELD_ATTRS
from faq.models import FAQuestion


class AddKeywordForm(forms.ModelForm):

    class Meta:
        model = Keyword
        fields = ['name', 'active']

    def __init__(self, *args, **kwargs):
        super(AddKeywordForm, self).__init__(*args, **kwargs)
        form_class = 'form-control col-md-7 col-xs-12'
        self.fields['name'].widget.attrs['class'] = form_class
        self.fields['name'].widget.attrs['maxlength'] = 100
        self.fields['name'].widget.attrs['placeholder'] = 'Add unique keyword'
        self.fields['name'].widget.attrs['data-parsley-trigger'] = 'change'
        self.fields['name'].widget.attrs['data-parsley-required-message'] = 'This field is required.'
        self.fields['name'].widget.attrs['data-parsley-length'] = "[2, 100]"
        self.fields['name'].widget.attrs['data-parsley-length-message'] = 'Length should be between 2-100 characters.'
        
        self.fields['active'].widget.attrs['class'] = 'js-switch'
        self.fields['active'].widget.attrs['data-switchery'] = 'true'

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
    
    def save(self, commit=True):
        keyword = super(AddKeywordForm, self).save(commit=False)
        if commit:
            keyword.save()
        return keyword


class AddAttributeForm(forms.ModelForm):

    class Meta:
        model = Attribute
        fields = ['name', 'product_class', 'display_name',
            'type_attribute', 'required', 'is_visible',
            'is_sortable', 'is_multiple', 'is_searchable',
            'is_filterable', 'is_indexable', 'active', 'option_group']

    def __init__(self, *args, **kwargs):
        super(AddAttributeForm, self).__init__(*args, **kwargs)
        form_class = 'form-control col-md-7 col-xs-12'
        self.fields['type_attribute'].widget.attrs['class'] = form_class

        self.fields['product_class'].widget.attrs['class'] = form_class
        self.fields['product_class'].required=True
        self.fields['option_group'].widget.attrs['class'] = form_class
        
        self.fields['active'].widget.attrs['class'] = 'js-switch'
        self.fields['active'].widget.attrs['data-switchery'] = 'true'
        self.fields['required'].widget.attrs['class'] = 'js-switch'
        self.fields['required'].widget.attrs['data-switchery'] = 'true'
        
        self.fields['is_sortable'].widget.attrs['class'] = 'js-switch'
        self.fields['is_sortable'].widget.attrs['data-switchery'] = 'true'

        self.fields['is_indexable'].widget.attrs['class'] = 'js-switch'
        self.fields['is_indexable'].widget.attrs['data-switchery'] = 'true'
        self.fields['is_visible'].widget.attrs['class'] = 'js-switch'
        self.fields['is_visible'].widget.attrs['data-switchery'] = 'true'

        self.fields['is_multiple'].widget.attrs['class'] = 'js-switch'
        self.fields['is_multiple'].widget.attrs['data-switchery'] = 'true'

        self.fields['is_searchable'].widget.attrs['class'] = 'js-switch'
        self.fields['is_searchable'].widget.attrs['data-switchery'] = 'true'

        self.fields['is_filterable'].widget.attrs['class'] = 'js-switch'
        self.fields['is_filterable'].widget.attrs['data-switchery'] = 'true'

        self.fields['name'].widget.attrs['class'] = form_class
        self.fields['name'].widget.attrs['maxlength'] = 100
        self.fields['name'].widget.attrs['placeholder'] = 'Add attribute name'
        self.fields['name'].widget.attrs['data-parsley-trigger'] = 'change'
        self.fields['name'].widget.attrs['data-parsley-required-message'] = 'This field is required.'
        self.fields['name'].widget.attrs['data-parsley-length'] = "[2, 100]"
        self.fields['name'].widget.attrs['data-parsley-length-message'] = 'Length should be between 2-100 characters.'

        self.fields['display_name'].widget.attrs['class'] = form_class
        self.fields['display_name'].widget.attrs['maxlength'] = 100
        self.fields['display_name'].widget.attrs['placeholder'] = 'Add display name'
        self.fields['display_name'].widget.attrs['data-parsley-trigger'] = 'change'
        self.fields['display_name'].widget.attrs['data-parsley-required-message'] = 'This field is required.'
        self.fields['display_name'].widget.attrs['data-parsley-length'] = "[2, 100]"
        self.fields['display_name'].widget.attrs['data-parsley-length-message'] = 'Length should be between 2-100 characters.'

    def clean(self):
        super(AddAttributeForm, self).clean()
        if any(self.errors):
            return
        value = self.cleaned_data['type_attribute']
        if value == 'option' or value == 'multi_option' :
            if not self.cleaned_data['option_group']:
                raise forms.ValidationError(
                    'Option Group is required.')
        return

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

    def clean_display_name(self):
        name = self.cleaned_data.get('display_name', '')
        if name:
            if len(name) < 2 or len(name) > 100:
                raise forms.ValidationError(
                    "Name should be between 2-100 characters.")
        else:
            raise forms.ValidationError(
                "This field is required.")
        return name

    def save(self, commit=True):
        attribute = super(AddAttributeForm, self).save(commit=False)
        if commit:
            if attribute.type_attribute == 'option' or attribute.type_attribute == 'multi_option':
                pass
            else:
                attribute.option_group = None
            attribute.save()
        return attribute


class AddAttributeOptionForm(forms.ModelForm):

    class Meta:
        model = AttributeOptionGroup
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super(AddAttributeOptionForm, self).__init__(*args, **kwargs)
        form_class = 'form-control col-md-7 col-xs-12'
        self.fields['name'].widget.attrs['class'] = form_class
        self.fields['name'].widget.attrs['maxlength'] = 100
        self.fields['name'].widget.attrs['placeholder'] = 'Add Option Group Name'
        self.fields['name'].widget.attrs['data-parsley-trigger'] = 'change'
        self.fields['name'].widget.attrs['data-parsley-required-message'] = 'This field is required.'
        self.fields['name'].widget.attrs['data-parsley-length'] = "[2, 100]"
        self.fields['name'].widget.attrs['data-parsley-length-message'] = 'Length should be between 2-100 characters.'
        


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

    def save(self, commit=True):
        opt_group = super(AddAttributeOptionForm, self).save(commit=False)
        if commit:
            opt_group.save()
        return opt_group


class DataColorSelect(forms.widgets.Select):

    def render_option(self, selected_choices, option_value, option_label):
        option_value = force_text(option_value)
        if option_value in selected_choices:
            selected_html = mark_safe(' selected="selected"')
            if not self.allow_multiple_selected:
                selected_choices.remove(option_value)
        else:
            selected_html = ''

        datacolor = option_label
        return format_html('<option value="{0}"{1} data-color="{3}">{2}</option>', option_value, selected_html, force_text(option_label), datacolor)


class DataColorChoiceField(forms.ChoiceField):
    
    def __init__(self, *args, **kwargs):
        kwargs['widget'] = DataColorSelect(attrs={'class': 'form-control col-md-7 col-xs-12 image_bg'})
        super(DataColorChoiceField, self).__init__(*args, **kwargs)


class ChangeProductForm(forms.ModelForm):

    image_bg = DataColorChoiceField(choices=BG_CHOICES)

    class Meta:
        model = Product
        fields = [
            'name', 'type_flow',
            'upc', 'image', 'image_bg', 'icon', 'banner', 'video_url',
            'vendor', 'product_tag',
            'no_review', 'buy_count', 'avg_rating', 'num_jobs', 'sub_type_flow']

    def __init__(self, *args, **kwargs):
        super(ChangeProductForm, self).__init__(*args, **kwargs)
        form_class = 'form-control col-md-7 col-xs-12'
        self.fields['type_flow'].widget.attrs['class'] = form_class
        self.fields['type_flow'].widget.attrs['data-parsley-notdefault'] = ''
        self.fields['sub_type_flow'].widget.attrs['class'] = form_class

        self.fields['vendor'].widget.attrs['class'] = form_class
        self.fields['vendor'].empty_label = 'Select Vendor'
        self.fields['vendor'].required = True
        
        self.fields['name'].widget.attrs['class'] = form_class
        self.fields['name'].widget.attrs['maxlength'] = 100
        self.fields['name'].widget.attrs['placeholder'] = 'Add product name'
        self.fields['name'].widget.attrs['data-parsley-trigger'] = 'change'
        self.fields['name'].widget.attrs['data-parsley-required-message'] = 'This field is required.'
        self.fields['name'].widget.attrs['data-parsley-length'] = "[2, 100]"
        self.fields['name'].widget.attrs['data-parsley-length-message'] = 'Length should be between 2-100 characters.'

        self.fields['upc'].widget.attrs['class'] = form_class
        
        self.fields['upc'].widget.attrs['maxlength'] = 100
        self.fields['upc'].widget.attrs['placeholder'] = 'Add Universal Product Code'
        self.fields['upc'].widget.attrs['data-parsley-trigger'] = 'change'
        self.fields['upc'].widget.attrs['data-parsley-length'] = "[2, 100]"
        self.fields['upc'].widget.attrs['data-parsley-length-message'] = 'Length should be between 2-100 characters.'
        
        self.fields['banner'].widget.attrs['class'] = form_class + ' clearimg'
        self.fields['banner'].widget.attrs['data-parsley-max-file-size'] = 300
        self.fields['banner'].widget.attrs['data-parsley-filemimetypes'] = 'image/jpeg, image/png, image/jpg, image/svg'
        self.fields['image'].widget.attrs['class'] = form_class + ' clearimg'
        self.fields['image'].widget.attrs['data-parsley-max-file-size'] = 300
        self.fields['image'].widget.attrs['data-parsley-filemimetypes'] = 'image/jpeg, image/png, image/jpg, image/svg'


        self.fields['icon'].widget.attrs['class'] = form_class + ' clearimg'
        self.fields['icon'].widget.attrs['data-parsley-max-file-size'] = 100
        self.fields['icon'].widget.attrs['data-parsley-filemimetypes'] = 'image/jpeg, image/png, image/jpg, image/svg'
        self.fields['video_url'].widget.attrs['class'] = form_class
        self.fields['video_url'].widget.attrs['maxlength'] = 100
        self.fields['video_url'].widget.attrs['placeholder'] = 'Add video url'
        self.fields['video_url'].widget.attrs['data-parsley-type'] = 'url'
        self.fields['avg_rating'].widget.attrs['class'] = form_class
        self.fields['no_review'].widget.attrs['class'] = form_class
        self.fields['buy_count'].widget.attrs['class'] = form_class
        self.fields['num_jobs'].widget.attrs['class'] = form_class
        self.fields['product_tag'].widget.attrs['class'] = form_class


        if self.data and int(self.data['type_flow']) not in list(SUB_FLOWS.keys()):
            self.fields.pop('sub_type_flow')

        if not self.data and self.initial['type_flow'] in list(SUB_FLOWS.keys()):
            self.fields['sub_type_flow'].choices = SUB_FLOWS[self.initial['type_flow']]

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

    def clean_type_flow(self):
        flow = self.cleaned_data.get('type_flow', '')
        if flow:
            if int(flow) == 0:
                raise forms.ValidationError(
                    "This should not be default.")
        else:
            raise forms.ValidationError(
                "This field is required.")
        return flow

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

    def clean_image_bg(self):
        image_bg = self.cleaned_data.get('image_bg', '')
        if image_bg:
            pass
        else:
            raise forms.ValidationError(
                "This field is required.")
        return image_bg

    def clean_video_url(self):
        link = self.cleaned_data.get('video_url', '')
        if link:
            from django.core.validators import URLValidator
            val = URLValidator()
            val('https://' + link.strip())
        return link

    def clean_image(self):
        file = self.cleaned_data.get('image')
        if file:
            if file.size > 200 * 1024:
                raise forms.ValidationError(
                    "Image file is too large ( > 200kb ).")
        return file

    def clean_banner(self):
        file = self.cleaned_data.get('banner')
        if file:
            if file.size > 500 * 1024:
                raise forms.ValidationError(
                    "Banner file is too large ( > 500kb ).")
        return file

    def clean_icon(self):
        file = self.cleaned_data.get('icon')
        if file:
            if file.size > 100 * 1024:
                raise forms.ValidationError(
                    "Icon file is too large ( > 100kb ).")
        return file


    def save(self, commit=True, *args, **kwargs):
        product = super(ChangeProductForm, self).save(
            commit=True, *args, **kwargs)
        if product.image:
            if not product.icon:
                product.create_icon()
        if product.type_product == 1:
            variation = product.variation.all()
            for pv in variation:
                if pv.type_flow != product.type_flow:
                    pv.type_flow = product.type_flow
                    pv.save()
        if product.type_flow == 14:
            UniversityCourseDetail.objects.get_or_create(product=product)

        if product.type_product == 1 and product.type_flow in list(SUB_FLOWS.keys()):
            child_variation = product.get_variations()
            child_variation.update(sub_type_flow=product.sub_type_flow)

        return product


class ChangeProductSEOForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ChangeProductSEOForm, self).__init__(*args, **kwargs)
        form_class = 'form-control col-md-7 col-xs-12'
        self.fields['image_alt'].widget.attrs['class'] = form_class
        self.fields['image_alt'].widget.attrs['maxlength'] = 100
        self.fields['image_alt'].widget.attrs['placeholder'] = 'Add Alt'
        self.fields['image_alt'].widget.attrs['data-parsley-trigger'] = 'change'
        self.fields['image_alt'].widget.attrs['data-parsley-required-message'] = 'This field is required.'
        self.fields['image_alt'].widget.attrs['data-parsley-length'] = "[2, 100]"
        self.fields['image_alt'].widget.attrs['data-parsley-length-message'] = 'Length should be between 2-100 characters.'

        self.fields['title'].widget.attrs['class'] = form_class
        self.fields['title'].widget.attrs['maxlength'] = 100
        self.fields['title'].widget.attrs['placeholder'] = 'Add unique title'
        self.fields['title'].widget.attrs['data-parsley-trigger'] = 'change'
        self.fields['title'].widget.attrs['required'] = "required"

        self.fields['title'].widget.attrs['data-parsley-required-message'] = 'This field is required.'
        self.fields['title'].widget.attrs['data-parsley-length'] = "[2, 100]"
        self.fields['title'].widget.attrs['data-parsley-length-message'] = 'Length should be between 2-100 characters.'

        self.fields['heading'].widget.attrs['class'] = form_class
        self.fields['heading'].widget.attrs['maxlength'] = 100
        self.fields['heading'].widget.attrs['required'] = "required"
        self.fields['heading'].widget.attrs['placeholder'] = 'Add H1'
        self.fields['heading'].widget.attrs['data-parsley-trigger'] = 'change'
        self.fields['heading'].widget.attrs['data-parsley-required-message'] = 'This field is required.'
        self.fields['heading'].widget.attrs['data-parsley-length'] = "[2, 100]"
        self.fields['heading'].widget.attrs['data-parsley-length-message'] = 'Length should be between 2-100 characters.'

        self.fields['meta_desc'].widget.attrs['class'] = form_class
        self.fields['meta_keywords'].widget.attrs['class'] = form_class
        if self.instance.type_flow == 14:
            for val in ['about', 'buy_shine', 'attend']:
                self.fields.pop(val)


    class Meta:
        model = Product
        fields = ('title', 'meta_desc', 'meta_keywords', 'heading','image_alt',
            'about', 'description', 'buy_shine', 'visibility', 'attend')

    def clean_title(self):
        title = self.cleaned_data.get('title', '')
        if title:
            if len(title) < 2 or len(title) > 100:
                raise forms.ValidationError(
                    "Name should be between 2-100 characters.")
        else:
            raise forms.ValidationError(
                "This field is required.")
        return title

    def clean_heading(self):
        heading = self.cleaned_data.get('heading', '')
        if heading:
            if len(heading) < 2 or len(heading) > 100:
                raise forms.ValidationError(
                    "Name should be between 2-100 characters.")
        else:
            raise forms.ValidationError(
                "This field is required.")
        return heading

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

    def clean_buy_shine(self):
        buy_shine = self.cleaned_data.get('buy_shine', '')
        if buy_shine or self.instance.type_flow == 16:
            pass
        else:
            raise forms.ValidationError(
                "This field is required.")
        return buy_shine


    def save(self, commit=True, *args, **kwargs):
        product = super(ChangeProductSEOForm, self).save(
            commit=True, *args, **kwargs)
        return product


class ProductPriceForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = [
            'inr_price', 'fake_inr_price',
            'usd_price', 'fake_usd_price', 
            'aed_price', 'fake_aed_price',
            'gbp_price', 'fake_gbp_price',]

    def __init__(self, *args, **kwargs):
        super(ProductPriceForm, self).__init__(*args, **kwargs)
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
        
        super(ProductPriceForm, self).clean()
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
        product = super(ProductPriceForm, self).save(
            commit=True, *args, **kwargs)
        return product


class ProductCountryForm(forms.ModelForm):

    countries = forms.ModelMultipleChoiceField(
        queryset=Country.objects.filter(active=True),
        to_field_name='pk',
        widget=forms.SelectMultiple(
            attrs={'class': 'form-control col-md-7 col-xs-12'}))

    def __init__(self, *args, **kwargs):
        super(ProductCountryForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Product
        fields = (
            'countries',)

    def clean(self):
        super(ProductCountryForm, self).clean()

    def clean_countries(self):
        countries = self.cleaned_data.get('countries', None)
        if countries:
            pass
        else:
            raise forms.ValidationError(
                "This field is required.")
        return countries


class ChangeProductOperationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ChangeProductOperationForm, self).__init__(*args, **kwargs)
        form_class = 'form-control col-md-7 col-xs-12'
        self.fields['call_desc'].widget.attrs['class'] = form_class
    class Meta:
        model = Product
        fields = ('call_desc',)

    
    def save(self, commit=True, *args, **kwargs):
        product = super(ChangeProductOperationForm, self).save(
            commit=True, *args, **kwargs)
        return product


class ProductAttributeForm(forms.ModelForm):
    FIELD_FACTORIES = FIELD_FACTORIES
    PRODUCT_TYPE_FLOW_FIELD_ATTRS = PRODUCT_TYPE_FLOW_FIELD_ATTRS
    def __init__(self, *args, **kwargs):
        super(ScreenProductAttributeForm, self).__init__(*args, **kwargs)
        form_class = 'form-control col-md-7 col-xs-12'
        self.fields['mail_desc'].widget.attrs['class'] = form_class
        
        

    class Meta:
        model = Product
        fields = ('mail_desc',)

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        if instance is None:
            return
        self.set_initial(instance.product_class, kwargs)
        super(ProductAttributeForm, self).__init__(*args, **kwargs)
        self.add_attribute_fields(instance.product_class)

    def set_initial(self, product_class, kwargs):
        if 'initial' not in kwargs:
            kwargs['initial'] = {}
        self.set_initial_attribute_values(product_class, kwargs)

    def set_initial_attribute_values(self, product_class, kwargs):
        instance = kwargs.get('instance')
        if instance is None:
            return
        prdt_class_attr = list(product_class.attributes.filter(active=True).values_list('id',flat=True))
        for attr in instance.productattributes.filter(attribute__in=prdt_class_attr).select_related('attribute').select_related('value_option'):
            kwargs['initial']['attribute_%s' % attr.attribute.name] = attr.value
        # for attribute in product_class.attributes.filter(active=True):
        #     try:
        #         value = instance.productattributes.get(
        #             attribute=attribute).value
        #     except exceptions.ObjectDoesNotExist:
        #         pass
        #     else:
        #         kwargs['initial']['attribute_%s' % attribute.name] = value

    def add_attribute_fields(self, product_class):
        for attribute in product_class.attributes.filter(active=True).select_related('option_group'):
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
        product = super(ProductAttributeForm, self).save(commit=True, *args, **kwargs)
        return product



class ProductCategoryForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        obj = kwargs.pop('object', None)
        super(ProductCategoryForm, self).__init__(*args, **kwargs)
        form_class = 'form-control col-md-7 col-xs-12'
        if self.instance.pk:
            queryset = Category.objects.filter(type_level__in=[3,4])
            self.fields['category'].queryset = queryset
        else:
            categories = obj.categories.all().values_list('pk', flat=True) 
            queryset = Category.objects.filter(active=True, type_level__in=[3,4]).exclude(pk__in=categories)
            self.fields['category'].queryset = queryset

        self.fields['category'].widget.attrs['class'] = form_class
        self.fields['category'].required = True
        self.fields['prd_order'].widget.attrs['class'] = form_class
        self.fields['cat_order'].widget.attrs['class'] = form_class
        self.fields['active'].widget.attrs['class'] = 'js-switch'
        self.fields['active'].widget.attrs['data-switchery'] = 'true'
        
        self.fields['is_main'].widget.attrs['class'] = 'js-switch'
        self.fields['is_main'].widget.attrs['data-switchery'] = 'true'
        
    class Meta:
        model = ProductCategory
        fields = (
            'category', 'prd_order', 'cat_order', 'active',
            'is_main')

    def clean(self):
        super(ProductCategoryForm, self).clean()


    def clean_category(self):
        category = self.cleaned_data.get('category', None)
        if category:
            pass
        else:
            raise forms.ValidationError(
                "This field is required.")
        return category


class CategoryInlineFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super(CategoryInlineFormSet, self).clean()
        if any(self.errors):
            return
        categories = []
        main_category = []
        duplicates = False
        duplicates_main = False
        for form in self.forms:
            if form.cleaned_data:
                category = form.cleaned_data['category']
                is_main = form.cleaned_data['is_main']
                product = form.cleaned_data['product']
                if category in categories:
                    duplicates = True
                categories.append(category)

                if is_main:
                    if main_category:
                        duplicates_main = True
                    main_category.append(category)

                if duplicates:
                    raise forms.ValidationError(
                        'Categories must be unique.',
                        code='duplicate_parent'
                    )

                if duplicates_main:
                    raise forms.ValidationError(
                        'Main category must be Unique',
                        code='double_main'
                    )
        return



class ProductFAQForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        obj = kwargs.pop('object', None)
        vendor = kwargs.pop('vendor', None)
        super(ProductFAQForm, self).__init__(*args, **kwargs)
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

        form_class = 'form-control col-md-7 col-xs-12'
        self.fields['question'].widget.attrs['class'] = form_class
        self.fields['question'].required = True        
        self.fields['question_order'].widget.attrs['class'] = form_class
        self.fields['active'].widget.attrs['class'] = 'js-switch'
        self.fields['active'].widget.attrs['data-switchery'] = 'true'
        
    class Meta:
        model = FAQProduct
        fields = (
            'question', 'question_order', 'active',)

    def clean(self):
        super(ProductFAQForm, self).clean()


    def clean_question(self):
        question = self.cleaned_data.get('question', None)
        if question:
            pass
        else:
            raise forms.ValidationError(
                "This field is required.")
        return question


class FAQInlineFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super(FAQInlineFormSet, self).clean()
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


class ProductChildForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        obj = kwargs.pop('object', None)
        super(ProductChildForm, self).__init__(*args, **kwargs)
        queryset = Product.objects.filter(active=True, type_product__in=[0,4,5]).exclude(pk=obj.pk)
        if self.instance.pk:
            self.fields['children'].queryset = queryset
        else:
            childs = obj.childs.filter(type_product__in=[0,4,5]).values_list('pk', flat=True) 
            queryset = queryset.exclude(pk__in=childs)
            self.fields['children'].queryset = queryset

        form_class = 'form-control col-md-7 col-xs-12'
        self.fields['children'].widget.attrs['class'] = form_class
        self.fields['children'].required = True        
        self.fields['sort_order'].widget.attrs['class'] = form_class
        self.fields['price_offset'].widget.attrs['class'] = form_class
        self.fields['price_offset_percent'].widget.attrs['class'] = form_class
        self.fields['active'].widget.attrs['class'] = 'js-switch'
        self.fields['active'].widget.attrs['data-switchery'] = 'true'

    class Meta:
        model = ChildProduct
        fields = (
            'children', 'sort_order', 'price_offset', 'price_offset_percent', 'active',)

    def clean(self):
        super(ProductChildForm, self).clean()


    def clean_children(self):
        children = self.cleaned_data.get('children', None)
        if children:
            pass
        else:
            raise forms.ValidationError(
                "This field is required.")
        return children


class ChildInlineFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super(ChildInlineFormSet, self).clean()
        if any(self.errors):
            return
        childs = []
        duplicates = False
        for form in self.forms:
            if form.cleaned_data:
                child = form.cleaned_data['children']
                product = form.cleaned_data['father']
                if child in childs:
                    duplicates = True
                childs.append(child)
                if child.type_product in [1, 2, 3]:
                    raise forms.ValidationError(
                        'Childs can only be standalone, virtual product.',
                        code='duplicate_parent'
                    )
                
                if child == product:
                    raise forms.ValidationError(
                        'Childs must be different.',
                        code='duplicate_parent'
                    )
                if duplicates:
                    raise forms.ValidationError(
                        'Childs must be unique.',
                        code='duplicate_parent'
                    )
        return


class ProductRelatedForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        obj = kwargs.pop('object', None)
        super(ProductRelatedForm, self).__init__(*args, **kwargs)
        queryset = Product.objects.filter(active=True, type_product__in=[0,4,5], product_class__in=[2,3]).exclude(pk=obj.pk)
        if self.instance.pk:
            self.fields['secondary'].queryset = queryset
        else:
            relations = obj.related.all().values_list('pk', flat=True) 
            queryset = queryset.exclude(pk__in=relations)
            self.fields['secondary'].queryset = queryset

        form_class = 'form-control col-md-7 col-xs-12'
        self.fields['secondary'].widget.attrs['class'] = form_class
        self.fields['secondary'].required = True
        self.fields['sort_order'].widget.attrs['class'] = form_class
        self.fields['price_offset'].widget.attrs['class'] = form_class
        self.fields['price_offset_percent'].widget.attrs['class'] = form_class
        self.fields['type_relation'].widget.attrs['class'] = form_class
        self.fields['ranking'].widget.attrs['class'] = form_class
        self.fields['active'].widget.attrs['class'] = 'js-switch'
        self.fields['active'].widget.attrs['data-switchery'] = 'true'

    class Meta:
        model = RelatedProduct
        fields = (
            'secondary', 'sort_order', 'price_offset', 'price_offset_percent', 'active',
            'type_relation', 'ranking')

    def clean(self):
        super(ProductRelatedForm, self).clean()

    def clean_secondary(self):
        secondary = self.cleaned_data.get('secondary', None)
        if secondary:
            pass
        else:
            raise forms.ValidationError(
                "This field is required.")
        return secondary


class RelatedInlineFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super(RelatedInlineFormSet, self).clean()
        if any(self.errors):
            return
        relatives = []
        duplicates = []
        for form in self.forms:
            if form.cleaned_data:
                rel = form.cleaned_data['secondary']
                product = form.cleaned_data['primary']
                type_relation = form.cleaned_data['type_relation']
                if rel == product:
                    raise forms.ValidationError(
                        'Related must be different.',
                        code='duplicate_parent'
                    )
                if rel in duplicates:
                    raise forms.ValidationError(
                        'Related must be unique.',
                        code='duplicate_unique'
                    )
                duplicates.append(rel)
                
        return


class ProductVariationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        obj = kwargs.pop('object', None)
        super(ProductVariationForm, self).__init__(*args, **kwargs)
        form_class = 'form-control col-md-7 col-xs-12'
        self.fields['sort_order'].widget.attrs['class'] = form_class
        self.fields['active'].widget.attrs['class'] = 'js-switch'
        self.fields['active'].widget.attrs['data-switchery'] = 'true'

    class Meta:
        model = VariationProduct
        fields = (
            'sort_order', 'active', )

    def clean(self):
        super(ProductVariationForm, self).clean()


class VariationInlineFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super(VariationInlineFormSet, self).clean()
        if any(self.errors):
            return


class ChangeProductVariantForm(forms.ModelForm):
    FIELD_FACTORIES = FIELD_FACTORIES
    PRODUCT_TYPE_FLOW_FIELD_ATTRS = PRODUCT_TYPE_FLOW_FIELD_ATTRS
    class Meta:
        model = Product
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
        
        super(ChangeProductVariantForm, self).__init__(*args, **kwargs)
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
        
        super(ChangeProductVariantForm, self).clean()
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
        self.instance.attr.initiate_attributes()
        for attribute in self.instance.attr.get_all_attributes():
            field_name = 'attribute_%s' % attribute.name
            if field_name in self.cleaned_data:
                value = self.cleaned_data[field_name]
                setattr(self.instance.attr, attribute.name, value)
        productscreen = super(ChangeProductVariantForm, self).save(
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
                value = instance.productattributes.get(
                    attribute=attribute).value
            except exceptions.ObjectDoesNotExist:
                pass
            else:
                kwargs['initial']['attribute_%s' % attribute.name] = value
        

class ProductChapterForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        obj = kwargs.pop('object', None)
        super(ProductChapterForm, self).__init__(*args, **kwargs)
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
        model = Chapter
        fields = (
            'heading', 'answer', 'ordering', 'status')

    def clean(self):
        super(ProductChapterForm, self).clean()


    def clean_heading(self):
        heading = self.cleaned_data.get('heading', None)
        if heading:
            pass
        else:
            raise forms.ValidationError(
                "This field is required.")
        return heading

class ChapterInlineFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super(ChapterInlineFormSet, self).clean()
        if any(self.errors):
            return

class SkillTypeForm(forms.Form):

    product_skill = forms.CharField(
        max_length=500,
        widget=forms.TextInput(attrs={
            'class': 'form-control col-md-3 col-xs-12',
            'placeholder':'Add skills'}),
        required=False
    )

    required_skill = forms.CharField(
        max_length=500,
        widget=forms.TextInput(attrs={
            'class': 'form-control col-md-3 col-xs-12',
            'placeholder':'Add skills'}),
        required=False
    )


    def save(self, commit=True):
        product = Product.objects.filter(id=self.data.get('product','')).first()

        new_product_skills = self.cleaned_data.get('product_skill','')
        new_required_skills = self.cleaned_data.get('required_skill','')

        new_product_skills = new_product_skills.split(",") if new_product_skills!='' else []
        new_required_skills = new_required_skills.split(",") if new_required_skills!='' else []

        old_product_skills = []
        old_required_skills = []

        product_skill = ProductSkill.objects.filter(product=product, active=True)
        for prd_sk in product_skill:
            if prd_sk.relation_type == 1:
                old_product_skills.append(prd_sk.skill.name.lower())
            elif prd_sk.relation_type == 2:
                old_required_skills.append(prd_sk.skill.name.lower())

        added_skills = { 1: list(set(new_product_skills)-set(old_product_skills)),
            2: list(set(new_required_skills)-set(old_required_skills))}

        deleted_skills = {1: list(set(old_product_skills)-set(new_product_skills)),
            2: list(set(old_required_skills)-set(new_required_skills))}

        for relation_type, skill_list in deleted_skills.items():
            for sk in skill_list:
                ProductSkill.objects.filter(product=product,
                    skill=Skill.objects.get(name=sk),
                    relation_type=relation_type).update(active=False)  

        for relation_type, skill_list in added_skills.items():
            for sk in skill_list:
                skill , created= Skill.objects.get_or_create(name=sk)
                sps , created_skill = ProductSkill.objects.get_or_create(skill=skill, product=product, relation_type=relation_type)
                sps.active = True
                sps.save()

        
# class AddProductBaseForm(forms.ModelForm):

#     class Meta:
#         model = Product
#         fields = [
#             'name', 'type_service',
#             'type_product', 'upc']

# class AddProductForm(AddProductBaseForm):

#     inr_price = forms.DecimalField(max_digits=12, decimal_places=2)

#     class Meta(AddProductBaseForm.Meta):
#         fields = AddProductBaseForm.Meta.fields + ['inr_price']

#     def __init__(self, *args, **kwargs):
#         super(AddProductForm, self).__init__(*args, **kwargs)
#         form_class = 'form-control col-md-7 col-xs-12'
        
#         self.fields['type_service'].widget.attrs['class'] = form_class
#         self.fields['type_service'].widget.attrs['data-parsley-notdefault'] = ''
#         self.fields['type_product'].widget.attrs['class'] = form_class
                       
#         self.fields['inr_price'].widget.attrs['class'] = form_class
#         self.fields['inr_price'].required = True
        
#         self.fields['name'].widget.attrs['class'] = form_class
#         self.fields['name'].widget.attrs['maxlength'] = 100
#         self.fields['name'].widget.attrs['placeholder'] = 'Add product name'
#         self.fields['name'].widget.attrs['data-parsley-trigger'] = 'change'
#         self.fields['name'].widget.attrs['data-parsley-required-message'] = 'This field is required.'
#         self.fields['name'].widget.attrs['data-parsley-length'] = "[4, 100]"
#         self.fields['name'].widget.attrs['data-parsley-length-message'] = 'Length should be between 4-100 characters.'
        
#         self.fields['upc'].widget.attrs['class'] = form_class
#         self.fields['upc'].widget.attrs['maxlength'] = 100
#         self.fields['upc'].widget.attrs['placeholder'] = 'Add Universal Product Code'
#         self.fields['upc'].widget.attrs['data-parsley-trigger'] = 'change'
#         self.fields['upc'].widget.attrs['data-parsley-required-message'] = 'This field is required.'
#         self.fields['upc'].widget.attrs['data-parsley-length'] = "[4, 100]"
#         self.fields['upc'].widget.attrs['data-parsley-length-message'] = 'Length should be between 4-100 characters.'

#     def clean_name(self):
#         name = self.cleaned_data.get('name', '')
#         if name:
#             if len(name) < 4 or len(name) > 100:
#                 raise forms.ValidationError(
#                     "Name should be between 4-100 characters.")
#         else:
#             raise forms.ValidationError(
#                 "This field is required.")
#         return name

    
#     def clean_type_flow(self):
#         flow = self.cleaned_data.get('type_flow', '')
#         if flow:
#             if int(flow) == 0:
#                 raise forms.ValidationError(
#                     "This should not be default.")
#         else:
#             raise forms.ValidationError(
#                 "This field is required.")
#         return flow

#     def clean_upc(self):
#         upc = self.cleaned_data.get('upc', '')
#         if upc:
#             if len(upc) < 4 or len(upc) > 100:
#                 raise forms.ValidationError(
#                     "Name should be between 4-100 characters.")
#         else:
#             raise forms.ValidationError(
#                 "This field is required.")
#         return upc

    
#     def save(self, commit=True, *args, **kwargs):
#         product = super(AddProductForm, self).save(
#             commit=True, *args, **kwargs)
#         return product

