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
        
        sql = """
                SELECT 
                    cart_orderitem.id, cart_orderitem.order_id, cart_orderitem.name, cart_orderitem.price, cart_orderitem.product_id, 
                    cart_orderitem.variation_id, cart_orderitem.parent_id, cart_orderitem.addon_id, cart_orderitem.combo_id, 
                    cart_orderitem.units, cart_orderitem.waybill, cart_orderitem.vendor_coupon, cart_orderitem.service_provider, 
                    cart_orderitem.added_on, cart_orderitem.modified_on, cart_orderitem.expires_on, cart_orderitem.has_discount_id, 
                    cart_orderitem.oio_resume, cart_orderitem.oio_linkedin_id, cart_orderitem.oio_operation_type, 
                    cart_orderitem.oio_rating, cart_orderitem.oio_assigned_by_id, cart_orderitem.oio_assigned_to_id, 
                    cart_orderitem.oio_added_on, cart_orderitem.oio_modified_on, cart_orderitem.oio_lock, cart_orderitem.feedback_date, 
                    cart_orderitem.closed_date, cart_orderitem.oi_flow_status, cart_orderitem.tat_date, cart_orderitem.new_status, 
                    cart_orderitem.status_flag, cart_orderitem.midout_sent_on, cart_orderitem.complain_counter, cart_orderitem.deduct_slab_id, 
                    cart_orderitem.net_payable_allocation, cart_orderitem.on_hold 
                FROM cart_orderitem 
                INNER JOIN cart_order 
                ON ( cart_orderitem.order_id = cart_order.id ) WHERE cart_order.added_on >= '2014-04-01 00:00:00'  
                ORDER BY cart_orderitem.added_on DESC
                """
        import ipdb;ipdb.set_trace()
        oi_df = pd.read_sql(sql,con=db)
                
        new_order_df = pd.read_sql('SELECT id AS order_obj, co_id as order_id  from order_order', con=db2)
        oi_df = pd.merge(oi_df, new_order_df, how='left', on='order_id')
        oi_df = oi_df[~oi_df.order_obj.isnull()]    
        
        staff_user_df = pd.read_sql('SELECT id as staff_obj, cp_id as user_id FROM users_user', con=db2)
        staff_user_df.user_id = pd.to_numeric(staff_user_df.user_id)
        staff_user_df.staff_obj = pd.to_numeric(staff_user_df.staff_obj)
        
        staff_user_df = staff_user_df.dropna()
        staff_user_df = staff_user_df.set_index('user_id')['staff_obj'].to_dict()



        product_df = pd.read_sql('SELECT id as product_obj, cp_id as pid, cpv_id as pvid, type_flow FROM shop_product', con=db2)
        product_variation_df = product_df[~product_df.pvid.isnull()]
        

        product_dict = product_df.set_index('pid')['product_obj'].to_dict()
        product_variation_dict = product_variation_df.set_index('pvid')['product_obj'].to_dict()
        
        product_flow_dict = product_df.set_index('pid')['type_flow'].to_dict()
        product_flow_variation_dict = product_variation_df.set_index('pvid')['type_flow'].to_dict()
        

        del product_variation_df
        del product_df
        def flow_map(row):
            print(row)
            return 1

        oi_df.oio_assigned_by_id = oi_df.oio_assigned_by_id.apply(lambda x : staff_user_df.get(x, None))
        oi_df.oio_assigned_to_id = oi_df.oio_assigned_to_id.apply(lambda x : staff_user_df.get(x, None))
        oi_df.product_id = oi_df.product_id.apply(lambda x : product_dict.get(x, None))
        oi_df.addon_id = oi_df.addon_id.apply(lambda x : product_dict.get(x, None))
        oi_df.variation_id = oi_df.variation_id.apply(lambda x : product_variation_dict.get(x, None))
        oi_df.combo_id = oi_df.combo_id.apply(lambda x : product_variation_dict.get(x, None))
        oi_df['type_flow'] = oi_df.apply(flow_map, axis=1)


        pass