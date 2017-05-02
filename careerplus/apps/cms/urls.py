from django.conf.urls import url, include

from .views import CMSPageView, LoginToCommentView, LeadManagementView,\
   DownloadPdfView

urlpatterns = [
    url(r'^page/(?P<slug>[-\w]+)/$', CMSPageView.as_view(), name='page'),

    url(r'^login/(?P<slug>[-\w]+)/$', LoginToCommentView.as_view(),
    	name='login-to-comment'),
    
    url(r'^lead-management/$', LeadManagementView.as_view(),
    	name='lead-management'),

    url(r'^download-pdf/(?P<slug>[-\w]+)/$', DownloadPdfView.as_view(),
    	name='download-pdf'),

    url(r'^api/', include('cms.api.urls', namespace='api')),
]