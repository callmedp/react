# from django.conf.urls import url, include
from django.urls import re_path, include
from . import views
app_name = 'console'
urlpatterns = [
    re_path(r'^partial/', include('console.partner.partials.urls', namespace='partials')),
    re_path(r'^', include('console.partner.pages.urls', namespace='pages')),

    # partner inbox Queue
    re_path(r'^inbox/$', views.PartnerInboxQueueView.as_view(),
        name='partnerinbox'),
    re_path(r'^hold/$', views.PartnerHoldQueueView.as_view(),
        name='partnerholdqueue'),
    re_path(r'^varification-reports/$', views.PartnerVarificationQueueView.as_view(),
        name='varificationreports'),
]
