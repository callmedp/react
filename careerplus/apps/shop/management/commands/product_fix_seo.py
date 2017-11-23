import logging

from django.core.management.base import BaseCommand
from ...models import Product

class Command(BaseCommand):
    """
        Custom command to fix seo command.
    """
    help = 'Custom command to fix seo command'
    
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def handle(self, *args, **options):
        import re
        from shop.models import Product

        p_list = Product.objects.filter(product_class__slug='course', active=True)
        for prd in p_list:
            prd.heading = re.sub("Certification Course", "", prd.heading)
            prd.title = re.sub("Certification Course", "", prd.title)
            prd.save()