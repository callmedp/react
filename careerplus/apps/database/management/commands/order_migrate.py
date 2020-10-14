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
        
#         db2_settings=settings.DATABASES.get('default')
#         db2_host = db2_settings.get('HOST')
#         if db2_host is '':
#             db2_host = "localhost"
#         db2_name = db2_settings.get('NAME')
#         db2_pwd = db2_settings.get('PASSWORD')
#         db2_user = db2_settings.get('USER')
#         db2 = MySQLdb.connect(db2_host,db2_user,db2_pwd,db2_name, autocommit=True)
#         db = MySQLdb.connect(db_host,db_user,db_pwd,db_name)
        
#         sql = """
#                 SELECT cart_order.id, auth_user.email as Email,  
#                 cart_order.transaction_id, cart_order.currency, cart_order.instrument_number, 
#                 cart_order.instrument_issuer, cart_order.instrument_issue_date, cart_order.added_on, 
#                 cart_order.modified_on, cart_order.closed_on, cart_order.status, 
#                 cart_order.payment_mode, cart_order.payment_date, cart_order.vendor, 
#                 cart_order.amount_payable, cart_order.total, 
#                 cart_order.coupon_discount, cart_order.convenience_charges,
#                 coupon_coupon.code as coupon,
#                 cart_order.coupon_id,
#                 cart_order.welcome_call, 
#                 cart_order.extra_info, theme_country.country_code as code2,  
#                 cart_order.order_mobile,  
#                 cart_order.flat_discount, cart_order.invoice_file,
#                 cart_order.wallettransaction_id,
#                 cart_order.wallettransaction_redeem_id,
#                 cart_order.wallet_cashback

#                 FROM cart_order 
#                 LEFT JOIN theme_country
#                 ON cart_order.country_id = theme_country.id
#                 LEFT JOIN coupon_coupon
#                 ON cart_order.coupon_id = coupon_coupon.code
#                 LEFT JOIN auth_user
#                 ON cart_order.candidate_id = auth_user.id
#                 WHERE (cart_order.id IN (939911, 941833, 941927, 941935, 941949, 941951, 941953, 941955, 941957, 941989, 941991, 941997, 942003, 942015, 942021, 942029, 942041, 942043, 942045, 942095, 942107, 942129, 942157, 942189, 942191, 942193, 942205, 942223, 942243, 942249, 942253, 942265, 942269, 942275, 942299, 942303, 942307, 942317, 942321, 942331, 941975, 942229, 942231) AND cart_order.candidate_id IS NOT NULL);
#             """
#         STATUS_MAP = {
#                 0: 0,
#                 1: 0,
#                 2: 1,
#                 5: 3,
#                 6: 0,
#                 7: 2,
#                 8: 3,
#             }
#         PAYMENT_MAP = {
#                 0: 0,
#                 1: 1,
#                 2: 2,
#                 3: 3,
#                 4: 4,
#                 5: 5,
#                 6: 6,
#                 7: 7,
#             }
#         # def clean_data(row):
#         #     row['added_on'] = str(row['added_on']) if row['added_on'] == row['added_on'] else None
#         #     row['modified_on'] = str(row['modified_on']) if row['modified_on'] == row['modified_on'] else None
#         #     row['transaction_id'] = row['transaction_id'] if row['transaction_id']  else row['id']
#         #     row['currency']  = row['currency'] if row['currency'] else 0
#         #     row['closed_on'] = str(row['closed_on']) if row['closed_on'] and row['closed_on'] == row['closed_on'] else None
#         #     row['status'] = STATUS_MAP.get(row['status'], 0)
#         #     row['payment_date'] = str(row['payment_date']) if row['payment_date'] and row['payment_date'] == row['payment_date'] else None
#         #     row['payment_mode'] = PAYMENT_MAP.get(row['payment_mode'], 0)
#         #     row['amount_payable']  = row['amount_payable'] if row['amount_payable'] else 0
#         #     row['total']  = row['total'] if row['total'] else 0
#         #     row['convenience_charges']  = row['convenience_charges'] if row['convenience_charges'] and row['convenience_charges'] == row['convenience_charges'] else 0
#         #     row['country_obj'] = int(row['country_obj']) if row['country_obj'] and row['country_obj'] == row['country_obj'] else None
#         #     row['coupon_obj'] = int(row['coupon_obj']) if row['coupon_obj'] and row['coupon_obj'] == row['coupon_obj'] else None
#         #     row['C_ID'] = row['C_ID'] if row['C_ID'] and row['C_ID'] == row['C_ID'] else None
#         #     row['']
#         #     return row
#         db2 = MySQLdb.connect(db2_host,db2_user,db2_pwd,db2_name, autocommit=True)
#         db = MySQLdb.connect(db_host,db_user,db_pwd,db_name)
        
