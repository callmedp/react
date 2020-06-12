# python imports

# django imports
# from django.conf.urls import url
from rest_framework import routers
from django.urls import re_path

# local imports

from .views import (WalletRedeemView, WalletRemoveView)

# inter app imports

# third party imports

router = routers.DefaultRouter()
app_name = 'coupon'
urlpatterns = [
    re_path(r'^redeem/$', WalletRedeemView.as_view()),
    re_path(r'^remove/$', WalletRemoveView.as_view())
]
