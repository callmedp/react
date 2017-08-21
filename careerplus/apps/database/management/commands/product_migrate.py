import MySQLdb
import pandas as pd
import numpy as np
from decimal import Decimal
from django.utils import timezone
from datetime import datetime
from django.conf import settings
from database.models import CPUser
from django.core.management.base import BaseCommand
from django.db import IntegrityError, transaction
from shop.models import *
from partner.models import *
from users.models import User


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
        cursor = db.cursor()

        # sql = """
        #         SELECT auth_user.id, auth_user.username, auth_user.first_name, auth_user.email, auth_user.is_active, cart_userprofile.mobile, cart_userprofile.usersite 
        #         FROM auth_user 
        #         LEFT OUTER JOIN cart_userprofile ON ( auth_user.id = cart_userprofile.user_id ) 
        #         WHERE auth_user.id IN (SELECT DISTINCT U0.owner_id FROM cart_product U0);
        #     """
        # cursor.execute(sql,{})
        # result = cursor.fetchall()
        # try:
        #     with transaction.atomic():
        #         count = 0
        #         for row in result:
        #             data = {
        #                     'id': row[0],
        #                     'username': row[1],
        #                     'email': row[3],
        #                     'first_name': row[2],
        #                     'active': row[4],
        #                     'mobile': row[5],
        #                     'website': row[6],
        #                 }
        #             ven, created = Vendor.objects.get_or_create(
        #                 name=data['username'],
        #                 cp_id=data['id'],
        #                 )
        #             ven.email = data['email']
        #             if data['mobile']:
        #                 ven.mobile=data['mobile']
        #             if data['website']:
        #                 ven.website=data['website']
        #             ven.save()
        # except IntegrityError:
        #     pass
        #     print(row)
        #     print('Fail')
        

        sql = """
            SELECT 
                cart_product.id AS 'pid', cart_productvariation.id AS 'pvid',cart_product.name AS 'pname',
                cart_product.price AS 'pprice', cart_product.short_desc, cart_product.long_desc, 
                cart_product.parent_id, cart_product.is_allocable, cart_product.country_id,
                cart_product.is_addon, cart_product.is_service,
                cart_product.added_on, cart_product.modified_on,
                cart_product.is_international, cart_product.to_boost, cart_product.to_highlight,
                cart_product.to_feature, cart_product.is_free_product,
                cart_product.product_trial, cart_product.is_active, cart_product.profile_update_required, 
                cart_product.salary_increment, cart_product.salary_candidates, cart_product.feedback_eligible, 
                cart_product.priority_in_emailer, cart_product.featured_eligible,
                cart_product.featured_days, cart_product.facebook_remarketing ,
                cart_product.owner_id, cart_product.country_id, cart_productvariation.name AS 'pvname',
                cart_productvariation.type_of_product, cart_productvariation.sub_type_of_product,
                cart_productvariation.vendor_pv_id, 
                cart_productvariation.price AS 'pvprice', cart_productvariation.aed_price, cart_productvariation.usd_price,
                cart_productvariation.fake_price, cart_productvariation.fake_usd_price, cart_productvariation.fake_aed_price,
                cart_productvariation.experience_level, cart_productvariation.sample_document, 
                cart_productvariation.email_cc, cart_productvariation.with_certificate,
                cart_productvariation.description, 
                cart_productvariation.introduction, cart_productvariation.about,
                cart_productvariation.what_you_get,  cart_productvariation.update_combo_price,
                cart_productvariation.combo_discount, cart_productvariation.frequently_bought, 
                cart_productvariation.cart_description 
            FROM cart_product 
            LEFT OUTER JOIN cart_productvariation ON ( cart_product.id = cart_productvariation.product_id );
            """        
        df = pd.read_sql(sql, con=db)
        product_withpv = df.loc[df['pvid'].notnull()]
        
        df2 = product_withpv[['pid', 'pvid']]
        df2 = df2.groupby('pid').count()

        with_variation = df2[df2['pvid']> 1].index
        without_variation = df2[df2['pvid']< 2].index
        
        product_standalone = product_withpv.loc[df['pid'].isin(without_variation)]
        product_variation = product_withpv.loc[df['pid'].isin(with_variation)]
        product_withoutpv = df.loc[df['pvid'].isnull()]
        try:
            with transaction.atomic():
                for i, row in product_withoutpv.iterrows():
                    psc, created = ProductScreen.objects.get_or_create(
                        name=row['pname'],
                        cp_id=row['pid'])
                    try:
                        vendor = Vendor.objects.get(pk=row['owner_id'])
                    except:
                        vendor = Vendor.objects.get(name='ops')
                    product_class = ProductClass.objects.get(
                        slug='other')
                    type_flow = 2
                    if row['is_international']:
                        type_flow = 4
                    elif row['to_boost']:
                        type_flow = 7
                    elif row['to_feature']:
                        type_flow = 5
                    elif row['profile_update_required']:
                        type_flow = 4


                    psc.inr_price = str(row['pprice']) if row['pprice'] == row['pprice'] else '0'
                    psc.type_product = 4
                    psc.product_class = product_class
                    psc.created = timezone.make_aware(datetime.strptime(str(row['added_on']), "%Y-%m-%d %H:%M:%S"),
                        timezone.get_current_timezone()) if str(row['added_on']) else timezone.now()
                    psc.about = row['short_desc'] if row['short_desc'] else '' 
                    psc.description = row['long_desc'] if row['long_desc'] else ''
                    psc.type_flow = type_flow
                    psc.save()    
                    prd = psc.create_product()
                    prd.created = timezone.make_aware(datetime.strptime(str(row['added_on']), "%Y-%m-%d %H:%M:%S"),
                        timezone.get_current_timezone()) if str(row['added_on']) else timezone.now()
                    prd.type_flow = type_flow
                    prd.about = row['short_desc'] if row['short_desc'] else ''
                    prd.description = row['long_desc'] if row['long_desc'] else ''
                    prd.archive_json = dict(row.to_dict())
                    prd.save()
        except Exception as e:
            print(e)
                    
        cursor.close()
        db.close()
