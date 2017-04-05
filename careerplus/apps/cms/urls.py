from django.conf.urls import url

from .views import CMSPageView, LoginToCommentView, LeadManagementView

urlpatterns = [
    url(r'^page/(?P<slug>[-\w]+)/$', CMSPageView.as_view(), name='page'),
    url(r'^login/(?P<slug>[-\w]+)/$', LoginToCommentView.as_view(),
    	name='login-to-comment'),
    url(r'^lead-management/$', LeadManagementView.as_view(),
    	name='lead-management'),
    
]