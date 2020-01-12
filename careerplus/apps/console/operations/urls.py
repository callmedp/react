from django.conf.urls import url
from . import views

app_name = 'console'
urlpatterns = [
    url(r'^vendor/(?P<vendor_id>\d+)/neworders/(?P<orderitem_id>\d+)/upload/$', views.NewOrdersVendorUpload.as_view(), name='neworders-vendor-upload'), 
    url(r'^vendor/(?P<vendor_id>\d+)/neworders/upload/$', views.NewOrdersVendorUploadDetails.as_view(), name='neworders-vendor-upload-details'),
]
