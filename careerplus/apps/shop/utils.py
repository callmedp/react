from decimal import Decimal
from django import forms
from django.core import exceptions
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
from django.utils.html import format_html

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.db import IntegrityError, transaction
from django.core import exceptions
from decimal import Decimal
from django.contrib import messages
from shop.choices import PRODUCT_VENDOR_CHOICES


def _attribute_text_field(attribute, attrs={}):
    attr = {'class': 'form-control col-md-7 col-xs-12'}
    attr.update(attrs)
    return forms.CharField(
        label=attribute.display_name,
        required=attribute.required,
        widget=forms.TextInput(
            attrs=attr))

def _attribute_textarea_field(attribute, attrs={}):
    attr = {'class': 'form-control col-md-7 col-xs-12'}
    attr.update(attrs)
    return forms.CharField(
        label=attribute.display_name,
        required=attribute.required,
        widget=forms.Textarea(
            attrs=attr))

def _attribute_integer_field(attribute, attrs={}):
    attr = {'class': 'form-control col-md-7 col-xs-12'}
    attr.update(attrs)
    return forms.IntegerField(
        label=attribute.display_name,
        required=attribute.required,
        widget=forms.NumberInput(
            attrs=attr),)

def _attribute_boolean_field(attribute, attrs={}):
    attr = {'class': 'js-switch'}
    attr.update(attrs)
    return forms.BooleanField(
        label=attribute.display_name,
        required=False,
        widget=forms.CheckboxInput(
            attrs=attr),)

def _attribute_float_field(attribute, attrs={}):
    attr = {'class': 'form-control col-md-7 col-xs-12'}
    attr.update(attrs)
    return forms.FloatField(
        label=attribute.display_name,
        required=attribute.required,
        widget=forms.NumberInput(
            attrs=attr),)

def _attribute_date_field(attribute, attrs={}):
    attr = {'class': 'form-control col-md-7 col-xs-12'}
    attr.update(attrs)
    return forms.DateField(label=attribute.display_name,
        required=attribute.required,
        widget=forms.widgets.DateInput(
            attrs=attr),)

def _attribute_option_field(attribute, attrs={}):
    attr = {'class': 'form-control col-md-7 col-xs-12'}
    attr.update(attrs)
    return forms.ModelChoiceField(
        label=attribute.display_name,
        required=attribute.required,
        queryset=attribute.option_group.options.all(),
        empty_label = 'Select',
        widget=forms.widgets.Select(
            attrs=attr),)


def _attribute_multi_option_field(attribute, attrs={}):
    attr = {'class': 'js-switch'}
    attr.update(attrs)
    return forms.ModelMultipleChoiceField(
        label=attribute.display_name,
        required=attribute.required,
        queryset=attribute.option_group.options.all(),
        widget=forms.widgets.SelectMultiple(
            attrs=attr),)

def _attribute_numeric_field(attribute, attrs={}):
    return forms.FloatField(label=attribute.display_name,
        required=attribute.required)


def _attribute_file_field(attribute, attrs={}):
    attr = {'class': 'form-control col-md-7 col-xs-12 clearimg'}
    attr.update(attrs)
    return forms.FileField(
        label=attribute.display_name,
        required=attribute.required,
        widget=forms.widgets.ClearableFileInput(
            attrs=attr)
        )


def _attribute_image_field(attribute, attrs):
    attr = {'class': 'form-control col-md-7 col-xs-12 clearimg'}
    attr.update(attrs)
    return forms.ImageField(
        label=attribute.display_name,
        required=attribute.required,
        widget=forms.widgets.ClearableFileInput(
            attrs=attr),)


FIELD_FACTORIES = {
        "text": _attribute_text_field,
        "richtext": _attribute_textarea_field,
        "integer": _attribute_integer_field,
        "boolean": _attribute_boolean_field,
        "float": _attribute_float_field,
        "date": _attribute_date_field,
        "option": _attribute_option_field,
        "multi_option": _attribute_multi_option_field,
        "numeric": _attribute_numeric_field,
        "file": _attribute_file_field,
        "image": _attribute_image_field,
    }

PRODUCT_TYPE_FLOW_FIELD_ATTRS = {
    'file': {
        14: {
            'data-parsley-max-file-size': 4096,
            'data-parsley-filemimetypes': 'application/pdf'
        },
        -1: {'data-parsley-max-file-size': 250}
    },
    'boolean': {
        -1: {'data-switchery': True}
    },
    'option': {
        -1: {'data-parsley-notdefault': ''}
    },
    'image': {
        -1: {
            'data-parsley-max-file-size': 250,
            'data-parsley-filemimetypes': 'image/jpeg, image/png, image/jpg, image/svg'
        }
    }
}


