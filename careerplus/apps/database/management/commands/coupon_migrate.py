import MySQLdb
from django.conf import settings
from database.models import CPUser
from django.core.management.base import BaseCommand
from django.db import IntegrityError, transaction


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

        sql = """
            SELECT coupon_coupon.code, coupon_coupon.user, coupon_coupon.discount, coupon_coupon.flat_discount, coupon_coupon.added_on, coupon_coupon.valid_from, coupon_coupon.valid_to, coupon_coupon.description, coupon_coupon.consumed_by_id, coupon_coupon.for_user_id, coupon_coupon.type, coupon_coupon.active, coupon_coupon.max_allowed_usage, coupon_coupon.usage_count, coupon_coupon.product_id, coupon_coupon.productvariation_id, coupon_coupon.category_id, coupon_coupon.multipleproduct_ids, coupon_coupon.for_order_id FROM coupon_coupon WHERE coupon_coupon.code IN (SELECT DISTINCT U0.coupon_id FROM cart_order U0 WHERE U0.coupon_id IS NOT NULL) ORDER BY coupon_coupon.added_on DESC"""
        cursor.execute(sql,{})
        result = cursor.fetchall()
        try:
            with transaction.atomic():
                for row in result:
                    data = {
                            'code': row[0],
                            'user': row[1],
                            'discount': row[2],
                            'flat_discount': row[3],
                            'added_on': row[4],
                            'valid_from': row[5],
                            'valid_to': row[6],
                            'description': row[7],
                            'consumed_by_id': row[8],
                            'for_user_id': row[8],
                            'type': row[9],
                            'active': row[10],
                            'max_allowed_usage': row[11],
                            'usage_count': row[12],
                        }
                    print(data)          
        except IntegrityError:
            pass
            print('Fail')
        cursor.close()
        db.close()
