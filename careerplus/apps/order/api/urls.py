from django.conf.urls import url, include

urlpatterns = [
    url(r'^v1/order/', include(('order.api.v1.urls','order'), namespace='v1')),
]