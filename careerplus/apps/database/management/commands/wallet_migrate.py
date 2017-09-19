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
        sql = """
                SELECT cart_order.id, auth_user.email as Email,  
                cart_order.transaction_id, cart_order.currency, cart_order.instrument_number, 
                cart_order.instrument_issuer, cart_order.instrument_issue_date, cart_order.added_on, 
                cart_order.modified_on, cart_order.closed_on, cart_order.status, 
                cart_order.payment_mode, cart_order.payment_date, cart_order.vendor, 
                cart_order.amount_payable, cart_order.total, 
                cart_order.coupon_discount, cart_order.convenience_charges,
                coupon_coupon.code as coupon,
                cart_order.coupon_id,
                cart_order.welcome_call, 
                cart_order.extra_info, theme_country.country_code as code2,  
                cart_order.order_mobile,  
                cart_order.flat_discount, cart_order.invoice_file,
                cart_order.wallettransaction_id,
                cart_order.wallettransaction_redeem_id,
                cart_order.wallet_cashback

                FROM cart_order 
                LEFT JOIN theme_country
                ON cart_order.country_id = theme_country.id
                LEFT JOIN coupon_coupon
                ON cart_order.coupon_id = coupon_coupon.code
                LEFT JOIN auth_user
                ON cart_order.candidate_id = auth_user.id
                WHERE (cart_order.added_on >= '2014-04-1 00:00:00' AND cart_order.candidate_id IS NOT NULL);
            """
        wallet_df = pd.read_sql(sql, con=db)
        print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        print( 'Mysql order select done')
        print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        