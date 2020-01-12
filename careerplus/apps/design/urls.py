from django.conf.urls import url
from .views import DesignPage, FrontDesignPage
app_name='design'
urlpatterns = [
    url(r'^console/(?P<html>[a-z\-\.1-90\_]+)$', DesignPage.as_view(), name='test'),
    url(r'^site/(?P<html>[a-z\-\.1-90\_]+)$', FrontDesignPage.as_view(), name='test'),
]
