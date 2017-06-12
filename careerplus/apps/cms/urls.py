from django.conf.urls import url

from .views import CMSPageView, LeadManagementView,\
   DownloadPdfView

urlpatterns = [
    url(r'^page/(?P<slug>[-\w]+)/(?P<pk>\d+)/$', CMSPageView.as_view(), name='page'),
    
    url(r'^lead-management/$', LeadManagementView.as_view(),
    	name='lead-management'),

    url(r'^download-pdf/(?P<pk>\d+)/$', DownloadPdfView.as_view(),
    	name='download-pdf'),
    
]