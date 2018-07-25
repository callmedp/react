import MySQLdb

import logging
import time

from django.conf import settings
from django.utils import timezone

from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from ...models import Product
from review.models import Review


class Command(BaseCommand):
    """
        Custom command to Update Jobs form Shine to Products.
    """
    help = 'Custom command to Update Jobs form Shine to Products.'
    
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def handle(self, *args, **options):
        db_settings=settings.DATABASES.get('default')
    
        db_host = db_settings.get('HOST')
        if db_host is '':
            db_host = "localhost"
        db_name = db_settings.get('NAME')
        db_pwd = db_settings.get('PASSWORD')
        db_user = db_settings.get('USER')
        db = MySQLdb.connect(db_host,db_user,db_pwd,db_name)
        cursor = db.cursor()
        content_type_id = ContentType.objects.get(app_label="shop", model="product").id
        cursor.execute('select object_id, avg(average_rating), count(id) from review_review where content_type_id = '+str(content_type_id)+' group by (object_id);',{})

        result = cursor.fetchall()
        try:
            for row in result:
                prod = Product.objects.filter(pk=row[0])
                if len(prod) > 0:
                    prod[0].no_review = int(row[2])
                    prod[0].avg_rating = round(row[1],2)
                    prod[0].save()
                else:
                    continue
        except:
            logging.getLogger('info_log').info("Fail")
