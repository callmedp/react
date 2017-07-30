from django.conf.urls import url
from users.views import DownloadBoosterResume, ForgotPasswordResetView


urlpatterns = [
    url(r'^resume/download/$',
        DownloadBoosterResume.as_view(), name='download_booster_resume'),
    url(r'^forgot/password/$',
        ForgotPasswordResetView.as_view(), name='forgot-password'),
]