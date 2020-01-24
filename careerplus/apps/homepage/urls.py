# from django.conf.urls import url
from django.urls import re_path,include

urlpatterns = [
    re_path(r'^api/', include('homepage.api.v1.urls', namespace='v1')),
]