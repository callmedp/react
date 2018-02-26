from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^queue/$', views.WelcomeQueueView.as_view(),
        name='queue'),
    url(r'^assigned/$', views.WelcomeAssignedView.as_view(),
        name='assigned'),
    url(r'^callback/$', views.WelcomeCallbackView.as_view(),
        name='callback'),
    url(r'^service-issue/$',
        views.WelcomeServiceIssueView.as_view(),
        name='service-issue'),
    url(r'^done/$', views.WelcomeCallDoneView.as_view(),
        name='done'),
]