#         order_df = pd.read_sql(sql, con=db)
#         print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#         print( 'Mysql order select done')
#         print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        
#         db2 = MySQLdb.connect(db2_host,db2_user,db2_pwd,db2_name, autocommit=True)
#         db = MySQLdb.connect(db_host,db_user,db_pwd,db_name)
        
#         country_df = pd.read_sql('SELECT id AS country_obj, code2 from geolocation_country', con=db2)
#         order_df = pd.merge(order_df,country_df, how='left', on='code2')
#         print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#         print( 'Merged Country')
#         print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        
#         del country_df
#         db2 = MySQLdb.connect(db2_host,db2_user,db2_pwd,db2_name, autocommit=True)
#         db = MySQLdb.connect(db_host,db_user,db_pwd,db_name)
        
#         coupon_df = pd.read_sql('SELECT id AS coupon_obj, code AS coupon, value AS coupon_value, coupon_type  from coupon_coupon', con=db2)
#         order_df = pd.merge(order_df, coupon_df, how='left', on='coupon')
#         print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#         print( 'Merged Coupons')
#         print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
         
#         del coupon_df
#         cursor = db2.cursor()

#         update_values = []
#         update_sql = """
#                 INSERT INTO order_order 
#                 (created, modified, number, site, candidate_id, status, currency, total_incl_tax, 
#                 total_excl_tax, date_placed, closed_on, email, country_code, mobile,
#                 country_id, invoice, payment_date, archive_json, co_id, conv_charge, welcome_call_done, paid_by_id, tax_config,
#                 crm_sales_id, crm_lead_id, sales_user_info) VALUES
#                 (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
#                 """
        
#         user_df = pd.read_csv('cleaned_present_user.csv', sep=',')
#         user_df = user_df[['Email', 'C_ID']]
#         user_df = user_df.drop_duplicates(subset=['Email'], keep='last')
        
#         order_df = pd.merge(order_df, user_df, how='left', on='Email')
#         order_df = order_df[order_df.C_ID.notnull()]
#         print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#         print( 'Merged Users')
#         print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        
#         del user_df
        
