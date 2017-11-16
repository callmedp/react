# import MySQLdb
# import json
# import pandas as pd
# import numpy as np
# import requests
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
        
#         # df = pd.read_csv('order_user.csv', sep=',')
#         # df2 = pd.read_csv('shine_id.csv', sep=',', names=['Email', 'C_ID'])
#         # df = pd.merge(df,df2,on='Email', how='left')
#         # df['OK'] = df.apply(lambda x: x['C_ID'] == x['C_ID'], axis=1)
#         # df_match = df[df['OK'] == True ]
#         # df_nomatch = df[df['OK'] == False ]
#         # df_match.to_csv('present_user.csv', index=False, encoding='utf-8')
#         SHINE_API_URL = "https://mapi.shine.com"
        
#         client_access_url = SHINE_API_URL + '/api/v2/client/access/?format=json'
#         client_data = {'key': 'ZiHCJeTKh4EppsrOEHXIQPd2OKvV4JWrlKql0Y1JONE',
#             'secret': 'QdEhIXFmhlHQdveZB1h9u9xxnfvFleET6bNUPlKYwU4'}
#         client_access_resp = requests.post(client_access_url, data=client_data)
#         client_access_resp_json = client_access_resp.json()
#         client_token = client_access_resp_json.get('access_token', None)
        
#         user_access_url = SHINE_API_URL + '/api/v2/user/access/?format=json'
#         user_data = {"email": 'scpapiuser@gmail.com', "password": 'tarun@123'}
#         user_access_resp = requests.post(user_access_url, data=user_data)
#         user_access_resp_json = user_access_resp.json()
#         access_token = user_access_resp_json.get('access_token', None)
        
#         detail_headers = {"User-Access-Token": access_token,
#                "Client-Access-Token": client_token,
#                "User-Agent": 'Mozilla/5.0 (Linux; Android 4.1.1; Galaxy Nexus Build/JRO03C) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19'}
                    
#         df_nomatch = pd.read_csv('cleaned_present_user.csv', sep=',')
        
#         from django.contrib.auth.models import BaseUserManager
#         manager = BaseUserManager()
#         try:
#             for i, row in df_nomatch.iterrows():
#                 if not i%50:
#                     print(i)
#                 # password = manager.make_random_password(length=10, allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ123456789')
#                 email = manager.normalize_email(row['Email'])
#                 email = email.lower()
#                 # try:
#                 #     country = str(int(row['Country_Code'].replace('+', '')))
#                 # except:
#                 #     country = '91' 

#                 # post_url = "{}/api/v2/web/candidate-profiles/?format=json".format(SHINE_API_URL)
#                 # headers = {'Content-Type': 'application/json'}
#                 # post_data = {
#                 #     "email": email,
#                 #     "raw_password": password,
#                 #     "cell_phone": row['Mobile'],
#                 #     "country_code": country,
#                 #     "vendor_id": 173,
#                 #     "is_job_seeker": False,
#                 # }
#                 # shine_id = None
#                 # response = requests.post(
#                 #     post_url, data=json.dumps(post_data), headers=headers)
#                 # df_nomatch.loc[df_nomatch.Email == row['Email'], 'RError'] = str(response.json())
#                 # if response.status_code == 201:
#                 #     response_json = response.json()
#                 #     shine_id = response_json.get("id", None)
#                 # elif "non_field_errors" in response.json():
#                 shine_id_url = SHINE_API_URL + "/api/v2/candidate/career-plus/email-detail/?email=" +\
#                     email + "&format=json"
#                 shine_id_response = requests.get(
#                     shine_id_url, headers= detail_headers,
#                     timeout=30)
#                 if shine_id_response and shine_id_response.status_code == 200 and shine_id_response.json():
#                     shine_id_json = shine_id_response.json()
#                     if shine_id_json:
#                         shine_id = shine_id_json[0].get("id", None)
#                 # df_nomatch.loc[df_nomatch.Email == row['Email'], 'LError'] = str(shine_id_response.json())
#                 if shine_id:
#                     df_nomatch.loc[[i], 'Email'] = email
#                     df_nomatch.loc[[i], 'C_ID'] = shine_id
#         except:
#             pass
#         finally:
#             df_nomatch = df_nomatch.drop_duplicates(subset=['Email'], keep='last')
#             df_nomatch.to_csv('cleaned_present_user.csv', index=False, encoding='utf-8')
            
#             # user_df = pd.read_csv('cleaned_present_user.csv', sep=',')
#             # user_df = user_df[['Email', 'C_ID']]
#             # user_df = user_df.drop_duplicates(subset=['Email'], keep='last')
#             # df2 = df_nomatch[~df_nomatch.C_ID.isnull()]
#             # df2 = df2[['Email', 'C_ID']]
#             # df2 = df2.drop_duplicates(subset=['Email'], keep='last')
#             # user_df = user_df.append(df2, ignore_index=True)
#             # user_df = user_df.drop_duplicates(subset=['Email'], keep='last')
#             # user_df.to_csv('cleaned_present_user.csv', index=False, encoding='utf-8')
#             # df_nomatch = df_nomatch[df_nomatch.C_ID.isnull()]
#             # df_nomatch.to_csv('new_absent_user.csv', index=False, encoding='utf-8')
#             