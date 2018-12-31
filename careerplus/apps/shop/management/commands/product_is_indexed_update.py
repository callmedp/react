import logging
from django.core.management.base import BaseCommand
from shop.models import Product
from haystack.query import SearchQuerySet
from emailers.email import SendMail
import datetime


class Command(BaseCommand):
    """
    Custom command to Update course catalogue list in cache.
    """
    help = 'Update is_indexed column of product'

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def handle(self, *args, **options):
        start = datetime.datetime.now()
        TO = ['ritesh.bisht@hindustantimes.com', 'amar.kumar@hindustantimes.com',
              'animesh.sharma@hindustantimes.com']

        subject = 'Update is_indexed Column Of Product'
        try:
            indexed_product_id = list(SearchQuerySet().values_list('id', flat=True))
            products = Product.objects.filter(id__in=indexed_product_id)
            products.update(is_indexed=True)
            logging.getLogger('info_log').info(
                "{} products exists on solr and updated locally".format(products.count())
            )
            end = datetime.datetime.now()
            body = "Cron for updating solr products on local which started on {} has been completed successfully at {}".format(start, end)
            SendMail().base_send_mail(subject, body, to=TO, headers=None)
        except Exception as e:
            subject = 'Error Occured during cron Update is_indexed Column Of Product'
            SendMail().base_send_mail(subject, str(e), to=TO, headers=None)
