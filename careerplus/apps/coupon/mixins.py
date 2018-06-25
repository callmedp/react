import datetime

from coupon.models import Coupon
from django.utils import timezone
from django.conf import settings


class CouponMixin(object):
    def create_feature_coupon(self, users=[]):
        coupon_obj = Coupon.objects.create_coupon(
            coupon_type='percent',
            value=100,
            users=users,
            valid_until=None,
            prefix="fp",
            campaign=None,
            user_limit=1
        )
        # coupon_obj.min_purchase = coupon_amount
        # coupon_obj.max_deduction = coupon_amount
        on_products = settings.FEATURE_PROFILE_PRODUCTS
        today = timezone.now()
        expiry = today + datetime.timedelta(days=90)
        coupon_obj.valid_from = today
        coupon_obj.valid_until = expiry
        coupon_obj.coupon_scope = 1
        coupon_obj.products = on_products
        coupon_obj.save()
        return coupon_obj