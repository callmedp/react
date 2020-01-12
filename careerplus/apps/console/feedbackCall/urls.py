#django imports
from django.conf.urls import url

#same folder imports
from . import views
app_name = 'console'
urlpatterns = [
    url(r'^queue/$', views.FeedbackQueueView.as_view(),
        name='queue'),
    url(r'^report/$', views.FeedbackReportView.as_view(),
        name='report'),
    url(r'^update/(?P<pk>\d+)/$',
        views.CustomerFeedbackUpdate.as_view(),
        name='update'),
    
]
