from django.conf.urls import url

from .views import CMSPageView


urlpatterns = [
    url(r'^page/(?P<slug>[-\w]+)/$', CMSPageView.as_view(), name='page'),
]