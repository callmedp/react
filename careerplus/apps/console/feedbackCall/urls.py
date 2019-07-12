from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^queue/$', views.FeedbackQueueView.as_view(),
        name='queue'),
]
