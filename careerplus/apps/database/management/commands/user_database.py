# import MySQLdb
# import csv
# import pandas as pd
# import numpy as np
# from django.utils import timezone
# from django.conf import settings
# from database.models import CPUser
# from django.core.management.base import BaseCommand
# from django.db import IntegrityError, transaction
# from users.models import User

# class Command(BaseCommand):
#     help = ('Get User Database from old Careerplus')

#     def handle(self, *args, **options):
#         """
#             User Migration From OLD Careerplus
#             Only Users with email are getting migrated
#             User Migrated only for Orders places after "1-04-2014" 
#         """
#         db_settings=settings.DATABASES.get('oldDB')
    
#         db_host = db_settings.get('HOST')
#         if db_host is '':
#             db_host = "localhost"
#         db_name = db_settings.get('NAME')
#         db_pwd = db_settings.get('PASSWORD')
#         db_user = db_settings.get('USER')
#         db = MySQLdb.connect(db_host,db_user,db_pwd,db_name)
#         cursor = db.cursor()

#         df = pd.read_csv('CP_staffusers_for_migration.csv', sep=',')
#         df2 = pd.read_csv('CP_staffusers.csv')
#         # try:
#         #     with transaction.atomic():
#         #         from django.contrib.auth.models import BaseUserManager
#         #         manager = BaseUserManager()
                
#         #         for i, row in df.iterrows():
#         #             if row['email'] == row['email']:
#         #                 if User.objects.filter(email=row['email']).exists():
#         #                     pass
#         #                 else:
#         #                     email = manager.normalize_email(row['email'])
#         #                     first_name = row['first_name'] if row['first_name'] == row['first_name'] else ''
#         #                     last_name = row['last_name'] if row['last_name'] == row['last_name'] else ''
#         #                     user_dict = {
#         #                         'name': first_name + ' ' + last_name,
#         #                         'email': row['email'],
#         #                         'cp_id': row['id'],
#         #                         'is_staff': False,
#         #                         'is_active': True,
#         #                         'date_joined': timezone.now(), 
#         #                         'last_login': timezone.now()
#         #                     }
#         #                     user = User(**user_dict)
#         #                     user.set_password('$hineP!us')
#         #                     user.save()

#         #         for i, row in df2.iterrows():
#         #             if row['email'] == row['email']:
#         #                 if User.objects.filter(email=row['email']).exists():
#         #                     pass
#         #                 else:
#         #                     email = manager.normalize_email(row['email'])
#         #                     first_name = row['first_name'] if row['first_name'] == row['first_name'] else ''
#         #                     last_name = row['last_name'] if row['last_name'] == row['last_name'] else ''
#         #                     user_dict = {
#         #                         'name': first_name + ' ' + last_name,
#         #                         'email': row['email'],
#         #                         'cp_id': row['id'],
#         #                         'is_staff': False,
#         #                         'is_active': False,
#         #                         'date_joined': timezone.now(), 
#         #                         'last_login': timezone.now()
#         #                     }
#         #                     user = User(**user_dict)
#         #                     user.set_password('$hineP!us')
#         #                     user.save()
#         # except IntegrityError:
#         #     print(row)
#         #     print('Fail')
#         sql = """
#                 SELECT auth_user.email as Email, cart_userprofile.shine_id as ShineID, cart_userprofile.mobile as Mobile, theme_country.isd_code as Country_Code 
#                 FROM auth_user 
#                 LEFT OUTER JOIN cart_userprofile ON ( auth_user.id = cart_userprofile.user_id ) 
#                 LEFT OUTER JOIN theme_country ON ( cart_userprofile.country_id = theme_country.id ) 
#                 WHERE  (auth_user.date_joined >= '2016-04-1 00:00:00' AND auth_user.email IS NOT NULL AND cart_userprofile.mobile IS NOT NULL AND NOT (auth_user.email =  '') AND NOT (cart_userprofile.mobile =  '' AND cart_userprofile.mobile IS NOT NULL))
#                 ORDER BY auth_user.date_joined DESC
#                 """
#         df = pd.read_sql(sql, con=db)
#         df = df.drop_duplicates(subset=['Email'], keep='last')
#         user_df = pd.read_csv('cleaned_present_user.csv', sep=',')
#         user_df = user_df[['Email', 'C_ID']]
#         user_df = user_df.drop_duplicates(subset=['Email'], keep='last')
#         df = pd.merge(df, user_df, how='left', on='Email')
#         df = df[df.C_ID.isnull()]
#         df.to_csv('new_absent_user.csv', index=False, encoding='utf-8')

#         # try:
#         #     with transaction.atomic():
#         #         for i,row in df.iterrows():
#         #             CPUser.objects.create(
#         #                 username=row['username'] if row['username'] else '',
#         #                 email=row['email'] if row['email'] else '',
#         #                 shine_id=row['shine_id'] if row['shine_id'] else '',
#         #                 cp_id=row['id'] if row['id'] else '',
#         #                 mobile=row['mobile'] if row['mobile'] else '',
#         #                 country=row['isd_code'] if row['isd_code'] else '')
#         # except IntegrityError:
#         #     print(i, row)
#         #     print('Fail')
#         # except:
#         #     print(i, row)
#         #     print('Wut')
#         # cursor.close()
#         # db.close()
        
#         # generated_file = open('check_user.csv', 'w')
#         # with open('CP_Data.csv', 'r', encoding='utf-8', errors='ignore') as upload:
#         #     uploader = csv.DictReader(upload, delimiter=',', quotechar='"')
#         #     fieldnames = uploader.fieldnames
#         #     fieldnames.append('Matching')
#         #     csvwriter = csv.DictWriter(generated_file, delimiter=',', fieldnames=fieldnames)
#         #     csvwriter.writerow(dict((fn, fn) for fn in fieldnames))
                        
#         #     for row in uploader:
#         #         email = row.get('Email')
#         #         ShineID = row.get('Shine_Id')
#         #         user = CPUser.objects.filter(email=email)[0] if CPUser.objects.filter(email=email) else None
#         #         if user:    
#         #             if ShineID:    
#         #                 if user.shine_id:    
#         #                     if user.shine_id == ShineID:
#         #                         row['Matching'] = 'Yes'
#         #                     else:
#         #                         row['Matching'] = 'No'
#         #                 else:
#         #                     row['Matching'] = 'Yes'
#         #             else:
#         #                 row['Matching'] = "Don't Know"
#         #             csvwriter.writerow(row)
#         #         else:
#         #             continue
        
        
#         # users = CPUser.objects.all()
#         # generated_file = open('order_user.csv', 'w')
#         # fieldnames = ['Email', 'ShineID', 'Mobile', 'Country_Code']
#         # csvwriter = csv.DictWriter(generated_file, delimiter=',', fieldnames=fieldnames)
#         # csvwriter.writerow(dict((fn, fn) for fn in fieldnames))
                                
#         # for  i, row in df.iterrows():
#         #     try:
#         #             crow = {}
#         #             crow['Email'] = row['email'] 
#         #             crow['ShineID'] = row['shine_id']
#         #             crow['Mobile'] = row['mobile'] 
#         #             crow['Country_Code'] = row['isd_code']
                    
                    
#         #             csvwriter.writerow(crow)
#         #     except:
#         #         continue

#         # df = pd.read_csv('cleaned_present_user.csv', sep=',')
#         # df2 = pd.read_csv('new_absent_user.csv',sep=',')


#         pass