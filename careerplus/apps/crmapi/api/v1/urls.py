# from django.conf.urls import url, include
from django.urls import re_path, include

#internal imports
from .views import LeadManagementAPI

#third party imports
from rest_framework import routers

router = routers.DefaultRouter()
app_name = 'crmapi'
urlpatterns = [
    re_path(r'^lead-management/$', LeadManagementAPI.as_view())
]