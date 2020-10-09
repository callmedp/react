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

#         def flow_map(row):
#             if row['addon_id'] and row['addon_id']== row['addon_id']:
#                 return product_flow_dict.get(row['addon_id'], None)
#             elif row['variation_id'] and row['variation_id'] == row['variation_id']:
#                 return product_flow_variation_dict.get(row['variation_id'], None)
#             elif row['product_id'] and row['product_id'] == row['product_id']:
#                 return product_flow_dict.get(row['product_id'], None)
#             return None
#         def map_oi_status(flow, otype, new_status):
#             new_status = not new_status
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
#                 SELECT cart_orderitemoperation.id, cart_orderitemoperation.order_item_id, 
#                 cart_orderitemoperation.resume, cart_orderitemoperation.linkedin_id, 
#                 cart_orderitemoperation.operation_type, cart_orderitemoperation.rating, 
#                 cart_orderitemoperation.assigned_by_id, cart_orderitemoperation.assigned_to_id, 
#                 cart_orderitemoperation.added_on, cart_orderitemoperation.modified_on, 
#                 cart_orderitemoperation.operation_changed_from 
#                 FROM cart_orderitemoperation 
#                 INNER JOIN cart_orderitem 
#                 ON ( cart_orderitemoperation.order_item_id = cart_orderitem.id ) 
#                 INNER JOIN cart_order 
#                 ON ( cart_orderitem.order_id = cart_order.id ) 
#                 WHERE cart_order.id IN (939911, 941833, 941927, 941935, 941949, 941951, 941953, 941955, 941957, 941989, 941991, 941997, 942003, 942015, 942021, 942029, 942041, 942043, 942045, 942095, 942107, 942129, 942157, 942189, 942191, 942193, 942205, 942223, 942243, 942249, 942253, 942265, 942269, 942275, 942299, 942303, 942307, 942317, 942321, 942331, 941975, 942229, 942231)   
#                 ORDER BY cart_orderitemoperation.added_on DESC;
#             """
#         db2 = MySQLdb.connect(db2_host,db2_user,db2_pwd,db2_name, autocommit=True)
#         db = MySQLdb.connect(db_host,db_user,db_pwd,db_name)
        
#         oio_df = pd.read_sql(sql,con=db)
#         print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#         print( 'Fetching Migrated OrderItem')
#         print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
           
#         new_order_item_df = pd.read_sql(
#             'SELECT order_orderitem.id as new_oi_id, order_orderitem.coi_id as order_item_id, order_orderitem.product_id, shop_product.type_flow FROM order_orderitem LEFT JOIN shop_product ON order_orderitem.product_id = shop_product.id;',con=db2)
#         print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#         print( 'Merging OrderItem')
#         print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        
#         oio_df = pd.merge(oio_df, new_order_item_df, how='left', on='order_item_id')
#         oio_df = oio_df[~oio_df.new_oi_id.isnull()]    
#         print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#         print( 'Merging Staff user OrderItem')
#         print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#         db2 = MySQLdb.connect(db2_host,db2_user,db2_pwd,db2_name, autocommit=True)
#         db = MySQLdb.connect(db_host,db_user,db_pwd,db_name)
        
#         staff_user_df = pd.read_sql('SELECT id as staff_obj, cp_id as user_id FROM users_user', con=db2)
#         staff_user_df.user_id = pd.to_numeric(staff_user_df.user_id)
#         staff_user_df.staff_obj = pd.to_numeric(staff_user_df.staff_obj)
        
#         staff_user_df = staff_user_df.dropna()
#         staff_user_df = staff_user_df.set_index('user_id')['staff_obj'].to_dict()
        

#         del new_order_item_df
        
        
        
#         oio_df.assigned_by_id = oio_df.assigned_by_id.apply(lambda x : staff_user_df.get(x, None))
#         oio_df.assigned_to_id = oio_df.assigned_to_id.apply(lambda x : staff_user_df.get(x, None))
#         cursor = db2.cursor()

#         update_values = []
#         update_sql = """
#                 INSERT INTO order_orderitemoperation 
#                 (
#                     created, modified, oi_resume, oi_draft, draft_counter,
#                     oi_status, last_oi_status, added_by_id, assigned_to_id,
#                     linkedin_id, oi_id, coio_id
#                 ) VALUES
#                 (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
#                 """
#         print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#         print( 'Bulk Insert Start')
#         print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        
#         for i, row in oio_df.iterrows():
#             if row['new_oi_id'] and row['new_oi_id'] == row['new_oi_id']:
#                 oi_status, last_oi_status, counter, feedback = map_oi_status(row['type_flow'], row['operation_type'], True)

