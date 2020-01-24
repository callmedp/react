# from django.conf.urls import url,include

from django.urls import re_path,include
from users.views import (
    DownloadBoosterResume, ForgotPasswordResetView,
    ForgotHtmlView, ForgotPasswordEmailView,
    SocialLoginView, LinkedinLoginView,
    GenerateWriterInvoiceView, DownloadWriterInvoiceView,DownloadMonthlyWriterInvoiceView)

app_name = 'users'
urlpatterns = [
    re_path(r'^resume/download/$',
        DownloadBoosterResume.as_view(), name='download_booster_resume'),
    re_path(r'^update/password/$',
        ForgotPasswordResetView.as_view(), name='update-password'),
    re_path(r'^forgot/html/$',
        ForgotHtmlView.as_view(), name='forgot-html'),
    re_path(r'^submit/forgot-email/$',
        ForgotPasswordEmailView.as_view(), name='forgot-email-sent'),
    re_path(r'^social/login/$',
        SocialLoginView.as_view(), name='social-login'),
    re_path(r'^linkedin/code/$',
        LinkedinLoginView.as_view(), name='linkedin-code'),

    re_path(r'^generate-writer-invoice/$',
        GenerateWriterInvoiceView.as_view(),
        name='generate-writer-invoice'),

    re_path(r'^download-writer-invoice/$',
        DownloadWriterInvoiceView.as_view(),
        name='download-writer-invoice'),

    re_path(r'^download-monthly-writer-invoice/$',
        DownloadMonthlyWriterInvoiceView.as_view(),
        name='download-monthly-writer-invoice'),
    re_path(r'^api/', include('users.api.urls', namespace='api')),

]