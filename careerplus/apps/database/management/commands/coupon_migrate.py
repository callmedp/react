# import MySQLdb
# from decimal import Decimal
# from django.utils import timezone
# from datetime import datetime
# from django.conf import settings
# from database.models import CPUser
# from django.core.management.base import BaseCommand
# from django.db import IntegrityError, transaction
# from coupon.models import Coupon


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
#         cursor = db.cursor()

#         sql = """
#             SELECT coupon_coupon.code, coupon_coupon.user, coupon_coupon.discount, coupon_coupon.flat_discount, coupon_coupon.added_on, coupon_coupon.valid_from, coupon_coupon.valid_to, coupon_coupon.description, coupon_coupon.consumed_by_id, coupon_coupon.for_user_id, coupon_coupon.type, coupon_coupon.active, coupon_coupon.max_allowed_usage, coupon_coupon.usage_count, coupon_coupon.product_id, coupon_coupon.productvariation_id, coupon_coupon.category_id, coupon_coupon.multipleproduct_ids, coupon_coupon.for_order_id 
#             FROM coupon_coupon 
#             WHERE (coupon_coupon.active = True  AND coupon_coupon.valid_to >= '2017-11-01 00:00:00'  AND coupon_coupon.valid_from <= '2017-10-15 00:00:00' ) ORDER BY coupon_coupon.added_on DESC
#             """
#         cursor.execute(sql,{})
#         count = 0
#         result = cursor.fetchall()
#         try:
#             with transaction.atomic():
#                 count = 0
#                 for row in result:
#                     data = {
#                             'code': row[0],
#                             'user': row[1],
#                             'discount': row[2],
#                             'flat_discount': row[3],
#                             'added_on': row[4],
#                             'valid_from': row[5],
#                             'valid_to': row[6],
#                             'description': row[7],
#                             'consumed_by_id': row[8],
#                             'for_user_id': row[9],
#                             'type': row[10],
#                             'active': row[11],
#                             'max_allowed_usage': row[12],
#                             'usage_count': row[13],
#                             'pvid': row[15],
                               
#                         }
#                     if data['usage_count'] < data['max_allowed_usage']: 
#                         if data['type'] == 0:
#                             cups, created = Coupon.objects.get_or_create(
#                                 code=data['code'],
#                                 )
#                             cups.active = True
#                             cups.valid_from = timezone.make_aware(data['valid_from'],
#                                     timezone.get_current_timezone()) if data['valid_from'] else timezone.now()
#                             cups.valid_until = timezone.make_aware(data['valid_to'],
#                                     timezone.get_current_timezone()) if data['valid_to'] else timezone.now()
#                             cups.user_limit = 1
#                             if data['discount']:
#                                 cups.coupon_type = 'percent'
#                                 cups.value = data['discount']
#                             elif data['flat_discount']:
#                                 cups.coupon_type = 'flat'
#                                 cups.value = data['flat_discount']
#                             cups.max_deduction = Decimal(5000)
#                             cups.created = timezone.make_aware(data['added_on'],
#                                     timezone.get_current_timezone()) if data['added_on'] else timezone.now()
#                             cups.save() 

