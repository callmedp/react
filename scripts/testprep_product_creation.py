import logging
import json
from decimal import Decimal
import xlrd

import sys,os,django

#Settings imports
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "careerplus.config.settings_staging")
ROOT_FOLDER = os.path.realpath(os.path.dirname(__file__))
ROOT_FOLDER = ROOT_FOLDER[:ROOT_FOLDER.rindex('/')]
if ROOT_FOLDER not in sys.path:
    sys.path.insert(1, ROOT_FOLDER + '/')
django.setup()



from shop.models import *
from partner.models import Vendor , ProductSkill
from shop.utils import ProductModeration
from requests.models import Request

from django.utils.text import slugify


if __name__ == "__main__":
    default_category = 'testprep'
    file_path = sys.argv[1:]
    if not file_path:
        print('Enter the file path to read')
        sys.exit()

    file_path = file_path[0]

    try:
        file_data = xlrd.open_workbook(file_path)
        file_data = file_data.sheet_by_index(0)
    except:
        print('unable to read file ')
        sys.exit()
    request = Request()
    pm = ProductModeration()
    product_class = ProductClass.objects.only('id').get(slug='assessment')
    vendor = Vendor.objects.get_or_create(name='testprep')[0]
    setattr(request, "user", vendor)
    for i in range(1,file_data.nrows):
        print('reading line {}'.format(i))
        data = file_data.row_values(i)
        name = data[0]
        upc = int(data[2])
        cat = data[4]
        about = data[5]
        no_of_question = data[6]
        duration =data[7]
        price = data[8]
        if not price:
            print('price cannot be empty')
            sys.exit()
        price = Decimal(price)
        skill = data[10]
        print('creating product screen')

        prodscreen = ProductScreen.objects.get_or_create(product_class=product_class,vendor=vendor,name=name,upc=upc,
                                                type_flow=16,
                                          sub_type_flow=1602,about=about,inr_price=price)[0]

        print('product screen created ,{}'.format(prodscreen.id))

        test_duration_attr = Attribute.objects.only('id','name').filter(name='test_duration').first()
        if not test_duration_attr:
            print('unable to set test duration')
            sys.exit()
        number_of_questions_attr = Attribute.objects.only('id','name').filter(name='number_of_questions').first()

        ProductAttributeScreen.objects.get_or_create(attribute=test_duration_attr,value_integer=duration,
                                                  product=prodscreen,
                                              active=True)
        ProductAttributeScreen.objects.get_or_create(attribute=number_of_questions_attr,value_integer=no_of_question,
                                              product=prodscreen,active=True)
        product = prodscreen.create_product()

        if not product.is_indexed:
            product,prodscreen,copy= pm.copy_to_product(request,product,prodscreen)
            print(copy)
            print('product is created , {}'.format(product.id))

        if skill:
            skill = skill.strip().split(',')
        else:
            skill = []

        primary_cat  = True
        skill = list(map(lambda x: x.strip(), skill))

        for sk in skill:
            print(sk)
            try:
                s, _ = Skill.objects.get_or_create(name=sk)
            except:
                print('s')
                s = Skill.objects.get(slug=slugify(name))
            category = Category.objects.only('id','name','type_level').filter(name__iexact=sk,type_level=3).first()
            if not category:
                category, created =Category.objects.get_or_create(name=default_category,type_level=3,active=True)
                # continue
            ProductCategory.objects.get_or_create(category=category,product=product)
            primary_cat = False
            ProductSkill.objects.get_or_create(skill=s,product=product,third_party_skill_id=upc)

        if not product.is_indexed:
            product.is_indexed=True
            product.active=True
            product.visible_on_crm = False
            product.is_indexable=True
            product.save()
        else:
            print('product is already indexed')


    print('complete')
    



