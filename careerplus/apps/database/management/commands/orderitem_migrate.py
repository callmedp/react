# import MySQLdb
# import json
# import pandas as pd
# import numpy as np
# from decimal import Decimal
# from django.utils import timezone
# from datetime import datetime
# from django.conf import settings
# from django.core.management.base import BaseCommand
# from django.db import IntegrityError, transaction
# from django.contrib.contenttypes.models import ContentType
# # from database.models import CPUser
# from shop.models import Product

# class Command(BaseCommand):
#     help = ('Get User Database from old Careerplus')

#     def handle(self, *args, **options):
#         db_settings=settings.DATABASES.get('oldDB')
#         db_host = db_settings.get('HOST')
#         if db_host is '':
#             db_host = "localhost"
#         db_name = db_settings.get('NAME')
#         db_pwd = db_settings.get('PASSWORD')
#         db_user = db_settings.get('USER')
#         db = MySQLdb.connect(db_host,db_user,db_pwd,db_name)
        
#         db2_settings=settings.DATABASES.get('default')
#         db2_host = db2_settings.get('HOST')
#         if db2_host is '':
#             db2_host = "localhost"
#         db2_name = db2_settings.get('NAME')
#         db2_pwd = db2_settings.get('PASSWORD')
#         db2_user = db2_settings.get('USER')
#         db2 = MySQLdb.connect(db2_host,db2_user,db2_pwd,db2_name, autocommit=True)

#         print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#         print( 'Fetching Migrated Order')
#         print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        
#         def flow_map(row):
#             if row['addon_id'] and row['addon_id']== row['addon_id']:
#                 return product_flow_dict.get(row['addon_id'], None)
#             elif row['variation_id'] and row['variation_id'] == row['variation_id']:
#                 return product_flow_variation_dict.get(row['variation_id'], None)
#             elif row['product_id'] and row['product_id'] == row['product_id']:
#                 return product_flow_dict.get(row['product_id'], None)
#             return None
        
#         def map_oi_status(flow, otype, new_status):
#             # new_status 
#             oi_status, last_oi_status, counter, feedback = 0, 0, 1, False
#             if flow in [1, 3, 5, 12, 13]:
#                 if otype == 0:
#                     oi_status = 2
#                     last_oi_status = 1
#                     counter = 0
#                     feedback = False
#                 elif otype in [1,8]:
#                     oi_status = 5
#                     last_oi_status = 2
#                     counter = 0
#                     feedback = False
#                 elif otype == 2:
#                     oi_status = 24
#                     last_oi_status = 24
#                     counter = 1
#                     feedback = False
#                 elif otype == 3:
#                     oi_status = 24
#                     last_oi_status = 24
#                     counter = 2
#                     feedback = False
#                 elif otype == 4:
#                     oi_status = 4
#                     last_oi_status = 24
#                     counter = 2
#                     feedback = False
#                 elif otype == 5:
#                     oi_status = 25
#                     last_oi_status = 25
#                     counter = 1
#                     feedback = True
#                 elif otype in [6,13]:
#                     oi_status = 26
#                     last_oi_status = 26
#                     counter = 1
#                     feedback = True
#                 elif otype == 7:
#                     oi_status = 23
#                     last_oi_status = 23
#                     counter = 1
#                     feedback = True
#                 else:
#                     oi_status = 4
#                     last_oi_status = 4
#                     counter = 0
#                     feedback = False
#             elif flow in [2, 10, 11]:
#                 if otype :
#                     oi_status = 4
#                     last_oi_status = 6
#                     counter = 0
#                     feedback = True
#                 else:
#                     oi_status = 5
#                     last_oi_status = 0
#                     counter = 0
#                     feedback = False
#             elif flow == 4:
#                 if otype in [0]:
#                     oi_status = 2
#                     last_oi_status = 2
#                     counter = 0
#                     feedback = False
#                 if otype in [1,8]:
#                     oi_status = 5
#                     last_oi_status = 5
#                     counter = 0
#                     feedback = False
#                 elif otype in [5,6]:
#                     oi_status = 25
#                     last_oi_status = 5
#                     counter = 0
#                     feedback = True
#                 elif otype == 7:
#                     oi_status = 23
#                     last_oi_status = 5
#                     counter = 0
#                     feedback = True
#                 else:
#                     oi_status = 4
#                     last_oi_status = 4
#                     counter = 0
#                     feedback = True
#             elif flow == 6:
#                 if otype in [4,10,11,12]:
#                     oi_status = 4
#                     last_oi_status = 4
#                     counter = 0
#                     feedback = True
#                 elif otype in [14]:
#                     oi_status = 81
#                     last_oi_status = 82
#                     counter = 0
#                     feedback = True
#                 else:
#                     oi_status = 82
#                     last_oi_status = 1
#                     counter = 0
#                     feedback = False
#             elif flow == 7:
#                 if otype in [4,9]:
#                     oi_status = 4
#                     last_oi_status = 62
#                     counter = 0
#                     feedback = True
#                 elif otype == 5:
#                     oi_status = 25
#                     last_oi_status = 25
#                     counter = 1
#                     feedback = True
#                 elif otype in [6,13]:
#                     oi_status = 25
#                     last_oi_status = 25
#                     counter = 1
#                     feedback = True
#                 elif otype == 7:
#                     oi_status = 23
#                     last_oi_status = 23
#                     counter = 1
#                     feedback = True
#                 else:
#                     oi_status = 5
#                     last_oi_status = 1
#                     counter = 0
#                     feedback = False
#             elif flow == 8:
#                 if otype in [0,1]:
#                     oi_status = 49
#                     last_oi_status = 2
#                     counter = 0
#                     feedback = False
#                 elif otype == 8:
#                     oi_status = 42
#                     last_oi_status = 49
#                     counter = 0
#                     feedback = False
#                 elif otype == 2:
#                     oi_status = 46
#                     last_oi_status = 45
#                     counter = 1
#                     feedback = False
#                 elif otype == 3:
#                     oi_status = 46
#                     last_oi_status = 45
#                     counter = 2
#                     feedback = False
#                 elif otype == 5:
#                     oi_status = 47
#                     last_oi_status = 45
#                     counter = 1
#                     feedback = True
#                 elif otype in [6,13]:
#                     oi_status = 48
#                     last_oi_status = 44
#                     counter = 1
#                     feedback = True
#                 elif otype == 7:
#                     oi_status = 45
#                     last_oi_status = 45
#                     counter = 1
#                     feedback = True
#                 else:
#                     oi_status = 4
#                     last_oi_status = 4
#                     counter = 3
#                     feedback = False
#             elif flow == 9:
#                 if otype == 4:
#                     oi_status = 4
#                     last_oi_status = 143
#                     counter = 0
#                     feedback = True
#                 else:
#                     oi_status = 5
#                     last_oi_status = 0
#                     counter = 0
#                     feedback = False
            
