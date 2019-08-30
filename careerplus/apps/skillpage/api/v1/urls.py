from django.conf.urls import url
from django.conf import settings

from .views import CertificationLoadMoreApiView

urlpatterns = [
    url(r'^v1/Certification-load-more/$',
        CertificationLoadMoreApiView.as_view(),
        name='certification-load-more'),
]