import os
import time
from django.core.exceptions import ValidationError
from random import random
from django.utils.translation import ugettext_lazy as _


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



    