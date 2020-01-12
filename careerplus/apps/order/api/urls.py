from django.conf.urls import url, include
app_name ='order'
urlpatterns = [
    url(r'^v1/order/', include('order.api.v1.urls', namespace='v1')),
]