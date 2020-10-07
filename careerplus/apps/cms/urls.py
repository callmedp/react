# from django.conf.urls import url, include
from django.urls import re_path,include

from .views import CMSPageView, CMSStaticView

app_name = 'cms'
urlpatterns = [
    # re_path(r'^download-pdf/(?P<pk>\d+)/$',
    #     DownloadPdfView.as_view(), name='download-pdf'),

    # re_path(r'^(?P<static_kwarg>[-\w]+)/$',
    #     CMSStaticView.as_view(), name='static-page'),

    re_path(r'^(?P<slug>[-\w]+)/(?P<pk>\d+)/$',
        CMSPageView.as_view(), name='page'),


    re_path(r'^(?P<parent_slug>[-\w]+)/(?P<child_slug>[-\w]+)/(?P<pk>\d+)/$',
        CMSPageView.as_view(), name='page'),

    # re_path(r'^lead-management/$', LeadManagementView.as_view(),
    #     name='lead-management'),

    re_path(r'^api/', include('cms.api.urls', namespace='api')),

]
