from django.conf.urls import url

from .views import (
    ProductListView, ProductDeleteView, ProductDetailView, CreatePracticeTestInfoAPIView,
    UpdatePracticeInfoApiView, BoardNeoProductApiView, ParseSkillFromTextApiView,
    UpdateProductSkillView, UpdateScreenProductSkillView
)
from django.conf import settings
from rest_framework import routers

router = routers.DefaultRouter()
app_name='shop'
urlpatterns = [
    url(r'^products/$', ProductListView.as_view()),
    url(r'^get-products/$', ProductDetailView.as_view(),name='get-product' ),
    url(r'^create_practice_test_info/$', CreatePracticeTestInfoAPIView.as_view()),
    url(r'^update_practice_info/$', UpdatePracticeInfoApiView.as_view()),
    url(r'^neo_board_user/$', BoardNeoProductApiView.as_view()),
    url(r'^parse-skill/$', ParseSkillFromTextApiView.as_view()),
    url(r'^screen-product-skill/update/$', UpdateScreenProductSkillView.as_view()),
    url(r'^product-skill/update/$', UpdateProductSkillView.as_view())

]

if settings.DEBUG:
    urlpatterns = [
                      url(r'^products/delete/$', ProductDeleteView.as_view())
                  ] + urlpatterns
