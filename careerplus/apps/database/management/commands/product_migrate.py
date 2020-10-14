# import MySQLdb
# import json
# import pandas as pd
# import numpy as np
# from decimal import Decimal
# from django.utils import timezone
# from datetime import datetime
# from django.conf import settings
# from database.models import CPUser
# from django.core.management.base import BaseCommand
# from django.db import IntegrityError, transaction
# from shop.models import *
# from faq.models import *
# from partner.models import *
# from users.models import User
# from shop.choices import *

# class Command(BaseCommand):
#     help = ('''Get Product Database from old Careerplus:
#         -- All Products with their Variations
#         -- Type of Product if chosen for product classes
#         -- Necessary Flags for Type Of Flow
#         ''')

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
        
#         cursor = db.cursor()

#         sql = """
#                 SELECT auth_user.id, auth_user.username, auth_user.first_name, auth_user.email, auth_user.is_active, cart_userprofile.mobile, cart_userprofile.usersite 
#                 FROM auth_user 
#                 LEFT OUTER JOIN cart_userprofile ON ( auth_user.id = cart_userprofile.user_id ) 
#                 WHERE auth_user.id IN (SELECT DISTINCT U0.owner_id FROM cart_product U0);
#             """
#         cursor.execute(sql,{})
#         result = cursor.fetchall()
#         try:
#             with transaction.atomic():
#                 count = 0
#                 for row in result:
#                     data = {
#                             'id': row[0],
#                             'username': row[1],
#                             'email': row[3],
#                             'first_name': row[2],
#                             'active': row[4],
#                             'mobile': row[5],
#                             'website': row[6],
#                         }
#                     ven, created = Vendor.objects.get_or_create(
#                         name=data['username'],
#                         cp_id=data['id'],
#                         )
#                     ven.email = data['email']
#                     if data['mobile']:
#                         ven.mobile=data['mobile']
#                     if data['website']:
#                         ven.website=data['website']
#                     ven.save()
#         except IntegrityError:
#             pass
#             print(row)
#             print('Fail')
#         cursor.close()
#         print("Vendor Migrated")        

#         sql = """
#             SELECT 
#                 cart_product.id AS 'pid', cart_productvariation.id AS 'pvid',cart_product.name AS 'pname',
#                 cart_product.price AS 'pprice', cart_product.short_desc, cart_product.long_desc, 
#                 cart_product.parent_id, cart_product.is_allocable, cart_product.country_id,
#                 cart_product.is_addon, cart_product.is_service,
#                 cart_product.added_on, cart_product.modified_on,
#                 cart_product.is_international, cart_product.to_boost, cart_product.to_highlight,
#                 cart_product.to_feature, cart_product.is_free_product,
#                 cart_product.product_trial, cart_product.is_active, cart_product.profile_update_required, 
#                 cart_product.salary_increment, cart_product.salary_candidates, cart_product.feedback_eligible, 
#                 cart_product.priority_in_emailer, cart_product.featured_eligible,
#                 cart_product.featured_days, cart_product.facebook_remarketing , cart_product.flags,
#                 cart_product.owner_id, cart_product.country_id, cart_productvariation.name AS 'pvname',
#                 cart_productvariation.type_of_product, cart_productvariation.sub_type_of_product,
#                 cart_productvariation.vendor_pv_id, 
#                 cart_productvariation.price AS 'pvprice', cart_productvariation.aed_price, cart_productvariation.usd_price,
#                 cart_productvariation.fake_price, cart_productvariation.fake_usd_price, cart_productvariation.fake_aed_price,
#                 cart_productvariation.experience_level, cart_productvariation.sample_document, 
#                 cart_productvariation.email_cc, cart_productvariation.with_certificate,
#                 cart_productvariation.description, 
#                 cart_productvariation.introduction, cart_productvariation.about,
#                 cart_productvariation.what_you_get,  cart_productvariation.update_combo_price,
#                 cart_productvariation.combo_discount, cart_productvariation.frequently_bought, 
#                 cart_productvariation.cart_description 
#             FROM cart_product 
#             LEFT OUTER JOIN cart_productvariation ON ( cart_product.id = cart_productvariation.product_id );
#             """        
#         df = pd.read_sql(sql, con=db)
#         df['flags'] = df['flags'].apply(lambda x:json.loads(x))
#         df['course'] = df['flags'].apply(lambda x:x.get('course', False))
#         df['combo'] = df['flags'].apply(lambda x:x.get('combo', False))
#         product_withpv = df.loc[df['pvid'].notnull()]
#         df2 = product_withpv[['pid', 'pvid']]
#         df2 = df2.groupby('pid').count()

