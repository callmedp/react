import logging
from decimal import Decimal
from django.core.management.base import BaseCommand

from emailers.email import SendMail
from shop.models import Skill, FunctionalArea, Product
from shine.core import ShineCandidateDetail
from linkedin.autologin import AutoLogin
from django.conf import settings
from django_redis import get_redis_connection


class Command(BaseCommand):
    """
        Daily Cron for updating search autocompletes
    """

    def handle(self, *args, **options):
        update_search_autocomplete()


def update_search_autocomplete():
    redis_conn = get_redis_connection('search_lookup')
    skills = Skill.objects.filter(active=True)
    for skill in skills:
        redis_conn.sadd('skills_set', skill.name)
    print('{} skills added'.format(skills.count()))
    func_areas = FunctionalArea.objects.filter(active=True)
    for func_area in func_areas:
        redis_conn.sadd('func_area_set', func_area.name)
    print('{} functional areas added'.format(func_areas.count()))
    products = Product.objects.filter(active=True, is_indexable=True)
    for product in products:
        redis_conn.sadd('product_set', product.name)
    print('{} products added'.format(products.count()))