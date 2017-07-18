from rest_framework import routers
from . import views

router = routers.SimpleRouter()

router.register(r'vendor', views.VendorViewSet)
router.register(r'vendorhierarchy', views.VendorHierarchyViewSet)

urlpatterns = router.urls