#         with_variation = df2[df2['pvid']> 1].index
#         without_variation = df2[df2['pvid']< 2].index
        
#         product_standalone = product_withpv.loc[df['pid'].isin(without_variation)]
#         product_variation = product_withpv.loc[df['pid'].isin(with_variation)]
#         product_withoutpv = df.loc[df['pvid'].isnull()]
        
#         pwriting = ProductClass.objects.get(
#                         slug='writing')
#         pcourse = ProductClass.objects.get(
#                         slug='course')
#         pservice = ProductClass.objects.get(
#                         slug='service')
#         pother = ProductClass.objects.get(
#                         slug='other')
        
#         try:
#             with transaction.atomic():
#                 for i, row in product_withoutpv.iterrows():
#                     flag_course = row['course']
#                     flag_combo = row['combo']
#                     type_flow = 2

#                     if flag_course:
#                         product_class = pcourse
#                         type_flow = 2
#                         type_product = 0
#                     elif row['to_boost']:
#                         product_class = pservice
#                         type_flow = 7
#                         type_product = 4
#                     elif row['to_feature'] or row['profile_update_required']:    
#                         product_class = pservice
#                         type_flow = 5
#                         type_product = 4
#                     elif row['is_international']:    
#                         product_class = pservice
#                         type_flow = 4
#                         type_product = 4
#                     else:    
#                         product_class = pother
#                         type_flow = 2
#                         type_product = 4
#                     try:
#                         vendor = Vendor.objects.get(cp_id=row['owner_id'])
#                     except:
#                         vendor = Vendor.objects.get(name='ops')
#                     psc, created = ProductScreen.objects.get_or_create(
#                         name=row['pname'],
#                         cp_id=row['pid'])
                    
#                     psc.inr_price = Decimal(str(row['pprice'])) if row['pprice'] == row['pprice'] else Decimal(0)
#                     psc.type_product = type_product
#                     psc.product_class = product_class
#                     psc.created = timezone.make_aware(datetime.strptime(str(row['added_on']), "%Y-%m-%d %H:%M:%S"),
#                         timezone.get_current_timezone()) if str(row['added_on']) else timezone.now()
#                     psc.about = row['short_desc'] if row['short_desc'] else '' 
#                     psc.description = row['long_desc'] if row['long_desc'] else ''
#                     psc.type_flow = type_flow
#                     psc.vendor = vendor
#                     psc.save()    
#                     prd = psc.create_product()
#                     prd.cp_id = row['pid']
                    
                    
#                     prd.created = timezone.make_aware(datetime.strptime(str(row['added_on']), "%Y-%m-%d %H:%M:%S"),
#                         timezone.get_current_timezone()) if str(row['added_on']) else timezone.now()
#                     prd.type_flow = type_flow
#                     prd.about = row['short_desc'] if row['short_desc'] else ''
#                     prd.description = row['long_desc'] if row['long_desc'] else ''
#                     prd.archive_json = dict(row.to_dict())
#                     prd.vendor = vendor
#                     prd.active = False
#                     prd.is_indexable = False
#                     prd.save()
#         except Exception as e:
#             print(row)
#             print(e)
#         print('Product Without Product Variation Migrated')
        

#         try:
#             with transaction.atomic():
#                 for i, row in product_standalone.iterrows():
#                     if not i%50:
#                         print(i)
#                     flag_course = row['course']
#                     flag_combo = row['combo']
#                     type_of_product = row['type_of_product']
#                     sub_type_of_product = row['sub_type_of_product']
#                     type_product = 0
#                     product_class = pother
#                     type_flow = 2
                    
