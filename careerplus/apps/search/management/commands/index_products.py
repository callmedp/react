import logging
from django.core.management.base import BaseCommand
from django.conf import settings

from shop.models import Skill, FunctionalArea, Product,Category
from django.conf import settings
from django_redis import get_redis_connection
import requests
from django.core.management import call_command
from django.core.cache import cache

class Command(BaseCommand):
    """
        Daily Cron for updating search autocompletes
    """

    def add_arguments(self, parser):
        parser.add_argument(
            '--noinput', action='store_false', dest='interactive', default=True,
            help='If provided, no prompts will be issued to the user and the data will be wiped out.'
        )
        parser.add_argument(
            '-u', '--using', action='append', default=[],
            help='Update only the named backend (can be used multiple times). '
                 'By default all backends will be updated.'
        )
        parser.add_argument(
            '-k', '--workers', default=0, type=int,
            help='Allows for the use multiple workers to parallelize indexing. Requires multiprocessing.'
        )
        parser.add_argument(
            '--nocommit', action='store_false', dest='commit',
            default=True, help='Will pass commit=False to the backend.'
        )
        parser.add_argument(
            '-b', '--batch-size', dest='batchsize', type=int,
            help='Number of items to index at once.'
        )

    def handle(self, *args, **options):
        cache_list = []
        if settings.IS_LIVE:
            response = requests.get('http://10.136.2.25:8989/solr/prdt/replication?command=disablereplication')
            logging.getLogger('info_log').info(
            "Disabled Replication on master. Response: {} {}".format(
                response, response.__dict__))
        for obj in Product.objects.values_list('id', flat=True):
            cache_list.append("product_{}_absolute_url".format(obj))
            cache_list.append("context_product_detail_" + str(obj))
            cache_list.append("detail_db_product_" + str(obj))
            cache_list.append("detail_solr_product_" + str(obj))
            cache_list.append("category_main_" + str(obj))
        for obj in Category.objects.values_list('id',flat=True):
            cache_list.append('cat_absolute_url' + str(obj))
        cache_list.append('course_catalogue')
        cache.delete_many(cache_list)
        call_command('rebuild_index', **options)
        if settings.IS_LIVE:
            response = requests.get('http://10.136.2.25:8989/solr/prdt/replication?command=enablereplication')
            logging.getLogger('info_log').info(
            "Enabled Replication on master. Response: {} {}".format(
                response, response.__dict__))
        response = requests.get('http://172.22.65.36:8983/solr/prdt/replication?command=fetchIndex')
        print("Fetched indexes on slave. Response:", response, response.__dict__)
