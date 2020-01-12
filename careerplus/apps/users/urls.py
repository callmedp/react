from django.conf.urls import url,include
from users.views import (
    DownloadBoosterResume, ForgotPasswordResetView,
    ForgotHtmlView, ForgotPasswordEmailView,
    SocialLoginView, LinkedinLoginView,
    GenerateWriterInvoiceView, DownloadWriterInvoiceView,DownloadMonthlyWriterInvoiceView)

app_name = 'users'
urlpatterns = [
    url(r'^resume/download/$',
        DownloadBoosterResume.as_view(), name='download_booster_resume'),
    url(r'^update/password/$',
        ForgotPasswordResetView.as_view(), name='update-password'),
    url(r'^forgot/html/$',
        ForgotHtmlView.as_view(), name='forgot-html'),
    url(r'^submit/forgot-email/$',
        ForgotPasswordEmailView.as_view(), name='forgot-email-sent'),
    url(r'^social/login/$',
        SocialLoginView.as_view(), name='social-login'),
    url(r'^linkedin/code/$',
        LinkedinLoginView.as_view(), name='linkedin-code'),

    url(r'^generate-writer-invoice/$',
        GenerateWriterInvoiceView.as_view(),
        name='generate-writer-invoice'),

    url(r'^download-writer-invoice/$',
        DownloadWriterInvoiceView.as_view(),
        name='download-writer-invoice'),

    url(r'^download-monthly-writer-invoice/$',
        DownloadMonthlyWriterInvoiceView.as_view(),
        name='download-monthly-writer-invoice'),
    url(r'^api/', include('users.api.urls', namespace='api')),

]