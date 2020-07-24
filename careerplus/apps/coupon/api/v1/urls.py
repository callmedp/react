# python imports

# django imports
# from django.conf.urls import url
from rest_framework import routers
from django.urls import re_path

# local imports

from .views import (CouponRedeemView, CouponRemoveView,ProductCouponDetail)

# inter app imports

# third party imports

router = routers.DefaultRouter()
app_name = 'coupon'
urlpatterns = [
    re_path(r'^redeem/$', CouponRedeemView.as_view()),
    re_path(r'^remove/$', CouponRemoveView.as_view()),
    re_path(r'^product-coupon/$',ProductCouponDetail.as_view())
]
