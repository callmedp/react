from django.conf.urls import url

from . import views

app_name = 'crmapi'
urlpatterns = [
    url(r'^lead-management/$',
        views.LeadManagement.as_view(), name='lead-management'),
    url(r'^lead-save/$',
        views.LeadManagementWithCaptcha.as_view(), name='lead-management-captcha'),
]