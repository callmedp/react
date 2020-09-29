import logging, requests
from django.utils import timezone
from django.core.management.base import BaseCommand
from django.core.cache import cache
from django.conf import settings

class Command(BaseCommand):
    """
        refresh payment tracking cache
    """
    help = "refresh payment tracking cache"
    
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def handle(self, *args, **options):
        try:
            payment_cache = cache.get('tracking_payment_action', {})
            cache_result = cache.get('tracking_payment_action', {})

            interval = timezone.now() - timezone.timedelta(hours = 1)

            for u_id in payment_cache:
                cache_u_id = payment_cache.get(str(u_id),{})
                date_time = cache_u_id.get('date_time', '')
                if not date_time or date_time > interval:
                    continue
                del cache_result[str(u_id)]

            cache.set('tracking_payment_action',cache_result, timeout=None)
            logging.getLogger('info_log').info("tracking_payment_action updated")
        except Exception as e:
            logging.getLogger('error_log').error("failed tracking_payment_action updated")




        
