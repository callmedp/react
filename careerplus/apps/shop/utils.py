from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.db import IntegrityError, transaction
from django.core import exceptions
from decimal import Decimal
from django.contrib import messages
from shop.choices import PRODUCT_VENDOR_CHOICES



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
        return self.product.product_class.attributes.filter(active=True)

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
                    if not product.name:
                        messages.error(request, "Product Name is required")
                        return test_pass
                    if not product.product_class:
                        messages.error(request, "Product Class is required")
                        return test_pass
                    if not product.upc:
                        messages.error(request, "UPC is required")
                        return test_pass
                    if not product.inr_price:
                        messages.error(request, "INR Price is required")
                        return test_pass
                    if not product.inr_price > Decimal(0):
                        messages.error(request, "INR Price is negetive")
                        return test_pass

                    if request.user.groups.filter(name='Product').exists() or request.user.is_superuser:
                        diction = [0,1, 3, 4, 5]
                    else:
                        diction = [0, 1]
                    if product.type_product in diction:
                            pass
                    else:
                        messages.error(request, "Invalid Product Choice")
                        return test_pass
                    if product.type_product in [0, 1, 3, 4]:
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
        except:
            messages.error(request, "Error Validation, Contact Product Team")
        return test_pass

    
    def validate_childs(self, request, product):
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
                            if not sibling.name:
                                messages.error(request, "Variation" + str(sibling) +" Name is required")
                                return test_pass
                            if not sibling.upc:
                                messages.error(request, "Variation" + str(sibling) +" UPC is required")
                                return test_pass
                            if not sibling.inr_price:
                                messages.error(request, "Variation" + str(sibling) +" INR Price is required")
                                return test_pass
                            if not sibling.inr_price > Decimal(0):
                                messages.error(request, "Variation" + str(sibling) +" INR Price is negetive")
                                return test_pass

                    test_pass = True
                    return test_pass
                else:
                    messages.error(request, "Object Do not Exists")
                    return test_pass
            else:
                return test_pass        
        except:
            messages.error(request, "Error Validation, Contact Product Team")
        return test_pass
    

    def validate_screenproduct(self, request, productscreen):
        test_pass = False
        try:
            if request and request.user:
                if productscreen:
                    vendor = request.user.get_vendor()
                    if not vendor:
                        messages.error(request, "Vendor is not associated")
                        return test_pass
                    if not productscreen.product:
                        messages.error(request, "Product is not associated")
                        return test_pass
                            
                    test_pass = self.validate_fields(
                        request=request, product=productscreen)
                    if productscreen.type_product == 1:
                        test_pass = self.validate_childs(
                            request=request, product=productscreen)
                else:
                    messages.error(request, "Object Do not Exists")
                    return test_pass
            else:
                return test_pass         
        except:
            pass
        return test_pass

    @transaction.atomic
    def copy_to_product(self, product, screen):
        copy = False
        import ipdb;ipdb.set_trace()
        try:
            with transaction.atomic():
                product.name = screen.name
                product.upc = screen.upc
                product.product_class = screen.product_class
                product.type_product = screen.type_product
                
                product.about = screen.about
                product.description = screen.description
                product.buy_shine = screen.buy_shine
                product.prg_structure = screen.prg_structure
                
                product.inr_price = screen.inr_price
                product.fake_inr_price = screen.fake_inr_price
                product.usd_price = screen.usd_price
                product.fake_usd_price = screen.fake_usd_price
                product.aed_price = screen.aed_price
                product.fake_aed_price = screen.fake_aed_price
                product.gbp_price = screen.gbp_price
                product.fake_gbp_price = screen.fake_gbp_price

                product.countries = screen.countries.all()
                product.save()
                for attribute in screen.attr.get_all_attributes():
                    if hasattr(screen.attr, attribute.name):
                        value = getattr(screen.attr, attribute.name)
                        attribute.save_value(product, value)
                product.save()
                
                copy = True
                return copy
                
        except IntegrityError:
            copy = False
        return copy

    @transaction.atomic
    def copy_to_screen(self, product, screen):
        copy = False
        try:
            with transaction.atomic():
                screen.name = product.name
                screen.upc = product.upc
                screen.product_class = product.product_class
                screen.type_product = product.type_product
                
                screen.about = product.about
                screen.description = product.description
                screen.buy_shine = product.buy_shine
                screen.prg_structure = product.prg_structure
                
                screen.inr_price = product.inr_price
                screen.fake_inr_price = product.fake_inr_price
                screen.usd_price = product.usd_price
                screen.fake_usd_price = product.fake_usd_price
                screen.aed_price = product.aed_price
                screen.fake_aed_price = product.fake_aed_price
                screen.gbp_price = product.gbp_price
                screen.fake_gbp_price = product.fake_gbp_price

                screen.countries = product.countries.all()

                screen.save()
                for attribute in product.attr.get_all_attributes():
                    if hasattr(product.attr, attribute.name):
                        value = getattr(product.attr, attribute.name)
                        attribute.save_screen_value(screen, value)
                screen.save()
                

                copy = True
                return copy
        
        except IntegrityError:
            copy = False
        return copy