#                     if row['pid'] in [357, 355, 4411]:
#                         product_class = pservice
#                         type_product = 0
#                         type_flow = 6
#                     elif row['pid'] in [1143, 4413]:
#                         product_class = pservice
#                         type_product = 0
#                         type_flow = 9
#                     elif row['to_boost']:
#                         product_class = pservice
#                         type_product = 0
#                         type_flow = 7
#                     elif row['profile_update_required']:
#                         product_class = pservice
#                         type_product = 0
#                         type_flow = 5
#                     elif row['is_international']:
#                         if row['is_service']:
#                             product_class = pservice
#                             if ['is_addon']:
#                                 type_product = 4
#                             else:
#                                 type_product = 0
#                             if type_of_product == 2:
#                                 type_flow = 6
#                             else:
#                                 type_flow = 4
#                         else:
#                             if type_of_product == 2:
#                                 product_class = pcourse
#                                 type_flow = 2
#                             else:
#                                 product_class = pwriting
#                                 type_flow = 12
#                     elif type_of_product == 5:
#                         product_class = pwriting
#                         type_product = 0
#                         type_flow = 3
#                     elif type_of_product == 1:
#                         if flag_combo:
#                             product_class = pwriting
#                             type_product = 3
#                             type_flow = 1
#                         else:
#                             if sub_type_of_product == 7:
#                                 product_class = pwriting
#                                 type_product = 0
#                                 type_flow = 8
#                             elif sub_type_of_product == 8:
#                                 product_class = pcourse
#                                 type_product = 0
#                                 type_flow = 6
#                             elif sub_type_of_product == 1:
#                                 product_class = pcourse
#                                 type_product = 0
#                                 type_flow = 2
#                             else:
#                                 if row['is_addon']:
#                                     type_product = 4
#                                     product_class = pwriting
#                                     type_flow = 1
#                                 else:
#                                     type_product = 0
#                                     product_class = pwriting
#                                     type_flow = 1
#                     elif type_of_product == 3:
#                         type_product = 0
#                         product_class = pother
#                         type_flow = 11
#                     else:
#                         if flag_combo:
#                             product_class = pcourse
#                             type_product = 3
#                             type_flow = 2
#                         elif sub_type_of_product == 13:
#                             product_class = pcourse
#                             type_product = 0
#                             type_flow = 10
#                         else:
#                             product_class = pcourse
#                             type_product = 0
#                             type_flow = 2
                    
#                     try:
#                         vendor = Vendor.objects.get(cp_id=row['owner_id'])
#                     except:
#                         vendor = Vendor.objects.get(name='ops')
#                     name = ''
#                     if type_of_product == 1:
#                         name = row['pname'] + ' - ' + row['pvname']
#                     else:
#                         name = row['pname']
                    
#                     psc, created = ProductScreen.objects.get_or_create(
#                         name=row['pname'][:100],
#                         cp_id=row['pid'],
#                         cpv_id=row['pvid'])
                    
#                     psc.inr_price = Decimal(str(row['pvprice'])) if row['pvprice'] == row['pvprice'] and row['pvprice'] else Decimal(0)
#                     psc.fake_inr_price = Decimal(str(row['fake_price'])) if row['fake_price'] == row['fake_price'] and row['fake_price'] else Decimal(0)
#                     psc.usd_price = Decimal(str(row['usd_price'])) if row['usd_price'] == row['usd_price'] and row['usd_price'] else Decimal(0)
#                     psc.fake_usd_price = Decimal(str(row['fake_usd_price'])) if row['fake_usd_price'] == row['fake_usd_price'] and row['fake_usd_price'] else Decimal(0)
#                     psc.aed_price = Decimal(str(row['aed_price'])) if row['aed_price'] == row['aed_price'] and row['aed_price'] else Decimal(0)
#                     psc.fake_aed_price = Decimal(str(row['fake_aed_price'])) if row['fake_aed_price'] == row['fake_aed_price'] and row['fake_aed_price'] else Decimal(0)
                                        

