from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^queue/$', views.FeedbackQueueView.as_view(),
        name='queue'),
    url(r'^update/(?P<pk>\d+)/$',
        views.CustomerFeedbackUpdate.as_view(),
        name='update'),
    
]
