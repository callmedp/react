# from django.conf.urls import url
from django.urls import re_path ,include
from django.conf import settings

from . import views
app_name='api'
urlpatterns = [
    re_path(r'^v1/create-order/$',
        views.CreateOrderApiView.as_view(), name='api-createorder'),
    re_path(r'^v1/get-ltvalue/$',
        views.EmailLTValueApiView.as_view(), name='api-ltvalue'),
    re_path(r'^v1/history/$',
        views.OrderHistoryAPIView.as_view(), name='historylist'),

    re_path(r'^v1/coupon-validate/$',
        views.ValidateCouponApiView.as_view(), name='coupon-validate'),
    re_path(r'^v1/remove-coupon/$',
        views.RemoveCouponApiView.as_view(), name='remove-coupon'),

    re_path(r'^v1/recommended-products-by-email/$',
        views.RecommendedProductsApiView.as_view(),
        name='api-recommended-products'),

    re_path(r'^v1/recommended-products-by-category/$',
        views.RecommendedProductsCategoryView.as_view(),
        name='api-recommended-products-category'),
    re_path(r'^v1/remove-cookie-from-header/$',
        views.RemoveCookieFromHeader.as_view(),
        name='remove-cookie-from-header'),
    re_path(r'^v1/update-certificate-assesment/(?P<vendor_name>[\w\-]+)/$',
        views.UpdateCertificateAndAssesment.as_view(),
        name='update-certificate-assesment'),
    re_path(r'^v1/shine-data-for-flow/$',
        views.ShineDataFlowDataApiView.as_view(),
        name='shine-data-for-flow'),
    re_path(r'^v1/question/$',
        views.QuestionAnswerApiView.as_view(),
        name='question-answer'),
    re_path(r'^v1/vendor-certificate/$',
        views.VendorCertificateMappingApiView.as_view(),
        name='vendor-certificate-mapping'),
    re_path(r'^v1/import-certificates/(?P<vendor_name>[\w\-]+)/$',
        views.ImportCertificateApiView.as_view(),
        name='import-certificate'),
    re_path(r'^v1/talent-economy-blogs/$',
        views.TalentEconomyApiView.as_view(),
        name='talent-economy-blogs'),

    re_path(r'^v1/order-detail/(?P<pk>\d+)/$',
        views.OrderDetailApiView.as_view(),
        name='order-detail'),

    re_path(r'^v1/order-list/$',
        views.OrderListApiView.as_view(),
        name='order-detail'),

    re_path(r'^v1/media-upload/$',
        views.MediaUploadView.as_view(),
        name='v1.media-upload'),
    re_path(r'^v1/resume-product-id/$',
        views.ResumeBuilderProductView.as_view(),
        name='v1.resume-product-id'),
    re_path(r'^v1/candidate-login/(?P<candidate_id>[0-9a-z]+)$', views.ShineCandidateLoginAPIView.as_view(), name='v1.api-login'),
    re_path(r'^v1/update-certificate-assesment/(?P<vendor_name>[\w\-]+)/$',
        views.UpdateCertificateAndAssesment.as_view(),
        name='remove-cookie-from-header'),
    re_path(r'^v1/candidate-insights/$',
        views.CandidateInsight.as_view(),
        name='candidate-insights'),
    re_path(r'^v1/get-set-time/$',
        views.TestTimer.as_view(),
        name='get-test-time'),
    re_path(r'^v1/set-session/$',
        views.SetSession.as_view(),
        name='set-session'),
    re_path(r'^v1/remove-cache/$',
        views.RemoveCache.as_view(),
        name='set-session'),
    re_path(r'^v1/get-server-time/$',
        views.ServerTimeAPIView.as_view(),
        name='get-server-time'
        ),
    re_path(r'^v1/claim-order/$',
        views.ClaimOrderAPIView.as_view(),
        name='claim-order'
        ),

    re_path(r'^v1/blog-tags/$',
            views.BlogTagsAPIView.as_view(),
            ),


    re_path(r'^v1/auto-login-token/(?P<order_item_id>\d+)/$',views.GetAutoLoginToken.as_view()),
    re_path(r'^v1/cache/$', views.GetCacheValue.as_view(), name='get-cache-value'),
    re_path(r'^v1/get-recommended-products/$',
    views.GetRecommendedProductApi.as_view(),
    name='get-recommended-products'
    ),
    re_path(r'^v1/update-candidate-badging/$',
    views.CandidateBadging.as_view(),
    name='candidate-badging-details'
    ),
    re_path(r'^v1/tracking-resume-shine/$',
        views.TrackingResumeShine.as_view(),
        name='tracking-resume-shine'
    ),
    re_path(r'^v1/resumetemplatedownload/$',
        views.ResumeTemplateDownload.as_view(),
        name='resume-template-download'
    ),
    re_path(r'^v2/', include('api.v2.urls')),
    re_path(r'^v1/resume_mailer_tracking/$', 
        views.ResumePromotionTrackingAPIView.as_view(),
        name='resume-mailer-tracking'),
    re_path(r'v1/search-query/$', views.SearchQueryAPI.as_view(),
        name='search-query-api'
    ),
    re_path(r'v1/recommended-courses-and-assesments/$', views.RecommendedCoursesAPI.as_view(),
        name='recommended-products-api'
    ),
    re_path(r'v1/fetch-info/$', views.FetchInfoAPIView.as_view(),
            name='fetch-info'
            ),
]

if settings.DEBUG:
    urlpatterns += [
        re_path(r'v1/cron/(?P<cron_id>\d+)/$', views.CronInitiateApiView.as_view(),
            name='api-cron-inititate')
    ]
