from django.conf.urls import url
from .views import PartnerHomeView, PartnerListView, PartnerDetailView, \
    GetReferenceView, SaveJobView, RedirectProfileView

urlpatterns = [

    url(r'^(?P<partner>[-\w]+)/?$', PartnerHomeView.as_view(),
        name='partner-home'),

    url(r'^(?P<partner>[-\w]+)/(?P<keyword>[-\w]+)-jobs-in-(?P<location>[-\w]+)/?$', 
    	PartnerListView.as_view(), name='partner-listing'),

    url(r'^(?P<partner>[-\w]+)/(?P<job_title>[-\w]+)/(?P<job_params>[-\w]+)/?$',
        PartnerDetailView.as_view(), name='partner-detail'),

    url(r'^roundone/get-reference/$', GetReferenceView.as_view(),
        name='roundone-get-reference'),

    url(regex=r'^roundone/redirect-profile/$',
        view=RedirectProfileView.as_view(),
        name='roundone-redirect-profile'),

    url(r'^roundone/save-job/$', SaveJobView.as_view(),
        name='roundone-save-job'),
]