#                     psc.type_product = type_product
#                     psc.product_class = product_class
#                     psc.created = timezone.make_aware(datetime.strptime(str(row['added_on']), "%Y-%m-%d %H:%M:%S"),
#                         timezone.get_current_timezone()) if str(row['added_on']) else timezone.now()
#                     about = row['short_desc'] if row['short_desc'] else ''
#                     about = about + row['about'] if row['about'] else ''
#                     description = row['long_desc'] if row['short_desc'] else ''
#                     description = description + row['description'] if row['description'] else ''
                    
#                     psc.about = about if about else '' 
#                     psc.description = description if description else ''
#                     psc.buy_shine = row['what_you_get'] if row['what_you_get'] else '' 
#                     psc.type_flow = type_flow
#                     psc.vendor = vendor
#                     psc.upc = row['vendor_pv_id'] if row['vendor_pv_id'] else ''


#                     psc.save()    
                    
                    
#                     prd = psc.create_product()
#                     prd.cp_id = row['pid']
#                     prd.cpv_id = row['pvid']
                    
#                     prd.inr_price = Decimal(str(row['pvprice'])) if row['pvprice'] == row['pvprice'] and row['pvprice'] else Decimal(0)
#                     prd.fake_inr_price = Decimal(str(row['fake_price'])) if row['fake_price'] == row['fake_price'] and row['fake_price'] else Decimal(0)
#                     prd.usd_price = Decimal(str(row['usd_price'])) if row['usd_price'] == row['usd_price'] and row['usd_price'] else Decimal(0)
#                     prd.fake_usd_price = Decimal(str(row['fake_usd_price'])) if row['fake_usd_price'] == row['fake_usd_price'] and row['fake_usd_price'] else Decimal(0)
#                     prd.aed_price = Decimal(str(row['aed_price'])) if row['aed_price'] == row['aed_price'] and row['aed_price'] else Decimal(0)
#                     prd.fake_aed_price = Decimal(str(row['fake_aed_price'])) if row['fake_aed_price'] == row['fake_aed_price'] and row['fake_aed_price'] else Decimal(0)
                    
#                     prd.created = timezone.make_aware(datetime.strptime(str(row['added_on']), "%Y-%m-%d %H:%M:%S"),
#                         timezone.get_current_timezone()) if str(row['added_on']) else timezone.now()
#                     prd.type_flow = type_flow
#                     prd.upc = row['vendor_pv_id'] if row['vendor_pv_id'] else '' 

#                     prd.about = about if about else '' 
#                     prd.description = description if description else ''
#                     prd.buy_shine = row['what_you_get'] if row['what_you_get'] else '' 
                    
#                     prd.archive_json = dict(row.to_dict())
#                     prd.vendor = vendor
#                     prd.active = False
#                     prd.is_indexable = False
#                     prd.save()
        
#         except Exception as e:
#             print(row)
#             print(e)
#         print('Product Standalone Product Variation Migrated')
        
        
#         try:
#             with transaction.atomic():
#                 for i, row in product_variation.iterrows():
#                     if not i%50:
#                         print(i)
#                     flag_course = row['course']
#                     flag_combo = row['combo']
#                     type_of_product = row['type_of_product']
#                     sub_type_of_product = row['sub_type_of_product']
#                     type_product = 0
#                     product_class = pother
#                     type_flow = 2
                    
