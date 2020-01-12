from django.conf.urls import url
from django.conf import settings

from .views import LoadMoreApiView
app_name='skillpage'
urlpatterns = [
    url(r'^v1/load-more/$',
        LoadMoreApiView.as_view(),
        name='load-more'),
]