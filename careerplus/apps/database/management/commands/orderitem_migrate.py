import MySQLdb
import json
import pandas as pd
import numpy as np
from decimal import Decimal
from django.utils import timezone
from datetime import datetime
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import IntegrityError, transaction
from django.contrib.contenttypes.models import ContentType
from database.models import CPUser
from shop.models import Product

class Command(BaseCommand):
    help = ('Get User Database from old Careerplus')

    def handle(self, *args, **options):
        db_settings=settings.DATABASES.get('oldDB')
        db_host = db_settings.get('HOST')
        if db_host is '':
            db_host = "localhost"
        db_name = db_settings.get('NAME')
        db_pwd = db_settings.get('PASSWORD')
        db_user = db_settings.get('USER')
        db = MySQLdb.connect(db_host,db_user,db_pwd,db_name)
        
        db2_settings=settings.DATABASES.get('default')
        db2_host = db2_settings.get('HOST')
        if db2_host is '':
            db2_host = "localhost"
        db2_name = db2_settings.get('NAME')
        db2_pwd = db2_settings.get('PASSWORD')
        db2_user = db2_settings.get('USER')
        db2 = MySQLdb.connect(db2_host,db2_user,db2_pwd,db2_name, autocommit=True)

        print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        print( 'Fetching Migrated Order')
        print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        new_order_df = pd.read_sql('SELECT id AS order_obj, co_id as id  from order_order', con=db2)
        staff_user_df = pd.read_sql('SELECT id as staff_obj, cp_id as id FROM users_user', con=db2)
        product_df = pd.read_sql('SELECT id as product_obj, cp_id as pid, cpv_id as pvid FROM shop_product', con=db2)
        import ipdb;ipdb.set_trace()
        pass