#                     if row['pid'] in [357, 355, 4411]:
#                         product_class = pservice
#                         type_product = 0
#                         type_flow = 6
#                     elif row['pid'] in [1143, 4413]:
#                         product_class = pservice
#                         type_product = 0
#                         type_flow = 9
#                     elif row['to_boost']:
#                         product_class = pservice
#                         type_product = 0
#                         type_flow = 7
#                     elif row['profile_update_required']:
#                         product_class = pservice
#                         type_product = 0
#                         type_flow = 5
#                     elif row['is_international']:
#                         if row['is_service']:
#                             product_class = pservice
#                             if ['is_addon']:
#                                 type_product = 4
#                             else:
#                                 type_product = 0
#                             if type_of_product == 2:
#                                 type_flow = 6
#                             else:
#                                 type_flow = 4
#                         else:
#                             if type_of_product == 2:
#                                 product_class = pcourse
#                                 type_flow = 2
#                             else:
#                                 product_class = pwriting
#                                 type_flow = 12
#                     elif type_of_product == 5:
#                         product_class = pwriting
#                         type_product = 0
#                         type_flow = 3
#                     elif type_of_product == 1:
#                         if flag_combo:
#                             product_class = pwriting
#                             type_product = 3
#                             type_flow = 1
#                         else:
#                             if sub_type_of_product == 7:
#                                 product_class = pwriting
#                                 type_product = 0
#                                 type_flow = 8
#                             elif sub_type_of_product == 8:
#                                 product_class = pcourse
#                                 type_product = 0
#                                 type_flow = 6
#                             elif sub_type_of_product == 1:
#                                 product_class = pcourse
#                                 type_product = 0
#                                 type_flow = 2
#                             else:
#                                 if row['is_addon']:
#                                     type_product = 4
#                                     product_class = pwriting
#                                     type_flow = 1
#                                 else:
#                                     type_product = 0
#                                     product_class = pwriting
#                                     type_flow = 1
#                     elif type_of_product == 3:
#                         type_product = 0
#                         product_class = pother
#                         type_flow = 11
#                     else:
#                         if flag_combo:
#                             product_class = pcourse
#                             type_product = 3
#                             type_flow = 2
#                         elif sub_type_of_product == 13:
#                             product_class = pcourse
#                             type_product = 0
#                             type_flow = 10
#                         else:
#                             product_class = pcourse
#                             type_product = 0
#                             type_flow = 2
                    
#                     try:
#                         vendor = Vendor.objects.get(cp_id=row['owner_id'])
#                     except:
#                         vendor = Vendor.objects.get(name='ops')
#                     name = ''
#                     if type_of_product == 1:
#                         name = row['pname'] + ' - ' + row['pvname']
#                     else:
#                         name = row['pname']
                    
#                     psc, created = ProductScreen.objects.get_or_create(
#                         name=row['pname'][:100],
#                         cp_id=row['pid'],
#                         cpv_id=row['pvid'])

#                     psc.type_product = type_product
#                     psc.product_class = product_class
#                     psc.created = timezone.make_aware(datetime.strptime(str(row['added_on']), "%Y-%m-%d %H:%M:%S"),
#                         timezone.get_current_timezone()) if str(row['added_on']) else timezone.now()
#                     about = row['short_desc'] if row['short_desc'] else ''
#                     about = about + row['about'] if row['about'] else ''
#                     description = row['long_desc'] if row['short_desc'] else ''
#                     description = description + row['description'] if row['description'] else ''
                    
#                     psc.about = about if about else '' 
#                     psc.description = description if description else ''
#                     psc.buy_shine = row['what_you_get'] if row['what_you_get'] else '' 
#                     psc.type_flow = type_flow
#                     psc.vendor = vendor
#                     psc.upc = row['vendor_pv_id'] if row['vendor_pv_id'] else ''


#                     psc.save()    
                    
                    
#                     psc.inr_price = Decimal(str(row['pvprice'])) if row['pvprice'] == row['pvprice'] and row['pvprice'] else Decimal(0)
#                     psc.fake_inr_price = Decimal(str(row['fake_price'])) if row['fake_price'] == row['fake_price'] and row['fake_price'] else Decimal(0)
#                     psc.usd_price = Decimal(str(row['usd_price'])) if row['usd_price'] == row['usd_price'] and row['usd_price'] else Decimal(0)
#                     psc.fake_usd_price = Decimal(str(row['fake_usd_price'])) if row['fake_usd_price'] == row['fake_usd_price'] and row['fake_usd_price'] else Decimal(0)
#                     psc.aed_price = Decimal(str(row['aed_price'])) if row['aed_price'] == row['aed_price'] and row['aed_price'] else Decimal(0)
#                     psc.fake_aed_price = Decimal(str(row['fake_aed_price'])) if row['fake_aed_price'] == row['fake_aed_price'] and row['fake_aed_price'] else Decimal(0)
                                        

                    
                    
#                     prd = psc.create_product()
#                     prd.cp_id = row['pid']
#                     prd.cpv_id = row['pvid']
                    
