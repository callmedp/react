#python imports
import logging
import time
from decimal import Decimal
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
    help = 'Custom command to Update Daily Reviews On Products.'
    
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
            if pid_rating_mapping.get(pid):
                pid_rating_mapping[pid].append(review.average_rating)
            else:
                pid_rating_mapping[pid] = [review.average_rating]

        all_products = Product.objects.filter(id__in=pid_rating_mapping.keys())

        for product in all_products:

            logging.getLogger('info_log').info("Updated ratings for product {}".format(product.id))
            num_reviews_to_consider = 1 if not product.no_review else product.no_review
            mul = num_reviews_to_consider * product.avg_rating
            # mul = product.avg_rating * product.no_review if product.no_review else product.avg_rating
            ratings = pid_rating_mapping[product.id]
            
            for rating in ratings:
                mul += Decimal(rating)

            new_avg_rating = round(mul / (num_reviews_to_consider + len(ratings)),2)
            product.avg_rating = new_avg_rating
            if product.type_flow == 1:
                prd_variations = product.variation.filter(siblingproduct__active=True,active=True)
                for prod in prd_variations:
                    product.no_review += prod.no_review
            elif product.type_flow == 3:
                prd_childs = product.childs.filter(childrenproduct__active=True,active=True)
                for prd in prd_childs:
                    product.no_review += prd.no_review
            product.no_review = product.no_review + len(ratings)
            product.save()

        logging.getLogger("info_log").info("Completed Ratings Update for Products.")


