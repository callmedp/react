# from django.conf.urls import url, include
from django.urls import re_path, include
app_name = 'shine'
urlpatterns = [
    re_path(r'^api/', include('shine.api.urls', namespace='v1')),
]