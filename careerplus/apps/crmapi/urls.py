# from django.conf.urls import url

from django.urls import re_path, include
from . import views

app_name = 'crmapi'
urlpatterns = [
    re_path(r'^lead-management/$',
        views.LeadManagement.as_view(), name='lead-management'),
    re_path(r'^lead-save/$',
        views.LeadManagementWithCaptcha.as_view(), name='lead-management-captcha'),
    re_path(r'^api/v1/', include('crmapi.api.urls', namespace='api')),
]