#             return oi_status, last_oi_status, counter, feedback

#         sql = """
#                 SELECT 
#                     cart_orderitem.id, cart_orderitem.order_id, cart_orderitem.name, cart_orderitem.price, cart_orderitem.product_id, 
#                     cart_orderitem.variation_id, cart_orderitem.parent_id, cart_orderitem.addon_id, cart_orderitem.combo_id, 
#                     cart_orderitem.units, cart_orderitem.waybill, cart_orderitem.vendor_coupon, cart_orderitem.service_provider, 
#                     cart_orderitem.added_on, cart_orderitem.modified_on, cart_orderitem.expires_on, cart_orderitem.has_discount_id, 
#                     cart_orderitem.oio_resume, cart_orderitem.oio_linkedin_id, cart_orderitem.oio_operation_type, 
#                     cart_orderitem.oio_rating, cart_orderitem.oio_assigned_by_id, cart_orderitem.oio_assigned_to_id, 
#                     cart_orderitem.oio_added_on, cart_orderitem.oio_modified_on, cart_orderitem.oio_lock, cart_orderitem.feedback_date, 
#                     cart_orderitem.closed_date, cart_orderitem.oi_flow_status, cart_orderitem.tat_date, cart_orderitem.new_status, 
#                     cart_orderitem.status_flag, cart_orderitem.midout_sent_on, cart_orderitem.complain_counter, cart_orderitem.deduct_slab_id, 
#                     cart_orderitem.net_payable_allocation, cart_orderitem.on_hold 
#                 FROM cart_orderitem 
#                 INNER JOIN cart_order 
#                 ON ( cart_orderitem.order_id = cart_order.id ) WHERE cart_order.id IN (939911, 941833, 941927, 941935, 941949, 941951, 941953, 941955, 941957, 941989, 941991, 941997, 942003, 942015, 942021, 942029, 942041, 942043, 942045, 942095, 942107, 942129, 942157, 942189, 942191, 942193, 942205, 942223, 942243, 942249, 942253, 942265, 942269, 942275, 942299, 942303, 942307, 942317, 942321, 942331, 941975, 942229, 942231)  
#                 ORDER BY cart_orderitem.added_on DESC
#                 """
#         db2 = MySQLdb.connect(db2_host,db2_user,db2_pwd,db2_name, autocommit=True)
#         db = MySQLdb.connect(db_host,db_user,db_pwd,db_name)
        
