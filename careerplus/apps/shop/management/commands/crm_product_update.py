import requests
import json
import logging
import time

from django.conf import settings
from django.utils import timezone

from django.core.management.base import BaseCommand
from optparse import make_option
from ...models import Product
from ...serializers import CRMProductSerializer


class Command(BaseCommand):
    """
        Custom command to Update Crm Products.
    """
    help = 'Update Products CRM'
    
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def handle(self, *args, **options):
        headers = {}
        lead = {}
        headers['content-type'] = 'application/json'
        headers['Authorization'] = 'Token ' + settings.SHINECPCRM_DICT.get('token')
        post_url = settings.SHINECPCRM_DICT.get('base_url') + \
            settings.SHINECPCRM_DICT.get('update_products_url')
        queryset_list = Product.objects.all()
        logging.getLogger('info_log').info("CRM - Total Products to be Updated {}".format(queryset_list.count()))
        success_count = 0

        for que in queryset_list:
            data_dict = CRMProductSerializer(que).data
            try:
                response = requests.post(
                    post_url,
                    data=json.dumps(data_dict),
                    headers=headers,
                    timeout=settings.SHINECPCRM_DICT.get('timeout'))
                
                if response.status_code == 200:
                    success_count += 1
                    logging.getLogger('info_log').info(
                        "{} Product Updated".format(que.id))

                else:
                    logging.getLogger('error_log').error(
                        "Product Update Failed {} - {}".format(que.id,response.content))
            except Exception as e:
                logging.getLogger('error_log').error("%s" % str(e))

        logging.getLogger('info_log').info("CRM - Total Products successfully Updated {}".format(success_count))