#         # print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#         # print( 'Cleaning And Mapping Start')
#         # print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#         # order_df = order_df.apply(clean_data, axis=1)
#         print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#         print( 'Bulk Insert Start')
#         print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        
#         for i, row in order_df.iterrows():
#             if row['C_ID'] and row['C_ID'] == row['C_ID']:
#                 invoice_file = row['invoice_file'] if row['invoice_file'] and row['invoice_file'] == row['invoice_file'] else None
#                 invoice_file = invoice_file.split('/')[-1] if invoice_file else None       
#                 data_tup = (
#                         str(row['added_on']) if row['added_on'] == row['added_on'] else None,
#                         str(row['modified_on']) if row['modified_on'] == row['modified_on'] else None,
#                         str(row['transaction_id']) if row['transaction_id'] and row['transaction_id'] == row['transaction_id'] else str(row['id']),
#                         0,
#                         row['C_ID'] if row['C_ID'] and row['C_ID'] == row['C_ID'] else None,
#                         STATUS_MAP.get(row['status'], 0),
#                         row['currency'] if row['currency'] else 0,
#                         row['amount_payable'] if row['amount_payable'] else Decimal(0),
#                         row['total'] if row['total'] else Decimal(0),
#                         str(row['added_on']) if row['added_on'] == row['added_on'] else None,
#                         str(row['closed_on']) if row['closed_on'] and row['closed_on'] == row['closed_on'] else None,
#                         row['Email'],
#                         str(row['code2']) if row['code2'] and row['code2'] == row['code2'] else None,
#                         str(row['order_mobile']) if row['order_mobile'] and row['order_mobile'] == row['order_mobile'] else None,
#                         int(row['country_obj']) if row['country_obj'] and row['country_obj'] == row['country_obj'] else None,
#                         invoice_file,
#                         str(row['payment_date']) if row['payment_date'] and row['payment_date'] == row['payment_date'] else None,
#                         str(dict(row.to_dict())),
#                         row['id'],
#                         row['convenience_charges'] if row['convenience_charges'] and row['convenience_charges'] == row['convenience_charges'] else Decimal(0),
#                         row['welcome_call'],
#                         None,
#                         None,
#                         '',
#                         '',
#                         '' 
#                     )
                
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
#         print( 'Order Migrated Adding Coupons')
#         print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#         db2 = MySQLdb.connect(db2_host,db2_user,db2_pwd,db2_name, autocommit=True)
#         db = MySQLdb.connect(db_host,db_user,db_pwd,db_name)
        
#         new_order_df = pd.read_sql('SELECT id AS order_obj, co_id as id, candidate_id  from order_order', con=db2)
#         migrated_df = order_df[order_df.id.isin(new_order_df.id)]
        
#         not_migrated_df = order_df[~order_df.id.isin(new_order_df.id)]
        
#         migrated_df = pd.merge(migrated_df, new_order_df, how='left', on='id')
#         del order_df
#         del new_order_df
        
#         update_values = []
        
#         update_sql2 = """INSERT INTO order_couponorder (created, modified, coupon_code, coupon_id, order_id, value) VALUES (%s, %s, %s, %s, %s, %s)"""
#         for i, row in migrated_df.iterrows():
#             if row['coupon_obj'] and row['coupon_obj'] == row['coupon_obj']:
#                 data_tup = (
#                         str(row['added_on']) if row['added_on'] == row['added_on'] else None,
#                         str(row['modified_on']) if row['modified_on'] == row['modified_on'] else None,
#                         str(row['coupon']) if row['coupon'] and row['coupon'] == row['coupon'] else None,
#                         int(row['coupon_obj']) if row['coupon_obj'] and row['coupon_obj'] == row['coupon_obj'] else None,
#                         int(row['order_obj']) if row['order_obj'] and row['order_obj'] == row['order_obj'] else None,
#                         Decimal(0)
#                     )
                
#                 update_values.append(data_tup)    
#             if len(update_values) > 5000:
                
#                 print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#                 print( 'Bulk Insert Coupons ' + str(i))
#                 print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
                
#                 cursor.executemany(update_sql2, update_values)
#                 update_values = []
                
#         if update_values:
#             cursor.executemany(update_sql2, update_values)
#             update_values = []
        
#         update_values = []
#         STATUS_MAP = {
#                 0: 0,
#                 1: 0,
#                 2: 1,
#                 5: 1,
#                 6: 0,
#                 7: 1,
#                 8: 1,
#             }
        
