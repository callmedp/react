from rest_framework import routers
from . import views

router = routers.SimpleRouter()

router.register(r'currency', views.CurrencyViewSet)
router.register(r'city', views.CityViewSet)

urlpatterns = router.urls
