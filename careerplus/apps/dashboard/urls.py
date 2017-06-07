from django.conf.urls import url
from .views import RoundoneDashboardView, DashboardSavedDeleteView, \
DashboardUpcomingView, DashboardPastView, DashboardSavedView, DashboardResultView

urlpatterns = [
    url(r'^roundone/$', RoundoneDashboardView.as_view(),
        name='roundone-dashboard'),

    url(r'^roundone/saved/delete/$', DashboardSavedDeleteView.as_view(),
        name='dashboard_saved_delete'),

    url(r'^roundone/upcoming/$',DashboardUpcomingView.as_view(),
        name='dashboard_upcoming'),

    url(r'^roundone/past/$', DashboardPastView.as_view(),
        name='dashboard_past'),

    url(r'^roundone/saved/$', DashboardSavedView.as_view(),
        name='dashboard_saved'),

    url(r'^roundone/result/$', DashboardResultView.as_view(),
        name='dashboard_roundone_result'),
]
