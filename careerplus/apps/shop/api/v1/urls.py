from django.conf.urls import url

from .views import (
    ProductListView, ProductDeleteView, ProductDetailView, CreatePracticeTestInfoAPIView,
    UpdatePracticeInfoApiView, BoardNeoProductApiView
)
from django.conf import settings
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    url(r'^products/$', ProductListView.as_view()),
    url(r'^get-products/$', ProductDetailView.as_view(),name='get-product' ),
    url(r'^create_practice_test_info/$', CreatePracticeTestInfoAPIView.as_view()),
    url(r'^update_practice_info/$', UpdatePracticeInfoApiView.as_view()),
    url(r'^neo_board_user/$', BoardNeoProductApiView.as_view())

]

if settings.DEBUG:
    urlpatterns = [
                      url(r'^products/delete/$', ProductDeleteView.as_view())
                  ] + urlpatterns
