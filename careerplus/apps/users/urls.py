from django.conf.urls import url
from users.views import DownloadBoosterResume, DashboardDetailView,\
    DashboardCommentView, DashboardRejectService


urlpatterns = [
    url(r'^resume/download/$',
        DownloadBoosterResume.as_view(), name='download_booster_resume'),

    # ajax call
    url(r'^dashboard/detail/$',
        DashboardDetailView.as_view(), name='dashboard-detail'),
    url(r'^dashboard/comment/$',
        DashboardCommentView.as_view(), name='dashboard-comment'),
    url(r'^dashboard/rejectservice/$',
        DashboardRejectService.as_view(), name='dashboard-rejectservice'),

]