#                         elif data['type'] == 1:
#                             cups, created = Coupon.objects.get_or_create(
#                                 code=data['code'],
#                                 )
#                             cups.active = True
#                             cups.valid_from = timezone.make_aware(data['valid_from'],
#                                     timezone.get_current_timezone()) if data['valid_from'] else timezone.now()
#                             cups.valid_until = timezone.make_aware(data['valid_to'],
#                                     timezone.get_current_timezone()) if data['valid_to'] else timezone.now()
#                             cups.user_limit = data['max_allowed_usage'] if data['max_allowed_usage'] < 1000 else 1000
#                             if data['discount']:
#                                 cups.coupon_type = 'percent'
#                                 cups.value = data['discount']
#                             elif data['flat_discount']:
#                                 cups.coupon_type = 'flat'
#                                 cups.value = data['flat_discount']
#                             cups.max_deduction = Decimal(5000)
#                             cups.created = timezone.make_aware(data['added_on'],
#                                     timezone.get_current_timezone()) if data['added_on'] else timezone.now()
#                             cups.save()
#                         elif data['type'] == 2:
#                             pass
#                         elif data['type'] == 3:
#                             cups, created = Coupon.objects.get_or_create(
#                                 code=data['code'],
#                                 )
#                             cups.active = True
#                             cups.valid_from = timezone.make_aware(data['valid_from'],
#                                     timezone.get_current_timezone()) if data['valid_from'] else timezone.now()
#                             cups.valid_until = timezone.make_aware(data['valid_to'],
#                                     timezone.get_current_timezone()) if data['valid_to'] else timezone.now()
#                             cups.user_limit = 1
#                             if data['flat_discount']:
#                                 cups.coupon_type = 'flat'
#                                 cups.value = data['flat_discount']
#                             cups.max_deduction = Decimal(2000)
#                             cups.created = timezone.make_aware(data['added_on'],
#                                     timezone.get_current_timezone()) if data['added_on'] else timezone.now()
#                             cups.save()
#                         elif data['type'] == 4:
#                             pass # no migrate
#                         elif data['type'] == 5:
#                             cups, created = Coupon.objects.get_or_create(
#                                 code=data['code'],
#                                 )
#                             cups.active = True
#                             cups.valid_from = timezone.make_aware(data['valid_from'],
#                                     timezone.get_current_timezone()) if data['valid_from'] else timezone.now()
#                             cups.valid_until = timezone.make_aware(data['valid_to'],
#                                     timezone.get_current_timezone()) if data['valid_to'] else timezone.now()
#                             cups.user_limit = 1
#                             cups.coupon_type = 'flat'
#                             if data['pvid'] == 23:
#                                 cups.value = Decimal(2399)
#                             elif data['pvid'] == 2083:
#                                 cups.value = Decimal(1699)
#                             elif data['pvid'] == 3303:
#                                 cups.value = Decimal(2899)
#                             else:
#                                 cups.value = Decimal(0)
#                             cups.max_deduction = Decimal(5000)
#                             cups.created = timezone.make_aware(data['added_on'],
#                                     timezone.get_current_timezone()) if data['added_on'] else timezone.now()
#                             cups.save()
#                         count +=1
#                         if not count%500:
#                             print(count)     
#         except IntegrityError:
#             pass
#             print('Fail')
        
#         db = MySQLdb.connect(db_host,db_user,db_pwd,db_name)
#         cursor = db.cursor()

#         sql2 = """
#                 SELECT coupon_coupon.code, coupon_coupon.user, coupon_coupon.discount, coupon_coupon.flat_discount, coupon_coupon.added_on, coupon_coupon.valid_from, coupon_coupon.valid_to, coupon_coupon.description, coupon_coupon.consumed_by_id, coupon_coupon.for_user_id, coupon_coupon.type, coupon_coupon.active, coupon_coupon.max_allowed_usage, coupon_coupon.usage_count, coupon_coupon.product_id, coupon_coupon.productvariation_id, coupon_coupon.category_id, coupon_coupon.multipleproduct_ids, coupon_coupon.for_order_id  
#                 FROM coupon_coupon 
#                 WHERE coupon_coupon.code in ( SELECT distinct(cart_order.coupon_id) FROM cart_order 
#                 WHERE cart_order.added_on >= '2014-04-1 00:00:00' AND cart_order.candidate_id IS NOT NULL);
#             """
#         cursor.execute(sql2,{})

#         result = cursor.fetchall()
#         try:
#             with transaction.atomic():
#                 count = 0
#                 for row in result:
#                     data = {
#                             'code': row[0],
#                             'user': row[1],
#                             'discount': row[2],
#                             'flat_discount': row[3],
#                             'added_on': row[4],
#                             'valid_from': row[5],
#                             'valid_to': row[6],
#                             'description': row[7],
#                             'consumed_by_id': row[8],
#                             'for_user_id': row[9],
#                             'type': row[10],
#                             'active': row[11],
#                             'max_allowed_usage': row[12],
#                             'usage_count': row[13],
#                             'pvid': row[15],
                               
