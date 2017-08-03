from django.conf.urls import url
from users.views import (
	DownloadBoosterResume, 
	ForgotPasswordResetView,
	ForgotHtmlView,
	ForgotPasswordEmailView,)


urlpatterns = [
    url(r'^resume/download/$',
        DownloadBoosterResume.as_view(), name='download_booster_resume'),
    url(r'^update/password/$',
        ForgotPasswordResetView.as_view(), name='update-password'),
    url(r'^forgot/html/$',
        ForgotHtmlView.as_view(), name='forgot-html'),
    url(r'^submit/forgot-email/$',
        ForgotPasswordEmailView.as_view(), name='forgot-email-sent'),
]