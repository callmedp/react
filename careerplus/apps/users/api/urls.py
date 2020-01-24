# from django.conf.urls import url, include
from django.urls import re_path, include

app_name = "users"
urlpatterns = [
    re_path(r'^v1/', include('users.api.v1.urls', namespace='v1')),
]