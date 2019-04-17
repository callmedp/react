from django.conf.urls import url
from .views import ProductListView, ProductDeleteView
from django.conf import settings
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    url(r'^products/$', ProductListView.as_view()),
]

if settings.DEBUG:
    urlpatterns = [
                      url(r'^products/delete/$', ProductDeleteView.as_view())
                  ] + urlpatterns
