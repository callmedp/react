from django.conf.urls import url
from .views import PartnerHomeView, PartnerListView

urlpatterns = [

    url(r'^(?P<partner>[-\w]+)/?$', PartnerHomeView.as_view(),
        name='partner-home'),

    url(r'^(?P<partner>[-\w]+)/(?P<keyword>[-\w]+)-jobs-in-(?P<location>[-\w]+)/?$', 
    	PartnerListView.as_view(), name='partner-listing'),
]
