# from django.conf.urls import url
from django.urls import re_path

from . import views
from order.api.v1.views import OrderItemPatchView

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
    re_path(r'^dashboard-order-list/$', views.UserInboxListApiView.as_view()),
    re_path(r'^download-invoice/$', views.DashboardResumeInvoiceDownload.as_view()),
    re_path(r'^dashboard-feedback/$', views.DashboardFeedbackSubmit.as_view()),
    re_path(r'^dashboard-pause-play/$', OrderItemPatchView.as_view()),
    re_path(r'^dashboard-neo-board-user/$', views.NeoBoardUserAPI.as_view()),
    re_path(r'^trending-courses-and-skills/$', views.TrendingCoursesAndSkillsAPI.as_view(),
            name='trending-courses-and-skills-api'),
    re_path(r'^nav-offers-and-tags/$', views.NavigationTagsAndOffersAPI.as_view()),
    re_path(r'^popular-services/$', views.PopularServicesAPI.as_view(), name='popular-services-api'),
    re_path(r'^recent-course-added/$', views.RecentCoursesAPI.as_view(), name='recent-course-added-api'),
    re_path(r'^trending-categories/$', views.TrendingCategoriesApi.as_view(), name='trending-categories-api'),
    re_path(r'^latest-blogs/$', views.LatestBlogAPI.as_view(), name='latest-blog-api'),
    re_path(r'^most-viewed-courses/$', views.MostViewedCourseAPI.as_view(), name='most-viewed-course-api'),
    re_path(r'^in-demand-product/$', views.PopularInDemandProductsAPI.as_view(), name='most-viewed-course-api'),

]