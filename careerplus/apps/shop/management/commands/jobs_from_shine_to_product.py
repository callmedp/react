import requests
import json
import logging
import time

from django.conf import settings
from django.utils import timezone

from django.core.management.base import BaseCommand
from ...models import Product


class Command(BaseCommand):
    """
        Custom command to Update Jobs form Shine to Products.
    """
    help = 'Custom command to Update Jobs form Shine to Products.'
    
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def handle(self, *args, **options):
        
        queryset_list = Product.browsable.filter(product_class__slug__in=['course', 'assessment'])
        count = 0
        for prod in queryset_list:
            data_dict = {}
            try:
                url = "https://www.shine.com/api/v2/search/simple/?q={}".format(prod.slug)
                response = requests.get(url)
                if response.status_code == 200:
                    response_data = response.json()
                    data_dict.update({
                        'job_count': int(response_data['count']),
                    })
            except Exception as e:
                logging.getLogger('error_log').error(str(e))
            if data_dict.get('job_count', 0):
                prod.num_jobs = data_dict.get('job_count', 0)
                prod.save()
                count += 1
                if not count % 10:
                    logging.getLogger('info_log').info("{}".format(count))
            time.sleep(0.1)