class ProductAttributesContainer(object):

    def __setstate__(self, state):
        self.__dict__ = state
        self.initialised = False

    def __init__(self, product):
        self.product = product
        self.initialised = False

    def initiate_attributes(self):
        values = self.get_values().select_related('attribute')
        for v in values:
            setattr(self, v.attribute.name, v.value)
        self.initialised = True

    def __getattr__(self, name):
        if not name.startswith('_') and not self.initialised:
            self.initiate_attributes()
            return getattr(self, name)
        raise AttributeError(
            _("%(obj)s has no attribute named '%(attr)s'") % {
                'obj': self.product.product_class, 'attr': name})

    def validate_attributes(self):
        for attribute in self.get_all_attributes():
            value = getattr(self, attribute.name, None)
            if value is None:
                if attribute.required:
                    raise ValidationError(
                        _("%(attr)s attribute cannot be blank") %
                        {'attr': attribute.name})
            else:
                try:
                    attribute.validate_value(value)
                except ValidationError as e:
                    raise ValidationError(
                        _("%(attr)s attribute %(err)s") %
                        {'attr': attribute.name, 'err': e})

    def get_values(self):
        from shop.models import Product, ProductScreen
        if isinstance(self.product, ProductScreen):
            return self.product.screenattributes.all()
        elif isinstance(self.product, Product):
            return self.product.productattributes.all()

    def get_value_by_attribute(self, attribute):
        return self.get_values().get(attribute=attribute)

    def get_all_attributes(self):
        if self.product:
            if self.product.product_class:
                return self.product.product_class.attributes.filter(active=True)  
        return self.objects.none()

    def get_attribute_by_name(self, name):
        return self.get_all_attributes().get(name=name)

    def __iter__(self):
        return iter(self.get_values())

    def save_screen(self):
        for attribute in self.get_all_attributes():
            if hasattr(self, attribute.name):
                value = getattr(self, attribute.name)
                attribute.save_screen_value(self.product, value)

    def save(self):
        for attribute in self.get_all_attributes():
            if hasattr(self, attribute.name):
                value = getattr(self, attribute.name)
                attribute.save_value(self.product, value)


