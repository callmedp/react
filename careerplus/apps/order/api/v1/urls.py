from rest_framework import routers
from . import views

router = routers.SimpleRouter()

router.register(r'orderitem', views.OrderItemViewSet)

urlpatterns = router.urls
