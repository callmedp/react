import MySQLdb
import pandas as pd
import numpy as np
import math
from django.utils import timezone
from datetime import datetime
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import IntegrityError, transaction
from django.contrib.contenttypes.models import ContentType
from database.models import CPUser
from review.models import Review
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
        

        sql = """
            SELECT product_feedback.user_id AS uid, product_feedback.productvariation_id AS pid, product_feedback.published, 
                product_feedback.more_feedback, product_feedback.rating, product_feedback.added_on, product_feedback.title 
                FROM product_feedback 
                WHERE (product_feedback.productvariation_id IS NOT NULL AND product_feedback.user_id IS NOT NULL AND product_feedback.published = True );
            """
        sqlp = """
                SELECT shop_product.id AS slpid, shop_product.cpv_id AS pid FROM shop_product WHERE shop_product.cpv_id IS NOT NULL ;
                """
        sqlu = """
            SELECT database_cpuser.id AS sluid, database_cpuser.username, database_cpuser.email, database_cpuser.shine_id, database_cpuser.cp_id AS uid
            FROM database_cpuser WHERE database_cpuser.cp_id IS NOT NULL
            """
        df = pd.read_sql(sql,con=db)

        dfp = pd.read_sql(sqlp,con=db2)
        dfu = pd.read_sql(sqlu,con=db2)
        dfu['uid'] = dfu['uid'].apply(int)

        df = pd.merge(df, dfu, on='uid', how='left')
        df = pd.merge(df, dfp, on='pid', how='left')
         
        try:
            with transaction.atomic():
                for i, row in df.iterrows():
                    if row['sluid'] and row['slpid']:
                        product_type = ContentType.objects.get(
                            app_label='shop', model='product')
                        rating = math.ceil(row['rating']/2) if row['rating'] == row['rating'] else 2
                        content = row['more_feedback'] if row['more_feedback'] == row['more_feedback'] else ''
                        created = timezone.make_aware(row['added_on'],
                                    timezone.get_current_timezone()) if row['added_on'] else timezone.now()
                            
                        rr = Review.objects.create(
                            content_type=product_type,
                            object_id=row['slpid'],
                            user_email=row['email'],
                            user_id=row['shine_id'],
                            content=content,
                            average_rating=rating,
                            status=1,
                            )
                        rr.created = created
                        rr.save()
        except IntegrityError:
            pass
            print('Fail')
        db.close()