#         oi_df = pd.read_sql(sql,con=db)
                
#         new_order_df = pd.read_sql('SELECT id AS order_obj, co_id as order_id  from order_order', con=db2)
        
#         oi_df = pd.merge(oi_df, new_order_df, how='left', on='order_id')
#         oi_df = oi_df[~oi_df.order_obj.isnull()]    
#         print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#         print( 'Merging Order')
#         print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#         db2 = MySQLdb.connect(db2_host,db2_user,db2_pwd,db2_name, autocommit=True)
#         db = MySQLdb.connect(db_host,db_user,db_pwd,db_name)
        
#         staff_user_df = pd.read_sql('SELECT id as staff_obj, cp_id as user_id FROM users_user', con=db2)
#         staff_user_df.user_id = pd.to_numeric(staff_user_df.user_id)
#         staff_user_df.staff_obj = pd.to_numeric(staff_user_df.staff_obj)
        
#         staff_user_df = staff_user_df.dropna()
#         staff_user_df = staff_user_df.set_index('user_id')['staff_obj'].to_dict()
        

#         db2 = MySQLdb.connect(db2_host,db2_user,db2_pwd,db2_name, autocommit=True)
#         db = MySQLdb.connect(db_host,db_user,db_pwd,db_name)
        
#         product_df = pd.read_sql('SELECT id as product_obj, cp_id as pid, cpv_id as pvid, type_flow FROM shop_product', con=db2)
#         product_variation_df = product_df[~product_df.pvid.isnull()]
        

#         product_dict = product_df.set_index('pid')['product_obj'].to_dict()
#         product_variation_dict = product_variation_df.set_index('pvid')['product_obj'].to_dict()
        
#         product_flow_dict = product_df.set_index('product_obj')['type_flow'].to_dict()
#         product_flow_variation_dict = product_variation_df.set_index('product_obj')['type_flow'].to_dict()
        

#         del product_variation_df
#         del product_df
#         del new_order_df
        
        
#         print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#         print( 'Merging STAFF PRODUCT FLOW')
#         print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        
#         oi_df.oio_assigned_by_id = oi_df.oio_assigned_by_id.apply(lambda x : staff_user_df.get(x, None))
#         oi_df.oio_assigned_to_id = oi_df.oio_assigned_to_id.apply(lambda x : staff_user_df.get(x, None))
#         oi_df.product_id = oi_df.product_id.apply(lambda x : product_dict.get(x, None))
#         oi_df.addon_id = oi_df.addon_id.apply(lambda x : product_dict.get(x, None))
#         oi_df.variation_id = oi_df.variation_id.apply(lambda x : product_variation_dict.get(x, None))
#         oi_df.combo_id = oi_df.combo_id.apply(lambda x : product_variation_dict.get(x, None))
#         oi_df['type_flow'] = oi_df.apply(flow_map, axis=1)
#         cursor = db2.cursor()

#         update_values = []
#         update_sql = """
#                 INSERT INTO order_orderitem 
#                 (
#                     partner_name, title, upc, quantity, oi_price_before_discounts_incl_tax, 
#                     oi_price_before_discounts_excl_tax, no_process, is_combo, is_variation,
#                     oi_status, last_oi_status, oi_resume, oi_draft, draft_counter, tat_date, waiting_for_input,
#                     closed_on, draft_added_on, approved_on, modified, assigned_by_id, assigned_to_id,
#                     oio_linkedin_id, order_id, parent_id, partner_id, product_id, user_feedback, created,
#                     is_addon, delivery_price_excl_tax, delivery_price_incl_tax, delivery_service_id,
#                     oi_flow_status, cost_price, discount_amount, selling_price,tax_amount,
#                     archive_json,coi_id, expiry_date
#                 ) VALUES
#                 (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
#                 %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
#                 %s, %s, %s, %s, %s, %s, %s, %s,%s) 
#                 """
#         print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#         print( 'Bulk Insert Start')
#         print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#         for i, row in oi_df.iterrows():
#             if row['order_obj'] and row['order_obj'] == row['order_obj']:
#                 is_combo = False,
#                 is_variation = False,
#                 is_addon = False
#                 product_id = row['product_id'] if row['product_id'] and row['product_id'] == row['product_id'] else None
#                 if row['combo_id'] and row['combo_id'] == row['combo_id']:
#                     is_combo = True

#                 if row['addon_id'] and row['addon_id']== row['addon_id']:
#                     is_addon = True
#                     product_id = row['addon_id']
                
#                 elif row['variation_id'] and row['variation_id'] == row['variation_id']:
#                     is_variation = True
#                     product_id = row['variation_id']
                
