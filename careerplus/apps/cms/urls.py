from django.conf.urls import url, include

from .views import CMSPageView, CMSStaticView


urlpatterns = [
    # url(r'^download-pdf/(?P<pk>\d+)/$',
    #     DownloadPdfView.as_view(), name='download-pdf'),

    # url(r'^(?P<static_kwarg>[-\w]+)/$',
    #     CMSStaticView.as_view(), name='static-page'),

    url(r'^(?P<slug>[-\w]+)/(?P<pk>\d+)/$',
        CMSPageView.as_view(), name='page'),


    url(r'^(?P<parent_slug>[-\w]+)/(?P<child_slug>[-\w]+)/(?P<pk>\d+)/$',
        CMSPageView.as_view(), name='page'),

    # url(r'^lead-management/$', LeadManagementView.as_view(),
    #     name='lead-management'),

    url(r'^api/', include(('cms.api.urls','cms'), namespace='api')),

]
