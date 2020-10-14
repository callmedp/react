from django.urls import re_path, include

app_name = 'geolocation'

urlpatterns = [
    re_path(r'^v1/', include('geolocation.api.v1.urls', namespace='v1')),
]