#                     prd.inr_price = Decimal(str(row['pvprice'])) if row['pvprice'] == row['pvprice'] and row['pvprice'] else Decimal(0)
#                     prd.fake_inr_price = Decimal(str(row['fake_price'])) if row['fake_price'] == row['fake_price'] and row['fake_price'] else Decimal(0)
#                     prd.usd_price = Decimal(str(row['usd_price'])) if row['usd_price'] == row['usd_price'] and row['usd_price'] else Decimal(0)
#                     prd.fake_usd_price = Decimal(str(row['fake_usd_price'])) if row['fake_usd_price'] == row['fake_usd_price'] and row['fake_usd_price'] else Decimal(0)
#                     prd.aed_price = Decimal(str(row['aed_price'])) if row['aed_price'] == row['aed_price'] and row['aed_price'] else Decimal(0)
#                     prd.fake_aed_price = Decimal(str(row['fake_aed_price'])) if row['fake_aed_price'] == row['fake_aed_price'] and row['fake_aed_price'] else Decimal(0)
                    
#                     prd.created = timezone.make_aware(datetime.strptime(str(row['added_on']), "%Y-%m-%d %H:%M:%S"),
#                         timezone.get_current_timezone()) if str(row['added_on']) else timezone.now()
#                     prd.type_flow = type_flow
#                     prd.upc = row['vendor_pv_id'] if row['vendor_pv_id'] else '' 

#                     prd.about = about if about else '' 
#                     prd.description = description if description else ''
#                     prd.buy_shine = row['what_you_get'] if row['what_you_get'] else '' 
                    
#                     prd.archive_json = dict(row.to_dict())
#                     prd.vendor = vendor
#                     prd.active = False
#                     prd.is_indexable = False
#                     prd.save()
        
#         except Exception as e:
#             print(row)
#             print(e)
#         print('Product with Product Variation Migrated')
        
#         sql = """
#             SELECT cart_productpageviews.variation_id, cart_productpageviews.views FROM cart_productpageviews
#             """        
#         df = pd.read_sql(sql, con=db)
#         cpv_list = []
#         cpv_id_list = []
#         for i, row in df.iterrows():
#             cpv_list.append(' WHEN {0} THEN {1} '.format(row['variation_id'], row['views']))
#             cpv_id_list.append(str(row['variation_id']))
#         update_sql = '''
#             UPDATE shop_product SET cp_page_view = (
#             CASE cpv_id 
#                 {0}
#             END) WHERE cpv_id IN ({1});
#             '''.format(' '.join(cpv_list), ', '.join(cpv_id_list))    
        
#         db2.query(update_sql)
#         print('Product Variation Views Migrated')
        
        
#         sql = """
#                 SELECT theme_faq.id, theme_faq.answer, theme_faq.question, cart_product_faq.product_id
#                 FROM theme_faq 
#                 LEFT OUTER JOIN cart_product_faq ON ( theme_faq.id = cart_product_faq.faq_id ) 
#                 LEFT OUTER JOIN cart_product ON ( cart_product_faq.product_id = cart_product.id );
#             """
#         df = pd.read_sql(sql, con=db)
#         df = df[np.isfinite(df['product_id'])]
#         product_list = dict(df.groupby(['id'])['product_id'].apply(list))
#         question = dict(df.groupby(['id'])['question'].apply(list))
#         answer = dict(df.groupby(['id'])['answer'].apply(list))
#         vendorfaq = Vendor.objects.get(name='ops')
#         j = 1 
#         try:
#             with transaction.atomic():
        
#                 for key in dict(question).keys():
#                     j += 1
#                     if not j %50:
#                         print(j)
                    
#                     sfaq, created = ScreenFAQ.objects.get_or_create(
#                         text=question.get(key)[0],
#                         vendor=vendorfaq
#                         )
                    
#                     sfaq.answer = answer.get(key)[0]
#                     sfaq.save()
#                     faq = sfaq.create_faq()
#                     pv_list = product_list.get(key, [])
#                     owner_list = []
#                     if pv_list:
#                         pv_list = ProductScreen.objects.filter(cpv_id__in=pv_list)
                        
