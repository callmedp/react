from django.conf.urls import url
from django.conf import settings

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
    url(r'^v1/remove-cookie-from-header/$',
        views.RemoveCookieFromHeader.as_view(),
        name='remove-cookie-from-header'),
    url(r'^v1/update-certificate-assesment/(?P<vendor_name>[\w\-]+)/$',
        views.UpdateCertificateAndAssesment.as_view(),
        name='update-certificate-assesment'),
    url(r'^v1/shine-data-for-flow/$',
        views.ShineDataFlowDataApiView.as_view(),
        name='shine-data-for-flow'),
    url(r'^v1/vendor-certificate/$',
        views.VendorCertificateMappingApiView.as_view(),
        name='vendor-certificate-mapping'),
    url(r'^v1/import-certificates/(?P<vendor_name>[\w\-]+)/$',
        views.ImportCertificateApiView.as_view(),
        name='import-certificate'),
    url(r'^v1/talent-economy-blogs/$',
        views.TalentEconomyApiView.as_view(),
        name='talent-economy-blogs'),
    url(r'^v1/media-upload/$',
        views.MediaUploadView.as_view(),
        name='v1.media-upload'),
    url(r'^v1/resume-product-id/$',
        views.ResumeBuilderProductView.as_view(),
        name='v1.resume-product-id'),
    url(r'^v1/candidate-login/$', views.ShineCandidateLoginAPIView.as_view(), name='v1.api-login'),
    url(r'^v1/update-certificate-assesment/(?P<vendor_name>[\w\-]+)/$',
        views.UpdateCertificateAndAssesment.as_view(),
        name='remove-cookie-from-header')
    url(r'^v1/candidate-insights/$',
        views.CandidateInsight.as_view(),
        name='candidate-insights')
]

if settings.DEBUG:
    urlpatterns += [
        url(r'v1/cron/(?P<cron_id>\d+)/$', views.CronInitiateApiView.as_view(),
            name='api-cron-inititate')
    ]
