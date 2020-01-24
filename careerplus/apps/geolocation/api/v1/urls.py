# python imports


# django imports
# from django.conf.urls import url
from django.urls import re_path

# local imports

from .views import (CountryListView, CurrencyViewSet, CityViewSet, CountryValidationView)
# inter app imports

# third party imports
from rest_framework import routers

router = routers.DefaultRouter()

router.register(r'currency', CurrencyViewSet)
router.register(r'city', CityViewSet)

urlpatterns = router.urls

app_name = "geolocation"
urlpatterns = [
    re_path(r'^country/$', CountryListView.as_view()),
    re_path(r'^validate/$',CountryValidationView.as_view())
]
