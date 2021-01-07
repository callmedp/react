from django.urls import re_path
from . import views

app_name = "dashboard"

urlpatterns = [
    re_path(r'^my-orders/$', views.DashboardMyorderApi.as_view(), name='my-orders'),
]
