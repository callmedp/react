from django.conf.urls import url, include

urlpatterns = [
    url(r'^v1/', include(('geolocation.api.v1.urls','geolocation'), namespace='v1')),
]