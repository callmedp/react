# from django.conf.urls import url
from django.urls import re_path
from django.urls import re_path, include

from .views import (
    RoundoneDashboardView,
    DashboardSavedDeleteView,
    DashboardUpcomingView,
    DashboardPastView,
    DashboardSavedView,
    DashboardResultView,
    DashboardMyProfileView,
    UpdateShineProfileView,
)
from . import dashboard_view, mobile_view

from django.views.decorators.csrf import csrf_exempt


app_name='dashboard'
urlpatterns = [
    re_path(r'^roundone/$', RoundoneDashboardView.as_view(),
        name='roundone-dashboard'),

    re_path(r'^roundone/saved/delete/$', DashboardSavedDeleteView.as_view(),
        name='dashboard_saved_delete'),

    re_path(r'^roundone/upcoming/$', DashboardUpcomingView.as_view(),
        name='dashboard_upcoming'),

    re_path(r'^roundone/past/$', DashboardPastView.as_view(),
        name='dashboard_past'),

    re_path(r'^roundone/saved/$', DashboardSavedView.as_view(),
        name='dashboard_saved'),

    # re_path(r'^roundone/result/$', DashboardResultView.as_view(),
    #     name='dashboard_roundone_result'),

    re_path(r'^roundone/profile/$', DashboardMyProfileView.as_view(),
        name='dashboard_profile'),

    re_path(r'^shine-profile/$',
        UpdateShineProfileView.as_view(), name='post_shine_detail'),

    re_path(r'^roundone/result/(?P<order_id>.+)/?$',
        DashboardResultView.as_view(), name='dashboard_roundone_result'),
]

urlpatterns += [
    re_path(r'^$',
        dashboard_view.DashboardView.as_view(), name='dashboard'),

    re_path(r'^v1/', include('dashboard.api.v1.urls', namespace='dashboard-api')),

    re_path(r'^myorder/$',
        dashboard_view.DashboardMyorderView.as_view(),
        name='dashboard-myorder'),

    re_path(r'^mywallet/$',
        dashboard_view.DashboardMyWalletView.as_view(),
        name='dashboard-mywallet'),

    # ajax call
    re_path(r'^inbox-detail/$',
        dashboard_view.DashboardDetailView.as_view(),
        name='dashboard-detail'),

    re_path(r'^inbox-comment/$',
        dashboard_view.DashboardCommentView.as_view(),
        name='dashboard-comment'),

    re_path(r'^inbox-feedback/$',
        dashboard_view.DashboardFeedbackView.as_view(),
        name='dashboard-feedback'),

    re_path(r'^inbox-rejectservice/$',
        dashboard_view.DashboardRejectService.as_view(),
        name='dashboard-rejectservice'),

    re_path(r'^inbox-acceptservice/$',
        dashboard_view.DashboardAcceptService.as_view(),
        name='dashboard-acceptservice'),

    re_path(r'^loadmore/orderitem/$',
        dashboard_view.DashboardInboxLoadmoreView.as_view(),
        name='dashboard-inbox-loadmore'),

    re_path(r'^inbox-filter/$',
        dashboard_view.DashboardInboxFilterView.as_view(),
        name='dashboard-inboxfilter'),

    re_path(r'^inbox-notificationbox/$',
        dashboard_view.DashboardNotificationBoxView.as_view(),
        name='dashboard-notificationbox'),

    re_path(r'^order-invoicedownload/$',
        dashboard_view.DashboardInvoiceDownload.as_view(),
        name='dashboard-invoicedownload'),
    re_path(r'^order-resumetemplatedownload/$',
        csrf_exempt(dashboard_view.DashboardResumeTemplateDownload.as_view()),
        name='dashboard-resumetemplatedownload'),

    re_path(r'^order-resumedownload/(?P<pk>[\d]+)/$',
        dashboard_view.DashboardResumeDownload.as_view(),
        name='dashboard-resumedownload'),

    re_path(r'^downloadquestionnaire/$',
        dashboard_view.DownloadQuestionnaireView.as_view(),
        name='dashboard-downloadquestionnaire'),

    re_path(r'cancel-order/$',
        dashboard_view.DashboardCancelOrderView.as_view(),
        name='cancel-order')
]


# for mobile pages

urlpatterns += [
    re_path(r'^item-detail/$',
        mobile_view.DashboardItemDetailView.as_view(),
        name='dashboard-itemdetail'),
    re_path(r'^itemfeedback/$',
        mobile_view.DashboardItemFeedbackView.as_view(),
        name='dashboard-itemfeedback'),

    re_path(r'^conversation/$',
        mobile_view.DashboardMobileCommentView.as_view(),
        name='dashboard-conversation'),

    re_path(r'^rejectconfirmation/$',
        mobile_view.DashboardMobileRejectView.as_view(),
        name='dashboard-reject'),
]
