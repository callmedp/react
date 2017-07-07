import os
import time
from django.core.exceptions import ValidationError
from random import random


def get_file_name(f_obj):
    file_name_tuple = os.path.splitext(f_obj)
    extention = file_name_tuple[len(
        file_name_tuple)-1] if len(file_name_tuple) > 1 else ''
    file_name = str(int(time.time())) + '_' + str(int(random()*9999)) + \
        extention
    return file_name


def get_upload_path_category(instance, filename):
    return "category/{cat_id}/{filename}".format(
        cat_id=instance.id, filename=get_file_name(filename))


def get_upload_path_product_image(instance, filename):
    return "product_image/{pr_id}/{filename}".format(
        pr_id=instance.id, filename=get_file_name(filename))


def get_upload_path_product_icon(instance, filename):
    return "product_icon/{pr_id}/{filename}".format(
        pr_id=instance.id, filename=get_file_name(filename))


def get_upload_path_product_banner(instance, filename):
    return "product_banner/{pr_id}/{filename}".format(
        pr_id=instance.id, filename=get_file_name(filename))


def get_upload_path_product_file(instance, filename):
    return "product_file/{pr_id}/{filename}".format(
        pr_id=instance.id, filename=get_file_name(filename))


def get_upload_path_vendor(instance, filename):
    return "vendor/{ven_id}/{filename}".format(
        ven_id=instance.id, filename=get_file_name(filename))


from django.utils.translation import ugettext_lazy as _


class ScreenProductAttributesContainer(object):

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
                'obj': self.product.get_product_class(), 'attr': name})

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
        return self.product.screenattributes.all()

    def get_value_by_attribute(self, attribute):
        return self.get_values().get(attribute=attribute)

    def get_all_attributes(self):
        return self.product.get_product_class().attributes.filter(active=True)

    def get_attribute_by_name(self, name):
        return self.get_all_attributes().get(name=name)

    def __iter__(self):
        return iter(self.get_values())

    def save(self):
        for attribute in self.get_all_attributes():
            if hasattr(self, attribute.name):
                value = getattr(self, attribute.name)
                attribute.save_screen_value(self.product, value)

        
