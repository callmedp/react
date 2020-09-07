import logging
from django.core.cache import cache
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        cache.set('email_sent_for_the_day', [])
        logging.getLogger('info_log').info("cache for emails sent is successfully cleared")