#         print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#         print( 'Order Migrated Adding Transactions')
#         print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#         update_sql2 = """INSERT INTO payment_paymenttxn (created, modified, txn, status, payment_mode, payment_date,
#                 currency, instrument_number, instrument_issuer, instrument_issue_date, cart_id, order_id, txn_amount, txn_info) 
#                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
#         for i, row in migrated_df.iterrows():
#             if row['order_obj'] and row['order_obj'] == row['order_obj']:
#                 data_tup = (
#                         str(row['added_on']) if row['added_on'] == row['added_on'] else None,
#                         str(row['modified_on']) if row['modified_on'] == row['modified_on'] else None,
#                         str(row['transaction_id']) if row['transaction_id'] and row['transaction_id'] == row['transaction_id'] else str(row['id']),
#                         STATUS_MAP.get(row['status'], 0),
#                         PAYMENT_MAP.get(row['payment_mode'], 0),
#                         str(row['payment_date']) if row['payment_date'] and row['payment_date'] == row['payment_date'] else None,
#                         row['currency'] if row['currency'] else 0,
#                         str(row['instrument_number']) if row['instrument_number'] and row['instrument_number'] == row['instrument_number'] else None,
#                         str(row['instrument_issuer']) if row['instrument_issuer'] and row['instrument_issuer'] == row['instrument_issuer'] else None,
#                         str(row['instrument_issue_date']) if row['instrument_issue_date'] and row['instrument_issue_date'] == row['instrument_issue_date'] else None,
#                         None,
#                         int(row['order_obj']) if row['order_obj'] and row['order_obj'] == row['order_obj'] else None,
#                         row['amount_payable'] if row['amount_payable'] else Decimal(0),
#                         ''
#                     )
#                 update_values.append(data_tup)    
#             if len(update_values) > 5000:
                
#                 print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#                 print( 'Bulk Insert Txns' + str(i))
#                 print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
                
#                 cursor.executemany(update_sql2, update_values)
#                 update_values = []
                
#         if update_values:
#             cursor.executemany(update_sql2, update_values)
#             update_values = []
        
#         sql3 = """
#             SELECT cart_roundoneorder.id as r_id, cart_roundoneorder.user_id, cart_roundoneorder.order_id as id, 
#             cart_roundoneorder.status, cart_roundoneorder.remark, cart_roundoneorder.added_on, 
#             cart_roundoneorder.completed_on FROM cart_roundoneorder
#             """
#         db2 = MySQLdb.connect(db2_host,db2_user,db2_pwd,db2_name, autocommit=True)
#         db = MySQLdb.connect(db_host,db_user,db_pwd,db_name)
        
#         round_df = pd.read_sql(sql3, con=db)
#         order_df = migrated_df[['id', 'C_ID', 'order_obj', 'wallettransaction_id', 'wallettransaction_redeem_id', 'wallet_cashback']]
#         migrated_df = migrated_df[['id', 'C_ID', 'order_obj']]
#         round_df = pd.merge(round_df, migrated_df, how='left', on='id')
#         round_df = round_df[~round_df.order_obj.isnull()]
        
#         update_values = []
#         update_sql2 = """
#                 INSERT INTO cart_subscription 
#                 (created, modified, expire_on, candidateid, order_id, status, remark) VALUES
#                 (%s, %s, %s, %s, %s, %s, %s) 
                
#                 """
        
        
#         print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#         print( 'Bulk ROunONE Order Insert Start')
#         print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        
#         for i, row in round_df.iterrows():
#             if row['order_obj'] and row['order_obj'] == row['order_obj']:
#                 data_tup = (
#                     str(row['added_on']) if row['added_on'] == row['added_on'] else None,
#                     str(row['added_on']) if row['added_on'] == row['added_on'] else None,
#                     str(row['completed_on']) if row['completed_on'] and row['completed_on'] == row['completed_on'] else None,
#                     row['C_ID'],
#                     row['order_obj'],
#                     row['status'],
#                     row['remark']
#                 )
#                 update_values.append(data_tup)    
#             if len(update_values) > 1000:
                
#                 print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#                 print( 'Bulk Insert ' + str(i))
#                 print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#                 cursor.executemany(update_sql2, update_values)
#                 update_values = []
        
#         if len(update_values):
                
