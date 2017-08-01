from django.conf.urls import url
from .views import RoundoneDashboardView, DashboardSavedDeleteView, \
DashboardUpcomingView, DashboardPastView, DashboardSavedView, \
DashboardResultView, DashboardMyProfileView, \
UpdateShineProfileView

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

    url(r'^roundone/profile/$', DashboardMyProfileView.as_view(),
        name='dashboard_profile'),
    
    url(r'^shine-profile/$',
        UpdateShineProfileView.as_view(), name='post_shine_detail'),
]
