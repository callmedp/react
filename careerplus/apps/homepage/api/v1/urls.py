# from django.conf.urls import url
from django.urls import re_path

from . import views

app_name = "homepage"

urlpatterns = [
    re_path(r'^static-site-page/(?P<page_type>\d+)/$', views.StaticSiteView.as_view(), name='StaticSitePage'),
    re_path(r'^testimonial-category-map/$', views.TestimonialCategoryMapping.as_view(),
            name='testimonial-category-map'),
    re_path(r'^user-inbox/$', views.UserDashboardApi.as_view()),
    re_path(r'^order-item-comment/$', views.OrderItemCommentApi.as_view()),
    re_path(r'^dashboard-detail/$', views.DashboardDetailApi.as_view()),
    re_path(r'^dashboard-notification-box/$', views.DashboardNotificationBoxApi.as_view()),
    re_path(r'^dashboard-cancellation/$', views.DashboardCancellationApi.as_view()),
    re_path(r'^dashboard-resume-upload/$',views.DashboardResumeUploadApi.as_view()),
    re_path(r'^dashboard-resume-download/$', views.DashboardResumeDownloadApi.as_view()),
    re_path(r'^dashboard-linkedin-download/$', views.DashboardDraftDownloadApi.as_view()),
    re_path(r'^dashboard-profile-cred-download/$', views.ResumeProfileCredentialDownload.as_view()),

]