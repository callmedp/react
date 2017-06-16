from django.conf.urls import url
from . import views


urlpatterns = [
	url(r'^vendor/(?P<vendor_id>\d+)/neworders/(?<order_item_id>\d+)/upload/$', views.NewOrdersVendorUpload.as_view(), name='neworders-vendor-upload'),	
]
