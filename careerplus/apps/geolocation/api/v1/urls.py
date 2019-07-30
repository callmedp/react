# python imports


# django imports
from django.conf.urls import url

# local imports

from .views import (CountryListView, CurrencyViewSet, CityViewSet)
# inter app imports

# third party imports
from rest_framework import routers

router = routers.DefaultRouter()

router.register(r'currency', CurrencyViewSet)
router.register(r'city', CityViewSet)

urlpatterns = router.urls

urlpatterns = [
    url(r'^country/$', CountryListView.as_view())

]