#                         for pv in pv_list:
#                             faq.public_vendor.add(pv.vendor) 
#                             screen = pv
#                             product = pv.create_product()
#                             fqprd, created = FAQProduct.objects.get_or_create(
#                                 product=product,
#                                 question=faq)
#                             sfqprd, created = FAQProductScreen.objects.get_or_create(
#                                 product=screen,
#                                 question=faq)
#                         faq.save()
#         except Exception as e:
#             print(e)
#         print('Product FAQ Migrated')
        
#         sql = """
#             SELECT cart_courseinfo.course_parent_id, cart_courseinfo.study_mode, 
#             cart_courseinfo.lms_duration, cart_courseinfo.program_struct, 
#             cart_productvariation.with_certificate 
#             FROM cart_courseinfo 
#             LEFT OUTER JOIN cart_productvariation 
#             ON ( cart_courseinfo.course_parent_id = cart_productvariation.id )"""
#         df = pd.read_sql(sql, con=db)
#         SM1 = AttributeOption.objects.get(code='OL')
#         SM2 = AttributeOption.objects.get(code='OF')
#         SM3 = AttributeOption.objects.get(code='IL')
#         SM4 = AttributeOption.objects.get(code='BL')
#         SM5 = AttributeOption.objects.get(code='CA')
#         SM6 = AttributeOption.objects.get(code='CF')
#         SM7 = AttributeOption.objects.get(code='DL')
#         try:
#             with transaction.atomic():
#                 for i, row in df.iterrows():
#                     if not i%50:
#                         print(i)
                    
#                     prd = Product.objects.get(cpv_id=row['course_parent_id'])
#                     scr = ProductScreen.objects.get(cpv_id=row['course_parent_id'])
#                     if row['with_certificate']:    
#                         setattr(prd.attr, C_ATTR_DICT.get('CERT'), 1)
#                         setattr(scr.attr, C_ATTR_DICT.get('CERT'), 1)
                        
#                     if row['study_mode'] in ['1','2','3','4','5','6','7']:
#                         SM = None
#                         if ['study_mode'] == '1':
#                             SM = SM1
#                         elif row['study_mode'] == '2':
#                             SM = SM2
#                         elif row['study_mode'] == '3':
#                             SM = SM3
#                         elif row['study_mode'] == '4':
#                             SM = SM4
#                         elif row['study_mode'] == '5':
#                             SM = SM5
#                         elif row['study_mode'] == '6':
#                             SM = SM6
#                         setattr(prd.attr, C_ATTR_DICT.get('SM'), SM)
#                         setattr(scr.attr, C_ATTR_DICT.get('SM'), SM)
#                     if row['program_struct']:
#                         ch_pr = Chapter.objects.create(
#                             heading='Program Structure',
#                             answer=row['program_struct'],
#                             product=prd)
#                         ch_scr = ScreenChapter.objects.create(
#                             heading='Program Structure',
#                             answer=row['program_struct'],
#                             product=scr,
#                             chapter=ch_pr)
                    
#                     if row['lms_duration']:
#                         dd = row['lms_duration'].lower()
#                         if 'inf' in dd or 'life' in dd or 'online' in dd or 'any' in dd:
#                             DD = 1500
#                         else:
#                             try:
#                                 DD = int(dd.split(' ')[0])    
#                             except:
#                                 DD = 0
#                             if 'day' in dd:
#                                 DD = DD
#                             elif 'mon' in dd:
#                                 DD = 31* DD
#                             elif 'week' in dd:
#                                 DD = 7*DD
#                             elif 'year' in dd:
#                                 DD = 365*DD
#                             elif 'hour' in dd:
#                                 DD = (DD//24)
#                             else:
#                                 DD = 0
#                             setattr(prd.attr, C_ATTR_DICT.get('DD'), DD)
#                             setattr(scr.attr, C_ATTR_DICT.get('DD'), DD)
                        
#                     prd.save()
#                     scr.save()
                                        
#         except Exception as e:
#             print(e)
#         print('Product Attribute Migrated')
        
#         db.close()
#         db2.close()