#                 oi_status, last_oi_status, counter, feedback = map_oi_status(row['type_flow'], row['oio_operation_type'], row['new_status'])
#                 assigned_to = None
#                 if oi_status not in [2]:
#                     assigned_to = row['oio_assigned_to_id'] if row['oio_assigned_to_id'] and row['oio_assigned_to_id'] == row['oio_assigned_to_id'] else None
#                 data_tup = (
#                         '',
#                         row['name'] if row['name'] and row['name'] == row['name'] else None,
#                         product_id,
#                         row['units'],
#                         Decimal(0),
#                         Decimal(0),
#                         False,
#                         is_combo,
#                         is_variation,
#                         oi_status,
#                         last_oi_status,
#                         row['oio_resume'] if row['oio_resume'] and row['oio_resume'] == row['oio_resume'] else None,
#                         row['oio_resume'] if row['oio_resume'] and row['oio_resume'] == row['oio_resume'] else None,
#                         counter,
#                         None,
#                         False,
#                         str(row['closed_date']) if row['closed_date'] == row['closed_date'] else None,
#                         None,
#                         None,
#                         str(row['modified_on']) if row['modified_on'] == row['modified_on'] else None,
#                         row['oio_assigned_by_id'] if row['oio_assigned_by_id'] and row['oio_assigned_by_id'] == row['oio_assigned_by_id'] else None,
#                         assigned_to,
#                         None,
#                         row['order_obj'],
#                         None,
#                         None,
#                         product_id,
#                         feedback,
#                         str(row['added_on']) if row['added_on'] == row['added_on'] else None,
#                         is_addon,
#                         Decimal(0),
#                         Decimal(0),
#                         None,
#                         row['oi_flow_status'] if row['oi_flow_status'] == row['oi_flow_status'] else 0,
#                         row['price'] if row['price'] and row['price'] == row['price'] else Decimal(0),
#                         Decimal(0),
#                         row['price'] if row['price'] and row['price'] == row['price'] else Decimal(0),
#                         Decimal(0),
#                         str(dict(row.to_dict())),
#                         row['id'],
#                         str(row['expires_on']) if row['expires_on'] == row['expires_on'] else None,
#                         )
#                 update_values.append(data_tup)    
#             if len(update_values) > 5000:
                
#                 print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#                 print( 'Bulk Insert ' + str(i))
#                 print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#                 cursor.executemany(update_sql, update_values)
#                 update_values = []
                
#         if update_values:
#             cursor.executemany(update_sql, update_values)
#             update_values = []
#         cursor.close()
#         cursor = db2.cursor()

#         print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#         print( 'Bulk Update Parent Order Items')
#         print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#         db2 = MySQLdb.connect(db2_host,db2_user,db2_pwd,db2_name, autocommit=True)
#         db = MySQLdb.connect(db_host,db_user,db_pwd,db_name)
        
#         new_order_item_df = pd.read_sql('SELECT id as new_parent_id, coi_id as parent_id FROM order_orderitem',con=db2)
#         new_order_item_df = new_order_item_df[new_order_item_df.parent_id.notnull()]
#         oi_df = pd.merge(oi_df, new_order_item_df, how='left', on='parent_id')
#         new_order_item_df = new_order_item_df.rename(columns={'new_parent_id': 'new_id', 'parent_id': 'id'})
#         oi_df = pd.merge(oi_df, new_order_item_df, how='left', on='id')

#         del new_order_item_df
#         coi_list = []
#         parent_id_list = []
#         for i, row in oi_df[~oi_df.new_parent_id.isnull()].iterrows():
#             coi_list.append(' WHEN {0} THEN {1} '.format(row['new_id'], row['new_parent_id']))
#             parent_id_list.append(str(row['new_id']))
#             if len(parent_id_list) > 5000:
#                 update_sql = '''
#                     UPDATE order_orderitem SET parent_id = (
#                     CASE id 
#                         {0}
#                     END) WHERE id IN ({1});
#                     '''.format(' '.join(coi_list), ', '.join(parent_id_list))
#                 print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#                 print( 'Bulk Update ' + str(i))
#                 print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
                
#                 db2.query(update_sql)
#                 update_sql = ''
#                 parent_id_list = []
#                 coi_list = []
#         if len(parent_id_list):
#             update_sql = '''
#                     UPDATE order_orderitem SET parent_id = (
#                     CASE id 
#                         {0}
#                     END) WHERE id IN ({1});
#                     '''.format(' '.join(coi_list), ', '.join(parent_id_list))
#             db2.query(update_sql)
#             update_sql = ''
#             parent_id_list = []
#             coi_list = []

#         print('Parent Order Items Migrated')
        
#         pass