#python imports
import logging
import time
from datetime import datetime,timedelta

#django imports
from django.conf import settings
from django.utils import timezone
from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType

#local imports
from ...models import Product

#inter app imports
from review.models import Review

#third party imports

class Command(BaseCommand):
    """
        Custom command to Update Jobs form Shine to Products.
    """
    help = 'Custom command to Update Dail;y Reviews On Products.'
    
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def handle(self, *args, **options):
        logging.getLogger("info_log").info("Started Ratings Update for Products.")

        content_type_id = ContentType.objects.get(app_label="shop", model="product").id
        todays_reviews = Review.objects.filter(created__gte=datetime.now()-timedelta(days=1),\
            content_type_id=content_type_id,status=1)

        logging.getLogger('info_log').info("Total Reviews under consideration {}".format(todays_reviews.count()))

        pid_rating_mapping = {}
        for review in todays_reviews:
            pid = review.object_id
            if pid_rating_mapping.has_key(pid):
                pid_rating_mapping[pid].append(review.average_rating)
            else:
                pid_rating_mapping[pid] = [review.average_rating]

        all_products = Product.objects.filter(id__in=pid_rating_mapping.keys())

        for product in all_products:
            logging.getLogger('info_log').info("Updated ratings for product {}".format(product.id))
            mul = product.avg_rating * product.no_review
            ratings = pid_rating_mapping[product.id]
            
            for rating in ratings:
                mul += rating

            new_avg_rating = round(mul / (product.no_review + len(ratings)),2)
            product.avg_rating = new_avg_rating
            product.no_review = product.no_review + len(ratings)
            product.save()

        logging.getLogger("info_log").info("Completed Ratings Update for Products.")


