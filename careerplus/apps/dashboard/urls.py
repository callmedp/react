from django.conf.urls import url

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


urlpatterns = [
    url(r'^roundone/$', RoundoneDashboardView.as_view(),
        name='roundone-dashboard'),

    url(r'^roundone/saved/delete/$', DashboardSavedDeleteView.as_view(),
        name='dashboard_saved_delete'),

    url(r'^roundone/upcoming/$', DashboardUpcomingView.as_view(),
        name='dashboard_upcoming'),

    url(r'^roundone/past/$', DashboardPastView.as_view(),
        name='dashboard_past'),

    url(r'^roundone/saved/$', DashboardSavedView.as_view(),
        name='dashboard_saved'),

    # url(r'^roundone/result/$', DashboardResultView.as_view(),
    #     name='dashboard_roundone_result'),

    url(r'^roundone/profile/$', DashboardMyProfileView.as_view(),
        name='dashboard_profile'),

    url(r'^shine-profile/$',
        UpdateShineProfileView.as_view(), name='post_shine_detail'),

    url(r'^roundone/result/(?P<order_id>.+)/?$',
        DashboardResultView.as_view(), name='dashboard_roundone_result'),
]

urlpatterns += [
    url(r'^$',
        dashboard_view.DashboardView.as_view(), name='dashboard'),

    url(r'^myorder/$',
        dashboard_view.DashboardMyorderView.as_view(),
        name='dashboard-myorder'),

    url(r'^mywallet/$',
        dashboard_view.DashboardMyWalletView.as_view(),
        name='dashboard-mywallet'),

    # ajax call
    url(r'^inbox-detail/$',
        dashboard_view.DashboardDetailView.as_view(),
        name='dashboard-detail'),

    url(r'^inbox-comment/$',
        dashboard_view.DashboardCommentView.as_view(),
        name='dashboard-comment'),

    url(r'^inbox-feedback/$',
        dashboard_view.DashboardFeedbackView.as_view(),
        name='dashboard-feedback'),

    url(r'^inbox-rejectservice/$',
        dashboard_view.DashboardRejectService.as_view(),
        name='dashboard-rejectservice'),

    url(r'^inbox-acceptservice/$',
        dashboard_view.DashboardAcceptService.as_view(),
        name='dashboard-acceptservice'),

    url(r'^loadmore/orderitem/$',
        dashboard_view.DashboardInboxLoadmoreView.as_view(),
        name='dashboard-inbox-loadmore'),

    url(r'^inbox-filter/$',
        dashboard_view.DashboardInboxFilterView.as_view(),
        name='dashboard-inboxfilter'),

    url(r'^inbox-notificationbox/$',
        dashboard_view.DashboardNotificationBoxView.as_view(),
        name='dashboard-notificationbox'),

    url(r'^order-invoicedownload/$',
        dashboard_view.DashboardInvoiceDownload.as_view(),
        name='dashboard-invoicedownload'),
    url(r'^order-resumetemplatedownload/$',
        dashboard_view.DashboardResumeTemplateDownload.as_view(),
        name='dashboard-resumetemplatedownload'),

    url(r'^order-resumedownload/(?P<pk>[\d]+)/$',
        dashboard_view.DashboardResumeDownload.as_view(),
        name='dashboard-resumedownload'),

    url(r'^downloadquestionnaire/$',
        dashboard_view.DownloadQuestionnaireView.as_view(),
        name='dashboard-downloadquestionnaire'),

    url(r'cancel-order/$',
        dashboard_view.DashboardCancelOrderView.as_view(),
        name='cancel-order')
]


# for mobile pages

urlpatterns += [
    url(r'^item-detail/$',
        mobile_view.DashboardItemDetailView.as_view(),
        name='dashboard-itemdetail'),
    url(r'^itemfeedback/$',
        mobile_view.DashboardItemFeedbackView.as_view(),
        name='dashboard-itemfeedback'),

    url(r'^conversation/$',
        mobile_view.DashboardMobileCommentView.as_view(),
        name='dashboard-conversation'),

    url(r'^rejectconfirmation/$',
        mobile_view.DashboardMobileRejectView.as_view(),
        name='dashboard-reject'),
]
