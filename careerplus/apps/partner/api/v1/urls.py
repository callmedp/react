from django.conf.urls import url
from rest_framework import routers
from . import views

router = routers.SimpleRouter()

router.register(r'vendor', views.VendorViewSet)
router.register(r'vendorhierarchy', views.VendorHierarchyViewSet)
app_name = 'partner'
urlpatterns = router.urls + \
    [url(r'^vendor-list', views.VendorListApiView.as_view())

]
