import logging ,json
from decimal import Decimal
from django.core.management.base import BaseCommand

from emailers.email import SendMail
from shop.models import Skill, FunctionalArea, Product, Category
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
    redis_conn.delete('skills_set')
    for skill in skills:
        redis_conn.sadd('skills_set', skill.name)
    logging.getLogger('info_log').info(
        "{} skills added".format(skills.count()))
    func_areas = FunctionalArea.objects.filter(active=True)
    redis_conn.delete('func_area_set')
    for func_area in func_areas:
        redis_conn.sadd('func_area_set', func_area.name)
    logging.getLogger('info_log').info(
        "{} functional areas added".format(func_areas.count()))
    products = Product.objects.filter(active=True, is_indexable=True,is_indexed=True)
    redis_conn.delete('product_url_set')
    for product in products:
        redis_conn.sadd('product_url_set', json.dumps({ "name":product.heading ,
                                              "url":product.get_absolute_url(

                                              )}))
    logging.getLogger('info_log').info(
        "{} products added".format(products.count()))
    categories = Category.objects.filter(is_skill = True)
    redis_conn.delete('category_url_set')
    for category in categories:
        if category.get_absolute_url():
            redis_conn.sadd("category_url_set", json.dumps({
                "name":category.name, "url":category.get_absolute_url()}))
    logging.getLogger('info_log').info(
        "{} categories added".format(categories.count()))