#             print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#             print( 'Bulk Insert ' + str(i))
#             print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#             cursor.executemany(update_sql2, update_values)
#             update_values = []
#         # del migrated_df
#         # sql = """
#         #         SELECT wallet.id, auth_user.email as Email, wallet.amount, 
#         #         wallet.created_on, wallet.expiring_on 
#         #         FROM wallet
#         #         LEFT JOIN auth_user
#         #         ON auth_user.id = wallet.user_id
#         #         """
#         # sql2 = """
#         #         SELECT wallettransaction.id, wallettransaction.wallet_id, 
#         #         wallettransaction.type_cashback, wallettransaction.amount, 
#         #         wallettransaction.current_amount, wallettransaction.created_on, 
#         #         wallettransaction.status, wallettransaction.order_id, 
#         #         wallettransaction.txn_id, wallettransaction.description, 
#         #         wallettransaction.expiring_on 
#         #         FROM wallettransaction
#         #     """
#         # user_df = pd.read_csv('cleaned_present_user.csv', sep=',')
#         # user_df = user_df[['Email', 'C_ID']]
#         # user_df = user_df.drop_duplicates(subset=['C_ID'], keep='last')
#         # db2 = MySQLdb.connect(db2_host,db2_user,db2_pwd,db2_name, autocommit=True)
#         # db = MySQLdb.connect(db_host,db_user,db_pwd,db_name)
        
#         # wallet_df = pd.read_sql(sql, con=db)
#         # wallettxn_df = pd.read_sql(sql2, con=db)
#         # wallet_df = pd.merge(wallet_df, user_df, how='left', on='Email')
#         # wallet_df = wallet_df[wallet_df.C_ID.notnull()]
#         # wallet_df = wallet_df.drop_duplicates(subset=['C_ID'], keep='last')
        
#         # del user_df


#         # print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#         # print( 'Wallet select done')
#         # print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        

#         # update_values = []
#         # update_sql2 = """
#         #         INSERT INTO wallet_wallet
#         #         (created, modified, owner, owner_email) VALUES
#         #         (%s, %s, %s, %s) 
                
#         #         """
        
        
#         # print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#         # print( 'Bulk Wallet Insert Start')
#         # print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        
#         # for i, row in wallet_df.iterrows():
#         #     if row['C_ID'] and row['C_ID'] == row['C_ID']:
#         #         data_tup = (
#         #             str(row['created_on']) if row['created_on'] == row['created_on'] else None,
#         #             str(row['created_on']) if row['created_on'] == row['created_on'] else None,
#         #             row['C_ID'],
#         #             row['Email']
#         #         )
#         #         update_values.append(data_tup)    
#         #     if len(update_values) > 1000:
                
#         #         print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#         #         print( 'Bulk Insert ' + str(i))
#         #         print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#         #         cursor.executemany(update_sql2, update_values)
#         #         update_values = []
        
#         # if len(update_values):
                
#         #     print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#         #     print( 'Bulk Insert ' + str(i))
#         #     print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#         #     cursor.executemany(update_sql2, update_values)
#         #     update_values = []
#         # db2 = MySQLdb.connect(db2_host,db2_user,db2_pwd,db2_name, autocommit=True)
#         # db = MySQLdb.connect(db_host,db_user,db_pwd,db_name)
        
#         # new_wallet_df = pd.read_sql('SELECT id as new_id, owner as C_ID, owner_email FROM wallet_wallet', con=db2)
#         # wallet_df = pd.merge(wallet_df, new_wallet_df, how='left', on='C_ID')
#         # wallet_df =  wallet_df[wallet_df.new_id.notnull()]
#         # wallettxn_df = wallettxn_df[wallettxn_df.wallet_id.isin(wallet_df.id)]
#         # order_df = order_df.rename(columns={'id': 'old_order_id', 'wallettransaction_redeem_id': 'id'})
#         # wallettxn_df = pd.merge(wallettxn_df, order_df, how='left', on='id')
        
#         # del new_wallet_df
#         # wallettxn_df = wallettxn_df[wallettxn_df.status == 2]
#         # wallet_add_df = wallettxn_df[(wallettxn_df.type_cashback == 2)]
#         # wallet_red_df = wallettxn_df[(wallettxn_df.type_cashback == 1)]
#         # wallet_exp_df = wallettxn_df[(wallettxn_df.type_cashback == 3)]
#         # del wallettxn_df
#         # wallet_df = wallet_df.rename(columns={'id': 'wallet_id', 'new_id': 'new_wallet_id'})
        
