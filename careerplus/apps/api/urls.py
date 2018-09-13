from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^v1/create-order/$',
        views.CreateOrderApiView.as_view(), name='api-createorder'),
    url(r'^v1/get-ltvalue/$',
        views.EmailLTValueApiView.as_view(), name='api-ltvalue'),
    url(r'^v1/history/$',
        views.OrderHistoryAPIView.as_view(), name='historylist'),

    url(r'^v1/coupon-validate/$',
        views.ValidateCouponApiView.as_view(), name='coupon-validate'),
    url(r'^v1/remove-coupon/$',
        views.RemoveCouponApiView.as_view(), name='remove-coupon'),

    url(r'^v1/recommended-products/$',
        views.RecommendedProductsApiView.as_view(),
        name='api-recommended-products'),

    url(r'^v1/recommended-products-by-category/$',
        views.RecommendedProductsCategoryView.as_view(),
        name='api-recommended-products-category'),
]