#django imports
# from django.conf.urls import url
from django.urls import re_path

#same folder imports
from . import views
app_name = 'console'
urlpatterns = [
    re_path(r'^queue/$', views.FeedbackQueueView.as_view(),
        name='queue'),
    re_path(r'^report/$', views.FeedbackReportView.as_view(),
        name='report'),
    re_path(r'^update/(?P<pk>\d+)/$',
        views.CustomerFeedbackUpdate.as_view(),
        name='update'),
    
]