#                         }
#                     if data['type'] == 0:
#                         cups, created = Coupon.objects.get_or_create(
#                             code=data['code'],
#                             )
#                         cups.active = True
#                         cups.valid_from = timezone.make_aware(data['valid_from'],
#                                 timezone.get_current_timezone()) if data['valid_from'] else timezone.now()
#                         cups.valid_until = timezone.make_aware(data['valid_to'],
#                                 timezone.get_current_timezone()) if data['valid_to'] else timezone.now()
#                         cups.user_limit = 1
#                         if data['discount']:
#                             cups.coupon_type = 'percent'
#                             cups.value = data['discount']
#                         elif data['flat_discount']:
#                             cups.coupon_type = 'flat'
#                             cups.value = data['flat_discount']
#                         cups.max_deduction = Decimal(5000)
#                         cups.created = timezone.make_aware(data['added_on'],
#                                 timezone.get_current_timezone()) if data['added_on'] else timezone.now()
#                         cups.save() 

#                     elif data['type'] == 1:
#                         cups, created = Coupon.objects.get_or_create(
#                             code=data['code'],
#                             )
#                         cups.active = True
#                         cups.valid_from = timezone.make_aware(data['valid_from'],
#                                 timezone.get_current_timezone()) if data['valid_from'] else timezone.now()
#                         cups.valid_until = timezone.make_aware(data['valid_to'],
#                                 timezone.get_current_timezone()) if data['valid_to'] else timezone.now()
#                         cups.user_limit = data['max_allowed_usage'] if data['max_allowed_usage'] < 1000 else 1000
#                         if data['discount']:
#                             cups.coupon_type = 'percent'
#                             cups.value = data['discount']
#                         elif data['flat_discount']:
#                             cups.coupon_type = 'flat'
#                             cups.value = data['flat_discount']
#                         cups.max_deduction = Decimal(5000)
#                         cups.created = timezone.make_aware(data['added_on'],
#                                 timezone.get_current_timezone()) if data['added_on'] else timezone.now()
#                         cups.save()
#                     elif data['type'] == 2:
#                         pass # no migrate
#                     elif data['type'] == 3:
#                         cups, created = Coupon.objects.get_or_create(
#                             code=data['code'],
#                             )
#                         cups.active = True
#                         cups.valid_from = timezone.make_aware(data['valid_from'],
#                                 timezone.get_current_timezone()) if data['valid_from'] else timezone.now()
#                         cups.valid_until = timezone.make_aware(data['valid_to'],
#                                 timezone.get_current_timezone()) if data['valid_to'] else timezone.now()
#                         cups.user_limit = 1
#                         if data['flat_discount']:
#                             cups.coupon_type = 'flat'
#                             cups.value = data['flat_discount']
#                         cups.max_deduction = Decimal(2000)
#                         cups.created = timezone.make_aware(data['added_on'],
#                                 timezone.get_current_timezone()) if data['added_on'] else timezone.now()
#                         cups.save()
#                     elif data['type'] == 4:
#                         pass # no migrate
#                     elif data['type'] == 5:
#                         cups, created = Coupon.objects.get_or_create(
#                             code=data['code'],
#                             )
#                         cups.active = True
#                         cups.valid_from = timezone.make_aware(data['valid_from'],
#                                 timezone.get_current_timezone()) if data['valid_from'] else timezone.now()
#                         cups.valid_until = timezone.make_aware(data['valid_to'],
#                                 timezone.get_current_timezone()) if data['valid_to'] else timezone.now()
#                         cups.user_limit = 1
#                         cups.coupon_type = 'flat'
#                         if data['pvid'] == 23:
#                             cups.value = Decimal(2399)
#                         elif data['pvid'] == 2083:
#                             cups.value = Decimal(1699)
#                         elif data['pvid'] == 3303:
#                             cups.value = Decimal(2899)
#                         else:
#                             cups.value = Decimal(0)
#                         cups.max_deduction = Decimal(5000)
#                         cups.created = timezone.make_aware(data['added_on'],
#                                 timezone.get_current_timezone()) if data['added_on'] else timezone.now()
#                         cups.save()
#                     count +=1
#                     if not count%500:
#                         print(count)    
#         except IntegrityError:
#             pass
#             print('Fail')

#         cursor.close()
#         db.close()
