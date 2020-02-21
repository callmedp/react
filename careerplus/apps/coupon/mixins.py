import datetime
import logging

from decimal import Decimal

from coupon.models import Coupon
from django.utils import timezone
from django.conf import settings

from haystack.query import SearchQuerySet


class CouponMixin(object):
    def create_feature_coupon(self, users=[]):
        coupon_obj = None
        try:
            on_products = settings.FEATURE_PROFILE_PRODUCTS
            fp_product = on_products[0]
            fp_sqs = SearchQuerySet().filter(id=fp_product)
            fp_sqs = fp_sqs[0]
            FP_COUPON_FLAT_AMOUNT = Decimal(fp_sqs.pPinb)
            coupon_obj = Coupon.objects.create_coupon(
                coupon_type='flat',
                value=FP_COUPON_FLAT_AMOUNT,
                users=users,
                valid_until=None,
                prefix="fp",
                campaign=None,
                user_limit=1
            )
            # coupon_obj.min_purchase = coupon_amount
            # coupon_obj.max_deduction = coupon_amount
            today = timezone.now()
            expiry = today + datetime.timedelta(days=90)
            coupon_obj.valid_from = today
            coupon_obj.valid_until = expiry
            coupon_obj.coupon_scope = 1
            coupon_obj.products.set(on_products)
            coupon_obj.save()
        except Exception as e:
            logging.getLogger('error_log').error(
                "Unable to get feature product - %s" % str(e))
        return coupon_obj