from django.conf.urls import url
from .views import DesignPage

urlpatterns = [
    url(r'^(?P<html>[a-z\-\.1-90\_]+)$', DesignPage.as_view(), name='test'),
]
