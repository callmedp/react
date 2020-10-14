# from django.conf.urls import url
from django.urls import re_path


from .views import PartnerHomeView, PartnerListView, PartnerDetailView, \
    GetReferenceView, SaveJobView, RedirectProfileView

urlpatterns = [

    re_path(r'^(?P<partner>[-\w]+)/?$', PartnerHomeView.as_view(),
        name='partner-home'),

    re_path(r'^(?P<partner>[-\w]+)/(?P<keyword>[-\w]+)-jobs-in-(?P<location>[-\w]+)/?$', 
    	PartnerListView.as_view(), name='partner-listing'),

    re_path(r'^(?P<partner>[-\w]+)/(?P<job_title>[-\w]+)/(?P<job_params>[-\w]+)/?$',
        PartnerDetailView.as_view(), name='partner-detail'),

    re_path(r'^roundone/get-reference/$', GetReferenceView.as_view(),
        name='roundone-get-reference'),

    re_path(r'^roundone/redirect-profile/$',
        RedirectProfileView.as_view(),
        name='roundone-redirect-profile'),

    re_path(r'^roundone/save-job/$', SaveJobView.as_view(),
        name='roundone-save-job'),
]
