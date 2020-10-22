# import MySQLdb
# import pandas as pd
# import numpy as np
# import math
# from django.utils import timezone
# from datetime import datetime
# from django.conf import settings
# from django.core.management.base import BaseCommand
# from django.db import IntegrityError, transaction
# from django.contrib.contenttypes.models import ContentType
# from database.models import CPUser
# from review.models import Review
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
        

#         sql = """
#             SELECT product_feedback.user_id AS uid, auth_user.email as Email, product_feedback.productvariation_id AS pid, product_feedback.published, 
#                 product_feedback.more_feedback, product_feedback.rating, product_feedback.added_on, product_feedback.title 
#                 FROM product_feedback
#                 LEFT JOIN auth_user
#                 ON product_feedback.user_id = auth_user.id 
#                 WHERE (product_feedback.productvariation_id IS NOT NULL AND product_feedback.user_id IS NOT NULL AND product_feedback.published = True );
#             """
#         sqlp = """
#                 SELECT shop_product.id AS slpid, shop_product.cpv_id AS pid FROM shop_product WHERE shop_product.cpv_id IS NOT NULL ;
#                 """
#         df = pd.read_sql(sql,con=db)
#         dfp = pd.read_sql(sqlp,con=db2)
#         user_df = pd.read_csv('cleaned_present_user.csv', sep=',')
#         user_df = user_df[['Email', 'C_ID']]
#         user_df = user_df.drop_duplicates(subset=['Email'], keep='last')
        
#         df = pd.merge(df, user_df, on='Email', how='left')
#         df = pd.merge(df, dfp, on='pid', how='left')
         
#         try:
#             with transaction.atomic():
#                 for i, row in df.iterrows():
#                     if not i%50:
#                         print(i)
#                     if row['slpid']:
#                         product_type = ContentType.objects.get(
#                             app_label='shop', model='product')
#                         rating = math.ceil(row['rating']/2) if row['rating'] == row['rating'] else 2
#                         content = row['more_feedback'] if row['more_feedback'] == row['more_feedback'] else ''
#                         created = timezone.make_aware(row['added_on'],
#                                     timezone.get_current_timezone()) if row['added_on'] else timezone.now()
#                         row['Email'] = row['Email'] if row['Email'] and row['Email'] == row['Email'] else '' 
#                         row['C_ID'] = row['C_ID'] if row['C_ID'] and row['C_ID'] == row['C_ID'] else '' 
                        
#                         rr = Review.objects.create(
#                             content_type=product_type,
#                             object_id=row['slpid'],
#                             user_email=row['Email'],
#                             user_id=row['C_ID'],
#                             content=content,
#                             average_rating=rating,
#                             status=1,
#                             )
#                         rr.created = created
#                         rr.save()
#         except IntegrityError:
#             pass
#             print('Fail')
#         db.close()
