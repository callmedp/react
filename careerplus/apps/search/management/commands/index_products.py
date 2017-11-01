import logging
from django.core.management.base import BaseCommand

from shop.models import Skill, FunctionalArea, Product
from django.conf import settings
from django_redis import get_redis_connection
import requests
from django.core.management import call_command


class Command(BaseCommand):
    """
        Daily Cron for updating search autocompletes
    """

    def handle(self, *args, **options):
        response = requests.get('http://172.22.65.35:8983/solr/prdt/replication?command=disablereplication')
        print("Disabled Replication on master. Response:", response, response.__dict__)
        call_command('rebuild_index', **options)
        response = requests.get('http://172.22.65.35:8983/solr/prdt/replication?command=enablereplication')
        print("Enabled Replication on master. Response:", response, response.__dict__)
        response = requests.get('http://172.22.65.36:8983/solr/prdt/replication?command=fetchIndex')
        print("Fetched indexes on slave. Response:", response, response.__dict__)
