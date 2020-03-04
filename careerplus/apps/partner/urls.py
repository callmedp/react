# from django.conf.urls import url, include
from django.urls import re_path, include

urlpatterns = [
    re_path(r'^api/', include('partner.api.urls', namespace='api')),
]