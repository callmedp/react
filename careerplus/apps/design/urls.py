# from django.conf.urls import url

from django.urls import re_path
from .views import DesignPage, FrontDesignPage


app_name = 'design'

urlpatterns = [
    re_path(r'^console/(?P<html>[a-z\-\.1-90\_]+)$', DesignPage.as_view(), name='test'),
    re_path(r'^site/(?P<html>[a-z\-\.1-90\_]+)$', FrontDesignPage.as_view(), name='test'),
]
