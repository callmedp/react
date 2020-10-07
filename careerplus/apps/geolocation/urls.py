# from django.conf.urls import url, include
from django.urls import re_path, include

app_name = 'geolocation'
urlpatterns = [
    re_path(r'^api/', include('geolocation.api.urls', namespace='api')),
]