class ProductModeration(object):

    def validate_fields(self, request, product):
        test_pass = False
        try:
            if request and request.user:
                if product:
                    # if not product.heading:
                    #     messages.error(request, "Product Heading is required")
                    #     return test_pass
                    if not product.name:
                        messages.error(request, "Product Name is required")
                        return test_pass
                    if not product.product_class:
                        messages.error(request, "Product Class is required")
                        return test_pass
                    if product.inr_price < Decimal(0):
                        messages.error(request, "INR Price is negetive")
                        return test_pass
                    if product.type_product in [0,1,3,5]:
                        if product.is_course:
                            if not product.chapter_product.filter(status=True):
                                messages.error(request, "Product has no active chapter")
                                return test_pass
                    if request.user.groups.filter(name='Product').exists() or request.user.is_superuser:
                        diction = [0, 1, 3, 4, 5]
                    else:
                        diction = [0, 1]
                    if product.type_product in diction:
                            pass
                    else:
                        messages.error(request, "Invalid Product Choice")
                        return test_pass
                    if product.type_product in [0, 1, 3, 4] and product.type_flow != 16:
                        if not product.description:
                            messages.error(request, "Description is required")
                            return test_pass
                    if not product.countries.all().exists():
                        messages.error(request, "Available Country is required")
                        return test_pass

                    if product.type_flow == 14:
                        attributes = ['batch_launch_date', 'apply_last_date',
                                      'application_process',
                                      'attendees_criteria', "payment_deadline"]
                        for attr in attributes:
                            if not getattr(product.screen_university_course_detail, attr):
                                messages.error(request, "Univeristy Course details are required")
                                return test_pass
                    test_pass = True
                    return test_pass
                else:
                    messages.error(request, "Object Do not Exists")
                    return test_pass
            else:
                return test_pass        
        except Exception as e:
            test_pass = False
            messages.error(request, (
                ("%(msg)s : %(err)s") % {'msg': 'Contact Tech ERROR', 'err': e}))
        return test_pass

    def validate_variation(self, request, product):
        test_pass = False
        try:
            if request and request.user:
                if product:
                    if product.type_product == 1:
                        childs = product.mainproduct.filter(active=True)
                        if not childs:
                            messages.error(request, "No Variation is created.")
                            return test_pass
                        for child in childs:
                            sibling = child.sibling
                            if not sibling.product:
                                messages.error(request, "Variation" + str(sibling) +" Product is not associated.")
                                return test_pass
                            if not sibling.name:
                                messages.error(request, "Variation" + str(sibling) +" Name is required")
                                return test_pass
                            if not sibling.inr_price:
                                messages.error(request, "Variation" + str(sibling) +" INR Price is required")
                                return test_pass
                            if sibling.inr_price < Decimal(0):
                                messages.error(request, "Variation" + str(sibling) +" INR Price is negetive")
                                return test_pass

                    test_pass = True
                    return test_pass
                else:
                    messages.error(request, "Object Do not Exists")
                    return test_pass
            else:
                return test_pass        
        except Exception as e:
            test_pass = False
            messages.error(request, (
                ("%(msg)s : %(err)s") % {'msg': 'Contact Tech ERROR', 'err': e}))
        return test_pass

    def validate_screenproduct(self, request, productscreen):
        test_pass = False
        try:
            if request and request.user:
                if productscreen:
                    vendor = request.user.get_vendor()
                    if not productscreen.vendor:
                        messages.error(request, "Vendor is not associated")
                        return test_pass
                    if not productscreen.product:
                        messages.error(request, "Product is not associated")
                        return test_pass
                            
                    if not self.validate_fields(
                        request=request, product=productscreen):
                        return test_pass
                    if productscreen.type_product == 1:
                        if not self.validate_variation(
                            request=request, product=productscreen):
                            return test_pass
                        
                    test_pass = True    
                    return test_pass
                else:
                    messages.error(request, "Object Do not Exists")
                    return test_pass
            else:
                return test_pass         
        except Exception as e:
            test_pass = False
            messages.error(request, (
                ("%(msg)s : %(err)s") % {'msg': 'Contact Tech ERROR', 'err': e}))
        return test_pass

    @transaction.atomic
    def copy_to_product(self, request, product, screen):
        copy = False
        try:
            with transaction.atomic():

                product.heading = screen.name
                product.upc = screen.upc
                product.product_class = screen.product_class
                product.type_product = screen.type_product
                product.type_flow = screen.type_flow
                product.sub_type_flow = screen.sub_type_flow
                
                product.about = screen.about
                product.description = screen.description
                product.buy_shine = screen.buy_shine
                # product.prg_structure = screen.prg_structure
                
                product.inr_price = screen.inr_price
                product.fake_inr_price = screen.fake_inr_price
                product.usd_price = screen.usd_price
                product.fake_usd_price = screen.fake_usd_price
                product.aed_price = screen.aed_price
                product.fake_aed_price = screen.fake_aed_price
                product.gbp_price = screen.gbp_price
                product.fake_gbp_price = screen.fake_gbp_price
                product.vendor = screen.vendor
                product.countries = screen.countries.all()
                product.save()
                screen.attr.initiate_attributes()
                product.attr.initiate_attributes()
                for attribute in screen.attr.get_all_attributes():
                    if hasattr(screen.attr, attribute.name):
                        value = getattr(screen.attr, attribute.name)
                        setattr(product.attr, attribute.name, value)
                
                product.save()
                from shop.models import (
                    FAQProduct, VariationProduct,
                    ProductSkill, UniversityCoursePayment)

                productfaq = product.productfaqs.all()
                screenfaq = screen.screenfaqs.all()
                scfq = screen.faqs.all()
                prdfq = product.faqs.all()
                for faq in screenfaq:
                    fqprd, created = FAQProduct.objects.get_or_create(
                        product=product,
                        question=faq.question)
                    fqprd.active = faq.active
                    fqprd.question_order = faq.question_order
                    fqprd.save()
                inactive_fq = [fq for fq in prdfq if fq not in scfq]
                for faq in inactive_fq:
                    fqprd, created = FAQProduct.objects.get_or_create(
                        product=product,
                        question=faq)
                    fqprd.active = False
                    fqprd.save()

                screen_skills = screen.screenskills.all()
                for screenskill in screen_skills:
                    skillprd, created = ProductSkill.objects.get_or_create(
                    product=product,
                    skill=screenskill.skill)

                    skillprd.active = screenskill.active
                    skillprd.priority = screenskill.priority
                    skillprd.save()
                
                screenchap = screen.chapter_product.all()
                prdchap = product.chapter_product.all()
                for chap in screenchap:
                    pchap = chap.create_chapter()
                    pchap.heading = chap.heading
                    pchap.answer = chap.answer
                    pchap.status = chap.status
                    pchap.ordering = chap.ordering
                    pchap.product = product
                    pchap.save()
                screenchap = [ch.chapter for ch in screenchap]
                inactive_chap = [ch for ch in prdchap if ch not in screenchap]
                
                for chap in inactive_chap:
                    chap.status = False
                    chap.save()
                
                if screen.type_product == 1:
                    screenvar = screen.variation.all()
                    screenvariation = screen.mainproduct.all()
                    productvar = product.variation.all()
                    productvariation = product.mainproduct.all()
                    screenvar = [scr.product for scr in screenvar]
                    for scv in screenvariation:
                        vscreen = scv.sibling
                        vproduct = vscreen.product
                        
                        vproduct.name = vscreen.name
                        vproduct.upc = vscreen.upc
                        vproduct.product_class = vscreen.product_class
                        vproduct.type_product = vscreen.type_product
                        vproduct.type_flow = vscreen.type_flow
                        vproduct.inr_price = vscreen.inr_price
                        vproduct.fake_inr_price = vscreen.fake_inr_price
                        vproduct.usd_price = vscreen.usd_price
                        vproduct.fake_usd_price = vscreen.fake_usd_price
                        vproduct.aed_price = vscreen.aed_price
                        vproduct.fake_aed_price = vscreen.fake_aed_price
                        vproduct.gbp_price = vscreen.gbp_price
                        vproduct.fake_gbp_price = vscreen.fake_gbp_price
                        vproduct.vendor = vscreen.vendor
                        vproduct.save()

                        vscreen.attr.initiate_attributes()
                        vproduct.attr.initiate_attributes()
                        for attribute in vscreen.attr.get_all_attributes():
                            if hasattr(vscreen.attr, attribute.name):
                                value = getattr(vscreen.attr, attribute.name)
                                setattr(vproduct.attr, attribute.name, value)
                        vproduct.save()
                        
                        pv, created = VariationProduct.objects.get_or_create(
                            main=product,
                            sibling=vproduct,
                            )
                        pv.active = scv.active
                        pv.sort_order = scv.sort_order
                        pv.save()
                    inactive_var = [var for var in productvar if var not in screenvar]
                    for pvar in inactive_var:
                        pv, created = VariationProduct.objects.get_or_create(
                            main=product,
                            sibling=pvar)
                        pv.active = False
                        pv.save()
                for attribute in screen.attr.get_all_attributes():
                    if hasattr(screen.attr, attribute.name):
                        value = getattr(screen.attr, attribute.name)
                        
                        attribute.save_value(product, value)
                if screen.type_flow == 14:
                    attributes = ['batch_launch_date', 'apply_last_date', 'sample_certificate', 
                                  'application_process', 'assesment', "benefits", 'eligibility_criteria',
                                  'attendees_criteria',"payment_deadline", "highlighted_benefits"]
                    for attr in attributes:
                        setattr(product.university_course_detail, attr, getattr(screen.screen_university_course_detail, attr))
                    product.university_course_detail.save()

                    product.type_flow = screen.type_flow
                    for university_payment in screen.screen_university_course_payment.all():
                        UniversityCoursePayment.objects.create(
                            product=product,
                            installment_fee=university_payment.installment_fee,
                            last_date_of_payment=university_payment.last_date_of_payment,
                            active=university_payment.active
                        )
                product.save()
                
                copy = True

                return (product, screen, copy)
        except IntegrityError:
            copy = False
        except Exception as e:
            copy = False
            messages.error(request, (
                ("%(msg)s : %(err)s") % {'msg': 'Contact Tech ERROR', 'err': e}))
        return (product, screen, copy)

    @transaction.atomic
    def copy_to_screen(self, request,product, screen):
        copy = False
        try:
            with transaction.atomic():
                screen.name = product.heading
                screen.upc = product.upc
                screen.product_class = product.product_class
                screen.type_product = product.type_product
                
                screen.about = product.about
                screen.description = product.description
                screen.buy_shine = product.buy_shine
                # screen.prg_structure = product.prg_structure
                
                screen.inr_price = product.inr_price
                screen.fake_inr_price = product.fake_inr_price
                screen.usd_price = product.usd_price
                screen.fake_usd_price = product.fake_usd_price
                screen.aed_price = product.aed_price
                screen.fake_aed_price = product.fake_aed_price
                screen.gbp_price = product.gbp_price
                screen.fake_gbp_price = product.fake_gbp_price

                screen.countries = product.countries.all()
                screen.vendor = product.vendor
                screen.save()
                screen.attr.initiate_attributes()
                product.attr.initiate_attributes()
                for attribute in product.attr.get_all_attributes():
                    if hasattr(product.attr, attribute.name):
                        value = getattr(product.attr, attribute.name)
                        setattr(screen.attr, attribute.name, value)
                screen.save()
                
                from shop.models import FAQProductScreen, VariationProductScreen
                productfaq = product.productfaqs.all()
                screenfaq = screen.screenfaqs.all()
                scfq = screen.faqs.all()
                prdfq = product.faqs.all()
                for faq in productfaq:
                    sfqprd, created = FAQProductScreen.objects.get_or_create(
                        product=screen,
                        question=faq.question)
                    sfqprd.active = faq.active
                    sfqprd.question_order = faq.question_order
                    sfqprd.save()
                inactive_fq = [fq for fq in scfq if fq not in prdfq]
                for faq in inactive_fq:
                    fqprd, created = FAQProductScreen.objects.get_or_create(
                        product=screen,
                        question=faq)
                    fqprd.active = False
                    fqprd.save()

                screenchap = screen.chapter_product.all()
                prdchap = product.chapter_product.all()
                for chap in prdchap:
                    schap = chap.create_screen()
                    schap.heading = chap.heading
                    schap.answer = chap.answer
                    schap.status = chap.status
                    schap.ordering = chap.ordering
                    schap.product = screen
                    schap.save()
                
                prdchap = [ch.get_screen() for ch in prdchap]
                inactive_chap = [ch for ch in prdchap if ch not in screenchap]
                
                for chap in inactive_chap:
                    chap.status = False
                    chap.save()
                
                if screen.type_product == 1:
                    screenvar = screen.variation.all()
                    screenvariation = screen.mainproduct.all()
                    productvar = product.variation.all()
                    productvariation = product.mainproduct.all()
                    productvar = [pv.get_screen() for pv in productvar]
                    for pv in productvariation:
                        vproduct = pv.sibling
                        vscreen = vproduct.get_screen()
                        
                        vscreen.name = vproduct.name
                        vscreen.upc = vproduct.upc
                        vscreen.product_class = vproduct.product_class
                        vscreen.type_product = vproduct.type_product
                        
                        vscreen.inr_price = vproduct.inr_price
                        vscreen.fake_inr_price = vproduct.fake_inr_price
                        vscreen.usd_price = vproduct.usd_price
                        vscreen.fake_usd_price = vproduct.fake_usd_price
                        vscreen.aed_price = vproduct.aed_price
                        vscreen.fake_aed_price = vproduct.fake_aed_price
                        vscreen.gbp_price = vproduct.gbp_price
                        vscreen.fake_gbp_price = vproduct.fake_gbp_price
                        vscreen.vendor = vproduct.vendor
                        vscreen.save()
                        vscreen.attr.initiate_attributes()
                        vproduct.attr.initiate_attributes()
                        for attribute in vproduct.attr.get_all_attributes():
                            if hasattr(vproduct.attr, attribute.name):
                                value = getattr(vproduct.attr, attribute.name)
                                setattr(vscreen.attr, attribute.name, value)
                        vscreen.save()
                        
                        spv, created = VariationProductScreen.objects.get_or_create(
                            main=screen,
                            sibling=vscreen,
                            )
                        spv.active = pv.active
                        spv.sort_order = pv.sort_order
                        spv.save()
                    inactive_svar = [var for var in screenvar if var not in productvar]
                    for svar in inactive_svar:
                        spv, created = VariationProductScreen.objects.get_or_create(
                            main=screen,
                            sibling=svar)
                        spv.active = False
                        spv.save()
            
                copy = True
                return (product, screen, copy)
        
        except IntegrityError:
            copy = False
        except Exception as e:
            copy = False
            messages.error(request, (
                ("%(msg)s : %(err)s") % {'msg': 'Contact Tech ERROR', 'err': e}))
        return (product, screen, copy)


