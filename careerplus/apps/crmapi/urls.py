from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^lead-management/$',
        views.LeadManagement.as_view(), name='lead-management'),
]