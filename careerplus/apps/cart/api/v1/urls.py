# django imports

from django.conf.urls import url

# local imports
from .views import CartOrderView

#  third party imports
from rest_framework import routers


router = routers.DefaultRouter()

urlpatterns = [
    url(r'^cart-order/$', CartOrderView.as_view())
]
