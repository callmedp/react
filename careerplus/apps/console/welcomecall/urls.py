# from django.conf.urls import url
from django.urls import re_path
from . import views
app_name = 'console'
urlpatterns = [
    re_path(r'^queue/$', views.WelcomeQueueView.as_view(),
        name='queue'),
    re_path(r'^assigned/$', views.WelcomeAssignedView.as_view(),
        name='assigned'),
    re_path(r'^callback/$', views.WelcomeCallbackView.as_view(),
        name='callback'),
    re_path(r'^service-issue/$',
        views.WelcomeServiceIssueView.as_view(),
        name='service-issue'),
    re_path(r'^done/$', views.WelcomeCallDoneView.as_view(),
        name='done'),

    re_path(r'^update/(?P<pk>\d+)/$',
        views.WelcomeCallUpdateView.as_view(),
        name='update'),

    re_path(r'^history/(?P<pk>\d+)/$',
        views.WelcomeCallHistoryView.as_view(),
        name='history'),
]
