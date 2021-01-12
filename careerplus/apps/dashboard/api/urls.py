# from django.conf.urls import url, include
from django.urls import re_path, include
app_name='dashboard'
urlpatterns = [
    re_path(r'^v1/', include('dashboard.api.v1.urls', namespace='dashboard-api')),
]