from django.conf.urls import url
from . import views
app_name = 'console'
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

    url(r'^update/(?P<pk>\d+)/$',
        views.WelcomeCallUpdateView.as_view(),
        name='update'),

    url(r'^history/(?P<pk>\d+)/$',
        views.WelcomeCallHistoryView.as_view(),
        name='history'),
]
