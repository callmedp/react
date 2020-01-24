# from django.conf.urls import url, include
from django.urls import re_path,include
app_name ='order'
urlpatterns = [
    re_path(r'^v1/order/', include('order.api.v1.urls', namespace='v1')),
]