#                 data_tup = (
#                         str(row['added_on']) if row['added_on'] == row['added_on'] else None,
#                         str(row['modified_on']) if row['modified_on'] == row['modified_on'] else None,
#                         row['resume'] if row['resume'] and row['resume'] == row['resume'] else None,
#                         row['resume'] if row['resume'] and row['resume'] == row['resume'] else None,
#                         counter,
#                         oi_status,
#                         last_oi_status,
#                         row['assigned_by_id'] if row['assigned_by_id'] and row['assigned_by_id'] == row['assigned_by_id'] else None,
#                         row['assigned_to_id'] if row['assigned_to_id'] and row['assigned_to_id'] == row['assigned_to_id'] else None,
#                         None,
#                         row['new_oi_id'],
#                         row['id'],
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

#         del oio_df
#         db2 = MySQLdb.connect(db2_host,db2_user,db2_pwd,db2_name, autocommit=True)
#         db = MySQLdb.connect(db_host,db_user,db_pwd,db_name)
        
#         oio_df = pd.read_sql(
#             'SELECT id as new_oio_id, oi_id as new_oi_id, coio_id as oio_id FROM order_orderitemoperation;',con=db2)

#         sql = """
#                 SELECT cart_message.id, cart_message.from_user_id, auth_user.email as 'Email', cart_message.to_user_id, 
#                 cart_message.oio_id, cart_message.order_message, cart_message.message, 
#                 cart_message.internal, cart_message.added_on, cart_message.modified_on 
#                 FROM cart_message 
#                 INNER JOIN cart_orderitemoperation 
#                 ON ( cart_message.oio_id = cart_orderitemoperation.id ) 
#                 INNER JOIN cart_orderitem 
#                 ON ( cart_orderitemoperation.order_item_id = cart_orderitem.id ) 
#                 INNER JOIN cart_order ON ( cart_orderitem.order_id = cart_order.id ) 
#                 LEFT JOIN auth_user ON (cart_message.from_user_id = auth_user.id)
#                 WHERE cart_order.id IN (939911, 941833, 941927, 941935, 941949, 941951, 941953, 941955, 941957, 941989, 941991, 941997, 942003, 942015, 942021, 942029, 942041, 942043, 942045, 942095, 942107, 942129, 942157, 942189, 942191, 942193, 942205, 942223, 942243, 942249, 942253, 942265, 942269, 942275, 942299, 942303, 942307, 942317, 942321, 942331, 941975, 942229, 942231)  
#                 ORDER BY cart_message.added_on DESC;  
#             """
#         db2 = MySQLdb.connect(db2_host,db2_user,db2_pwd,db2_name, autocommit=True)
#         db = MySQLdb.connect(db_host,db_user,db_pwd,db_name)
        
#         msg_df = pd.read_sql(sql,con=db)
#         msg_df = pd.merge(msg_df, oio_df, how='left', on='oio_id')
#         msg_df = msg_df[~msg_df.new_oio_id.isnull()]
#         msg_df.from_user_id = msg_df.from_user_id.apply(lambda x : staff_user_df.get(x, None))
#         user_df = pd.read_csv('cleaned_present_user.csv', sep=',')
#         user_df = user_df[['Email', 'C_ID']]
#         user_df = user_df.drop_duplicates(subset=['Email'], keep='last')
        
#         user_df = user_df.set_index('Email')['C_ID'].to_dict()
#         msg_df.Email = msg_df.Email.apply(lambda x : user_df.get(x, None))
        
#         cursor = db2.cursor()

#         update_values = []
#         update_sql = """
#                 INSERT INTO order_message 
#                 (
#                     created, modified, added_by_id, candidate_id, is_internal,
#                     message, oio_id, oi_id
#                 ) VALUES
#                 (%s, %s, %s, %s, %s, %s, %s, %s) 
#                 """
#         print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#         print( 'Bulk Insert Start')
#         print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#         for i, row in msg_df.iterrows():
#             if row['new_oio_id'] and row['new_oio_id'] == row['new_oio_id']:
#                 added_by = None
#                 candidate_id = None
#                 if row['from_user_id'] and row['from_user_id'] == row['from_user_id']:
#                     added_by = row['from_user_id']
#                 else:
#                     if row['Email'] and row['Email'] == row['Email']:
#                         candidate_id = row['Email']
#                     else:
#                         candidate_id = '' 
#                 data_tup = (
#                         str(row['added_on']) if row['added_on'] == row['added_on'] else None,
#                         str(row['modified_on']) if row['modified_on'] == row['modified_on'] else None,
#                         added_by,
#                         candidate_id,
#                         row['internal'],
#                         row['message'] if row['message'] and row['message'] == row['message'] else None,
#                         row['new_oio_id'],
#                         row['new_oi_id'],
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


#         pass