class CategoryValidation(object):

    def validate_before_university(self, request, category):
        test_pass = False
        try:
            if request and category:
                if not self.validate_fields(
                    request=request, category=category):
                    return test_pass
                if category.type_level in [2, 3, 4]:
                    if not self.validate_parent(
                        request=request, category=category):
                        return test_pass
                if not self.validate_universitypage(
                    request=request, category=category):
                    return test_pass
                test_pass = True
                return test_pass
            else:
                messages.error(request, "Object Do not Exists")
                return test_pass
        except Exception as e:
            test_pass = False
            messages.error(request, (
                ("%(msg)s : %(err)s") % {'msg': 'Contact Tech ERROR', 'err': e}))
        return test_pass


    def validate_before_active(self, request, category):
        test_pass = False
        try:
            if request:
                if category:
                    if not self.validate_fields(
                        request=request, category=category):
                        return test_pass
                    if category.type_level in [2, 3, 4]:
                        if not self.validate_parent(
                            request=request, category=category):
                            return test_pass
                    if category.is_skill:
                        if not self.validate_skillpage(
                            request=request, category=category):
                            return test_pass
                    test_pass = True
                    return test_pass
                else:
                    messages.error(request, "Object Do not Exists")
                    return test_pass
            else:
                return test_pass         
        except Exception as e:
            test_pass = False
            messages.error(request, (
                ("%(msg)s : %(err)s") % {'msg': 'Contact Tech ERROR', 'err': e}))
        return test_pass


    def validate_before_inactive(self, request, category):
        test_pass = False
        try:
            if request:
                if category:
                    if category.type_level in [1, 2, 3]:
                        if not self.validate_childs(
                            request=request, category=category):
                            return test_pass
                    if category.check_products():
                        messages.error(request, "Products is associated please reassign")
                        return test_pass
                    test_pass = True
                    return test_pass
                else:
                    messages.error(request, "Object Do not Exists")
                    return test_pass
            else:
                return test_pass         
        except Exception as e:
            test_pass = False
            messages.error(request, (
                ("%(msg)s : %(err)s") % {'msg': 'Contact Tech ERROR', 'err': e}))
        return test_pass

    def validate_before_skill(self, request, category):
        test_pass = False
        try:
            if request:
                if category:
                    if not self.validate_fields(
                        request=request, category=category):
                        return test_pass
                    if category.type_level in [2, 3, 4]:
                        if not self.validate_parent(
                            request=request, category=category):
                            return test_pass
                    if not self.validate_skillpage(
                        request=request, category=category):
                        return test_pass
                    test_pass = True
                    return test_pass
                else:
                    messages.error(request, "Object Do not Exists")
                    return test_pass
            else:
                return test_pass         
        except Exception as e:
            test_pass = False
            messages.error(request, (
                ("%(msg)s : %(err)s") % {'msg': 'Contact Tech ERROR', 'err': e}))
        return test_pass

    def validate_fields(self, request, category):
        test_pass = False
        try:
            if request:
                if category:
                    if not category.name:
                        messages.error(request, "Category Name is required")
                        return test_pass
                    if not category.heading:
                        messages.error(request, "Category Display Heading is required")
                        return test_pass
                    if not category.type_level:
                        messages.error(request, "Category Level is required")
                        return test_pass
                    test_pass = True
                    return test_pass
                else:
                    messages.error(request, "Object Do not Exists")
                    return test_pass
            else:
                return test_pass         
        except Exception as e:
            test_pass = False
            messages.error(request, (
                ("%(msg)s : %(err)s") % {'msg': 'Contact Tech ERROR', 'err': e}))
        return test_pass

    
    def validate_parent(self, request, category):
        test_pass = False
        try:
            if request:
                if category:
                    if category.type_level == 1:
                        pass
                    elif category.type_level == 2:
                        parent = category.get_parent()
                        if not parent:
                            messages.error(request, "Level 1 parent is not assigned or active")
                            return test_pass
                    elif category.type_level == 3:
                        parent = category.get_parent()
                        if not parent:
                            messages.error(request, "Level 2 parent is not assigned or active")
                            return test_pass
                    elif category.type_level == 4:
                        parent = category.get_parent()
                        if not parent:
                            messages.error(request, "Level 3 parent is not assigned or active")
                            return test_pass
                    test_pass = True
                    return test_pass
                else:
                    messages.error(request, "Object Do not Exists")
                    return test_pass
            else:
                return test_pass         
        except Exception as e:
            test_pass = False
            messages.error(request, (
                ("%(msg)s : %(err)s") % {'msg': 'Contact Tech ERROR', 'err': e}))
        return test_pass

    
    def validate_skillpage(self, request, category):
        test_pass = False
        try:
            if request:
                if category:
                    if category.type_level in [1, 2]:
                        messages.error(request, "Level 1 Can't be made Skill")
                        return test_pass
                    if not category.description:
                        messages.error(request, "Skill Description is required")
                        return test_pass
                    if not category.career_outcomes:
                        messages.error(request, "Skill Career Outcomes is required")
                        return test_pass
                    if not category.check_products():
                        messages.error(request, "Skill Products is required")
                        return test_pass
                    test_pass = True
                    return test_pass
                else:
                    messages.error(request, "Object Do not Exists")
                    return test_pass
            else:
                return test_pass         
        except Exception as e:
            test_pass = False
            messages.error(request, (
                ("%(msg)s : %(err)s") % {'msg': 'Contact Tech ERROR', 'err': e}))
        return test_pass

    def validate_universitypage(self, request, category):
        test_pass = False
        try:
            if request:
                if category:
                    if category.type_level in [1, 2]:
                        messages.error(
                            request,
                            "Level 1 and 2 Can't be made University")
                        return test_pass
                    if not category.description:
                        messages.error(
                            request,
                            "University Description is required")
                        return test_pass
                    if not category.image:
                        messages.error(
                            request,
                            "University Image is required")
                        return test_pass

                    if not category.icon:
                        messages.error(
                            request,
                            "University Icon is required")
                        return test_pass

                    # if not category.check_products():
                    #     messages.error(request, "University Products is required")
                    #     return test_pass
                    test_pass = True
                    return test_pass
                else:
                    messages.error(request, "Object Do not Exists")
                    return test_pass
            else:
                return test_pass
        except Exception as e:
            test_pass = False
            messages.error(request, (
                ("%(msg)s : %(err)s") % {'msg': 'Contact Tech ERROR', 'err': e}))
        return test_pass

    
    def validate_childs(self, request, category):
        test_pass = False
        try:
            if request:
                if category:
                    if category.type_level == 1:
                        childs = category.get_childrens()
                        if childs:
                            messages.error(request, "Level 2 childs exists. Please inactive relationship between them")
                            return test_pass
                    elif category.type_level == 2:
                        childs = category.get_childrens()
                        if childs:
                            messages.error(request, "Level 3 childs exists. Please inactive relationship between them")
                            return test_pass
                    elif category.type_level == 3:
                        childs = category.get_childrens()
                        if childs:
                            messages.error(request, "Level 4 childs exists. Please inactive relationship between them")
                            return test_pass
                    elif category.type_level == 4:
                        pass
                    test_pass = True
                    return test_pass
                else:
                    messages.error(request, "Object Do not Exists")
                    return test_pass
            else:
                return test_pass         
        except Exception as e:
            test_pass = False
            messages.error(request, (
                ("%(msg)s : %(err)s") % {'msg': 'Contact Tech ERROR', 'err': e}))
        return test_pass