#         # wallet_add_df = pd.merge(wallet_add_df, wallet_df[['wallet_id','new_wallet_id']], how='left', on='wallet_id')
#         # wallet_red_df = pd.merge(wallet_red_df, wallet_df[['wallet_id','new_wallet_id']], how='left', on='wallet_id')
#         # wallet_exp_df = pd.merge(wallet_exp_df, wallet_df[['wallet_id','new_wallet_id']], how='left', on='wallet_id')
        
#         # update_values = []
#         # update_sql2 = """
#         #         INSERT INTO wallet_rewardpoint
#         #         (created, modified, original, current, expiry, last_used, status, txn, wallet_id, cw_id) VALUES
#         #         (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
#         #         """
        
#         # print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#         # print( 'Bulk ADD Credit Insert Start')
#         # print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#         # for i, row in wallet_add_df.iterrows():
#         #     if row['new_wallet_id'] and row['new_wallet_id'] == row['new_wallet_id']:
                
#         #         # status = 3
#         #         # if row['expiring_on'] and row['expiring_on'] == row['expiring_on']:
#         #         #     if row['expiring_on'].to_pydatetime() >= datetime.today():
#         #         #         status = 1
#         #         data_tup = ( 
#         #             str(row['created_on'].to_pydatetime()),
#         #             str(row['created_on'].to_pydatetime()),
#         #             row['amount'],       
#         #             row['amount'],       
#         #             str(row['expiring_on'].to_pydatetime()),
#         #             None,
#         #             1,
#         #             row['txn_id'],
#         #             row['new_wallet_id'],
#         #             row['id']
#         #         )
#         #         update_values.append(data_tup)    
#         #     if len(update_values) > 5000:
                
#         #         print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#         #         print( 'Bulk Insert ' + str(i))
#         #         print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#         #         cursor.executemany(update_sql2, update_values)
#         #         update_values = []
                
#         # if len(update_values):
                
#         #     print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#         #     print( 'Bulk Insert ' + str(i))
#         #     print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#         #     cursor.executemany(update_sql2, update_values)
#         #     update_values = []
#         # db2 = MySQLdb.connect(db2_host,db2_user,db2_pwd,db2_name, autocommit=True)
#         # db = MySQLdb.connect(db_host,db_user,db_pwd,db_name)
        
#         # new_point_df = pd.read_sql('SELECT id as new_pt_id, cw_id as id, status as pt_status FROM wallet_rewardpoint', con=db2)
#         # wallet_add_df = pd.merge(wallet_add_df, new_point_df, how='left', on='id') 
        
#         # update_values = []
#         # update_sql2 = """
#         #         INSERT INTO wallet_wallettransaction
#         #         (created, modified, txn_type, status, notes, txn, point_value, ecash_value, 
#         #         cart_id, order_id, wallet_id, current_value) VALUES
#         #         (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
#         #         """
        
#         # print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#         # print( 'Bulk ADD Credit TXN Insert Start')
#         # print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#         # for i, row in wallet_add_df.iterrows():
#         #     if row['new_pt_id'] and row['new_pt_id'] == row['new_pt_id']:
#         #         data_tup = ( 
#         #             str(row['created_on'].to_pydatetime()),
#         #             str(row['created_on'].to_pydatetime()),
#         #             1,       
#         #             1,       
#         #             'Migrated from CP',
#         #             row['new_pt_id'],
#         #             row['amount'],
#         #             0,
#         #             None,
#         #             None,
#         #             row['new_wallet_id'],
#         #             0
#         #         )
#         #         update_values.append(data_tup)    
#         #     if len(update_values) > 5000:
                
#         #         print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#         #         print( 'Bulk Insert ' + str(i))
#         #         print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#         #         cursor.executemany(update_sql2, update_values)
#         #         update_values = []
                
#         # if len(update_values):
                
#         #     print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#         #     print( 'Bulk Insert ' + str(i))
#         #     print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#         #     cursor.executemany(update_sql2, update_values)
#         #     update_values = []
#         # db2 = MySQLdb.connect(db2_host,db2_user,db2_pwd,db2_name, autocommit=True)
#         # db = MySQLdb.connect(db_host,db_user,db_pwd,db_name)
        
