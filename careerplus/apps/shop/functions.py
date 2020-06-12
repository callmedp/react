import os
import time
from django.core.exceptions import ValidationError
from random import random
from django.utils.translation import ugettext_lazy as _
import csv
import logging

def get_file_name(f_obj):
    file_name_tuple = os.path.splitext(f_obj)
    extention = file_name_tuple[len(
        file_name_tuple)-1] if len(file_name_tuple) > 1 else ''
    file_name = str(int(time.time())) + '_' + str(int(random()*9999)) + \
        extention
    return file_name


def get_upload_path_faculty(instance, filename):
    return "faculty/{faculty_id}/{filename}".format(
        faculty_id=instance.id, filename=get_file_name(filename))


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


def get_upload_path_badge_file(instance, filename):
    return "badge_file/{ven_id}/{filename}".format(
        ven_id=instance.id, filename=get_file_name(filename))

def get_upload_path_mobile_banner_file(instance, filename):
    return "badge_file/{ven_id}/{filename}".format(
        ven_id=instance.id, filename=get_file_name(filename))

def get_upload_path_feature_profile_file(instance, filename):
    return "featured_profile/{feature_id}/{filename}".format(
        feature_id=instance.id, filename=get_file_name(filename))

def get_upload_path_product_subsection_icon(instance, filename):
    return "section/subsection/product/{filename}".format(filename=get_file_name(filename))


def get_mobile_upload_path_product_subsection_icon(instance, filename):
    return "section/subsection/mobile/product/{filename}".format(filename=get_file_name(filename))

def get_upload_path_product_section_image(instance, filename):
    return "section/product/{filename}".format(filename=get_file_name(filename))

def get_upload_path_product_offer_icon(instance, filename):
    return "offer/{id}/product/{filename}".format(filename=get_file_name(filename),id=instance.id)


def upload_FA(filename):
    from .models import FunctionalArea, Product, ProductFA
    csvfile = open(filename)
    mapping_dict = csv.DictReader(csvfile)
    for d in mapping_dict:
        product = Product.objects.filter(cpv_id=d['VARIATION ID(OLD)'])
        if product:
            product = product[0]
            for i in range(1, 4):
                faname = d['Shine FA{}'.format(i)]
                if faname not in ['', 'ALL']:
                    try:
                        int(faname)
                    except Exception as e:
                        logging.getLogger('error_log').error(str(e))
                        try:
                            faobj = FunctionalArea.objects.get_or_create(name=faname)
                            ProductFA.objects.get_or_create(product=product, fa=faobj[0])
                        except Exception as e:
                            print("Failed @ {},{},{},{}".format(product.id, faname, product.name, e))
        else:
            print('Failed. Product not found @ {},{}'.format(d['PRODUCT NAME(OLD)'], d['VARIATION ID(OLD)']))

def upload_Skill(filename):
    from .models import Skill, Product, ProductSkill
    csvfile = open(filename)
    mapping_dict = csv.DictReader(csvfile)
    for d in mapping_dict:
        product = Product.objects.filter(name__iexact=d['Variation ID'])
        if product:
            product = product[0]
            for i in range(1, 253):
                skill = d['Skill{}'.format(i)]
                if skill not in ['', 'ALL']:
                    try:
                        int(skill)
                    except Exception as e:
                        logging.getLogger('error_log').error(str(e))
                        try:
                            faobj = Skill.objects.get_or_create(name=skill)
                            ProductSkill.objects.get_or_create(product=product, skill=faobj[0])
                        except Exception as e:
                            print("Failed @ {},{},{},{}".format(product.id, skill, product.name, e))
        else:
            print('Failed. Product not found @ {}'.format(d['Product name']))


def get_upload_path_for_sample_certicate(instance, filename):
    return "university_courses/sample_certificates/{pr_id}/{filename}".format(
        pr_id=instance.id, filename=get_file_name(filename))