class ProductValidation(object):

    def validate_before_active(self, request, product):
        test_pass = False
        try:
            if request:
                if product:
                    
                    if not self.validate_fields(
                        request=request, product=product):
                            return test_pass
                    if not self.validate_category(
                        request=request, product=product):
                            return test_pass
                    if product.type_product in [0, 3, 4, 5]:
                        if not self.validate_attributes(
                            request=request, product=product):
                            return test_pass
                    if product.type_product == 1:
                        if not self.validate_variation(
                            request=request, product=product):
                            return test_pass
                    if product.type_product == 3:
                        if not self.validate_childs(
                            request=request, product=product):
                            return test_pass
                    test_pass = True
                    return test_pass
                else:
                    messages.error(request, "Object Do not Exists")
                    return test_pass
            else:
                return test_pass         
        except Exception as e:
            test_pass = False
            messages.error(request, (
                ("%(msg)s : %(err)s") % {'msg': 'Contact Tech ERROR', 'err': e}))
        return test_pass


    def validate_before_index(self, request, product):
        test_pass = False
        try:
            if request:
                if product:
                    if not product.active:
                        messages.error(request, "First Make Product Active")
                        return False
                    
                    if not self.validate_fields(
                        request=request, product=product):
                            return test_pass
                    if not self.validate_category(
                        request=request, product=product):
                            return test_pass
                    if product.type_product in [0, 3, 4, 5]:
                        if not self.validate_attributes(
                            request=request, product=product):
                            return test_pass
                    if product.type_product == 1:
                        if not self.validate_variation(
                            request=request, product=product):
                            return test_pass
                    if product.type_product == 3:
                        if not self.validate_childs(
                            request=request, product=product):
                            return test_pass
                    test_pass = True
                    return test_pass
                else:
                    messages.error(request, "Object Do not Exists")
                    return test_pass
            else:
                return test_pass         
        except Exception as e:
            test_pass = False
            messages.error(request, (
                ("%(msg)s : %(err)s") % {'msg': 'Contact Tech ERROR', 'err': e}))
        return test_pass

    def validate_fields(self, request, product):
        test_pass = False
        try:
            if request:
                if product:
                    if not product.vendor:
                        messages.error(request, "Product Vendor is Required")
                        return test_pass
                    if not product.heading:
                        messages.error(request, "Product Heading is required")
                        return test_pass
                    
                    if not product.name:
                        messages.error(request, "Product Name is required")
                        return test_pass
                    if not product.product_class:
                        messages.error(request, "Product Class is required")
                        return test_pass
                    if not product.type_flow:
                        messages.error(request, "Product Flow is required")
                        return test_pass
                    
                    if product.inr_price < Decimal(0):
                        messages.error(request, "INR Price is negetive")
                        return test_pass

                    if not product.image:
                        messages.error(request, "Product Image is Required")
                        return test_pass
                    
                    if not product.heading:
                        messages.error(request, "Product Display Heading is required")
                        return test_pass
                    
                    if product.type_product in [0,1,3,5]:
                        if product.is_course:
                            if not product.chapter_product.filter(status=True):
                                messages.error(request, "Product has no active chapter")
                                return test_pass
                    

                    if product.type_product in [0, 1, 3, 4] and product.type_flow != 16:
                        if not product.description:
                            messages.error(request, "Description is required")
                            return test_pass
                    if not product.countries.all().exists():
                        messages.error(request, "Available Country is required")
                        return test_pass
                    
                    test_pass = True
                    return test_pass
                else:
                    messages.error(request, "Object Do not Exists")
                    return test_pass
            else:
                return test_pass         
        except Exception as e:
            test_pass = False
            messages.error(request, (
                ("%(msg)s : %(err)s") % {'msg': 'Contact Tech ERROR', 'err': e}))
        return test_pass

    def validate_category(self, request, product):
        test_pass = False
        try:
            if request:
                if product:
                    if not product.productcategories.filter(active=True, category__active=True).exists():
                        messages.error(request, "Product Category is required")
                        return test_pass   
                    test_pass = True
                    return test_pass
                else:
                    messages.error(request, "Object Do not Exists")
                    return test_pass
            else:
                return test_pass         
        except Exception as e:
            test_pass = False
            messages.error(request, (
                ("%(msg)s : %(err)s") % {'msg': 'Contact Tech ERROR', 'err': e}))
        return test_pass

    
    def validate_childs(self, request, product):
        test_pass = False
        try:
            if request:
                if product:
                    if not product.parentproduct.filter(active=True).exists():
                        messages.error(request, "Product Childs is required")
                        return test_pass   
                    test_pass = True
                    return test_pass
                else:
                    messages.error(request, "Object Do not Exists")
                    return test_pass
            else:
                return test_pass         
        except Exception as e:
            test_pass = False
            messages.error(request, (
                ("%(msg)s : %(err)s") % {'msg': 'Contact Tech ERROR', 'err': e}))
        return test_pass

    def validate_variation(self, request, product):
        test_pass = False
        try:
            if request:
                if product:
                    if product.type_product != 1:
                        return True
                    varslist = product.mainproduct.filter(active=True)
                    if not varslist:
                        messages.error(request, "Product Variation is required")
                        return test_pass
                    for pv in varslist:
                        sibling = pv.sibling
                        if not sibling.name:
                            messages.error(request, "Variation" + str(sibling) +" Name is required")
                            return test_pass
                        if not sibling.upc:
                            messages.error(request, "Variation" + str(sibling) +" UPC is required")
                            return test_pass
                        if not sibling.inr_price:
                            messages.error(request, "Variation" + str(sibling) +" INR Price is required")
                            return test_pass
                        if sibling.inr_price < Decimal(0):
                            messages.error(request, "Variation" + str(sibling) +" INR Price is negetive")
                            return test_pass
                        if not self.validate_attributes(request=request, product=sibling):
                            return test_pass
                           
                    test_pass = True
                    return test_pass
                else:
                    messages.error(request, "Object Do not Exists")
                    return test_pass
            else:
                return test_pass         
        except Exception as e:
            test_pass = False
            messages.error(request, (
                ("%(msg)s : %(err)s") % {'msg': 'Contact Tech ERROR', 'err': e}))
        return test_pass

    def validate_attributes(self, request, product):
        test_pass = False
        try:
            if request:
                if product:
                    productattr = product.attr
                    for attribute in productattr.get_all_attributes():
                        value = getattr(productattr, attribute.name, None)
                        if value is None:
                            if attribute.required:    
                                messages.error(request, (
                                ("%(attr)s attribute cannot be blank") %
                                {'attr': attribute.name}))
                                return test_pass
                        else:
                            try:
                                attribute.validate_value(value)
                            except Exception as e:
                                messages.error(request, (
                                    ("%(attr)s attribute %(err)s") %
                                    {'attr': attribute.name, 'err': e}))
                                return test_pass
                    test_pass = True
                    return test_pass
                else:
                    messages.error(request, "Object Do not Exists")
                    return test_pass
            else:
                return test_pass         
        except Exception as e:
            test_pass = False
            messages.error(request, (
                ("%(msg)s : %(err)s") % {'msg': 'Contact Tech ERROR', 'err': e}))
        return test_pass


def get_days_month_year(days_value=0):


    def get_attr_repr(val,attr):
        if not val:
            return ""
        repr = (str(attr)+"s") if val > 1 else attr
        return str(val) + repr

    if not days_value or not isinstance(days_value, int):
        return ""

    years, remain = divmod(days_value, 365)
    months, days = divmod(remain, 30)
    return "-".join(filter(None,[get_attr_repr(years,"year"),\
                                 get_attr_repr(months,"month"),get_attr_repr(days,'day')]))





