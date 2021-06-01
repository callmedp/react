# from django.conf.urls import url
from django.urls import re_path

from .views import (
    ProductListView, ProductDeleteView, ProductDetailView, CreatePracticeTestInfoAPIView,
    UpdatePracticeInfoApiView, BoardNeoProductApiView, ParseSkillFromTextApiView,
    UpdateProductSkillView, UpdateScreenProductSkillView, RecommendedProductsAPIView,
    ProductReview,SkillProductView, CourseCatalogueAPI
)

from .api import (
    ProductDetailAPI,
    ProductReviewAPIListing,
    ProductReviewAPI

)

from django.conf import settings
from rest_framework import routers

router = routers.DefaultRouter()
app_name = 'shop'
urlpatterns = [
    re_path(r'^products/$', ProductListView.as_view()),
    re_path(r'^get-products/$', ProductDetailView.as_view(),name='get-product' ),
    re_path(r'^create_practice_test_info/$', CreatePracticeTestInfoAPIView.as_view()),
    re_path(r'^update_practice_info/$', UpdatePracticeInfoApiView.as_view()),
    re_path(r'^neo_board_user/$', BoardNeoProductApiView.as_view()),
    re_path(r'^parse-skill/$', ParseSkillFromTextApiView.as_view()),
    re_path(r'^screen-product-skill/update/$', UpdateScreenProductSkillView.as_view()),
    re_path(r'^product-skill/update/$', UpdateProductSkillView.as_view()),
    re_path(r'^recommend-products/$', RecommendedProductsAPIView.as_view()),
    re_path(r'^product-review',ProductReview.as_view()),
    re_path(r'^skill-product/$',SkillProductView.as_view()),
    re_path(r'^course-catalogue/$', CourseCatalogueAPI.as_view(), name='course-catalogue-api'),

    re_path(r'^get-product/$', ProductDetailAPI.as_view(), name='get-product-api'),
    re_path(r'^get-prd-review/$', ProductReviewAPIListing.as_view(), name='get-product-review-api'),
    re_path(r'^product/review/$', ProductReviewAPI.as_view(), name='product-review-add-update-api')
]

if settings.DEBUG:
    urlpatterns = [
                      re_path(r'^products/delete/$', ProductDeleteView.as_view())
                  ] + urlpatterns
