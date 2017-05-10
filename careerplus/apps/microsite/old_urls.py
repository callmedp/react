from django.conf.urls import url

from .views import PartnerHomeView, PartnerListView, PartnerDetailView
    #GetReferenceView, RoundoneRegisterView, SaveJobView, RedirectProfileView,\
    #RoundoneAboutUsView, RoundoneReferralView

urlpatterns = [
    url(regex=r'^(?P<partner>[-\w]+)/?$', view=PartnerHomeView.as_view(),
        name='partner-home'),

    url(regex=r'^(?P<partner>[-\w]+)/(?P<keyword>[-\w]+)-jobs-in-(?P<location>[-\w]+)/?$', view=PartnerListView.as_view(), name='partner-listing'),

    url(regex=r'^(?P<partner>[-\w]+)/(?P<job_title>[-\w]+)/(?P<job_params>[-\w]+)/?$', view=PartnerDetailView.as_view(), name='partner-detail'),

    # # roundone specific urls
    # url(regex=r'^roundone/get-reference/$',
    #     view=GetReferenceView.as_view(),
    #     name='roundone-get-reference'),

    # url(regex=r'^roundone/redirect-profile/$',
    #     view=RedirectProfileView.as_view(),
    #     name='roundone-redirect-profile'),

    # url(regex=r'^roundone/save-job/$',
    #     view=SaveJobView.as_view(),
    #     name='roundone-save-job'),

    # url(regex=r'^roundone/register/$',
    #     view=RoundoneRegisterView.as_view(),
    #     name='roundone-register'),

    # url(regex=r'^roundone/aboutus/$',
    #     view=RoundoneAboutUsView.as_view(),
    #     name='roundone-aboutus'),

    # url(regex=r'^roundone/job-referral/$',
    #     view=RoundoneReferralView.as_view(),
    #     name='roundone-job-referral'),

    # url(regex=r'^(?P<partner_name>[-\w]+)/listing/$', view=PartnerHomeView.as_view(), name='partner-home'),
    # url(regex=r'^(?P<partner_name>[-\w]+)/detail/$', view=PartnerHomeView.as_view(), name='partner-home'),
]
