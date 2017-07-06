from django.conf.urls import url, include

urlpatterns = [
    url(r'^api/', include('order.api.urls', namespace='api')),
]