#         # new_point_df = pd.read_sql('SELECT id as new_txn_id, txn as new_pt_id FROM wallet_wallettransaction', con=db2)
#         # new_point_df.new_pt_id = pd.to_numeric(new_point_df.new_pt_id, errors='ignore')  
#         # wallet_add_df = pd.merge(wallet_add_df, new_point_df, how='left', on='new_pt_id') 
        
#         # update_values = []
#         # update_sql3 = """
#         #         INSERT INTO wallet_pointtransaction
#         #         (created, modified, txn_type, point_value, point_id, transaction_id) VALUES
#         #         (%s, %s, %s, %s, %s, %s) 
#         #         """
        
#         # print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#         # print( 'Bulk Add pt TXN Insert Start')
#         # print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#         # for i, row in wallet_add_df.iterrows():
#         #     if row['new_pt_id'] and row['new_pt_id'] == row['new_pt_id']:
#         #         data_tup = ( 
#         #             str(row['created_on'].to_pydatetime()),
#         #             str(row['created_on'].to_pydatetime()),
#         #             1,
#         #             row['amount'],
#         #             row['new_pt_id'],
#         #             row['new_txn_id'],
#         #         )
#         #         update_values.append(data_tup)    
#         #     if len(update_values) > 5000:
#         #         print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#         #         print( 'Bulk Insert ' + str(i))
#         #         print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#         #         cursor.executemany(update_sql3, update_values)
#         #         update_values = []
                
#         # if len(update_values):
                
#         #     print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#         #     print( 'Bulk Insert ' + str(i))
#         #     print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#         #     cursor.executemany(update_sql3, update_values)
#         #     update_values = []
        
#         # print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#         # print( 'Bulk REDEEM Credit TXN Insert Start')
#         # print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#         # for i, row in wallet_red_df.iterrows():
#         #     if row['new_wallet_id'] and row['new_wallet_id'] == row['new_wallet_id']:
#         #         data_tup = ( 
#         #             str(row['created_on'].to_pydatetime()),
#         #             str(row['created_on'].to_pydatetime()),
#         #             2,       
#         #             1,       
#         #             'Migrated from CP',
#         #             row['id'],
#         #             row['amount'],
#         #             0,
#         #             None,
#         #             row['order_obj'] if row['order_obj'] and row['order_obj'] == row['order_obj'] else None,
#         #             row['new_wallet_id'],
#         #             0
#         #         )
#         #         update_values.append(data_tup)    
#         #     if len(update_values) > 5000:
                
#         #         print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#         #         print( 'Bulk Insert ' + str(i))
#         #         print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#         #         cursor.executemany(update_sql2, update_values)
#         #         update_values = []
                
#         # if len(update_values):
                
#         #     print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#         #     print( 'Bulk Insert ' + str(i))
#         #     print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#         #     cursor.executemany(update_sql2, update_values)
#         #     update_values = []
        
#         # print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#         # print( 'Bulk EXP Credit TXN Insert Start')
#         # print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#         # for i, row in wallet_exp_df.iterrows():
#         #     if row['new_wallet_id'] and row['new_wallet_id'] == row['new_wallet_id']:
#         #         data_tup = ( 
#         #             str(row['created_on'].to_pydatetime()),
#         #             str(row['created_on'].to_pydatetime()),
#         #             4,       
#         #             1,       
#         #             'Migrated from CP',
#         #             row['id'],
#         #             row['amount'],
#         #             0,
#         #             None,
#         #             None,
#         #             row['new_wallet_id'],
#         #             0
#         #         )
#         #         update_values.append(data_tup)    
#         #     if len(update_values) > 5000:
                
#         #         print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#         #         print( 'Bulk Insert ' + str(i))
#         #         print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#         #         cursor.executemany(update_sql2, update_values)
#         #         update_values = []
                
#         # if len(update_values):
                
#         #     print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#         #     print( 'Bulk Insert ' + str(i))
#         #     print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#         #     cursor.executemany(update_sql2, update_values)
#         #     update_values = []
                

#         # db.close()
#         # db2.close()
