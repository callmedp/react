from django.conf.urls import url, include
from . import views
app_name ='console'
urlpatterns = [
    url(r'^partial/', include('console.partner.partials.urls', namespace='partials')),
    url(r'^', include('console.partner.pages.urls', namespace='pages')),

    # partner inbox Queue
    url(r'^inbox/$', views.PartnerInboxQueueView.as_view(),
        name='partnerinbox'),
    url(r'^hold/$', views.PartnerHoldQueueView.as_view(),
        name='partnerholdqueue'),
    url(r'^varification-reports/$', views.PartnerVarificationQueueView.as_view(),
        name='varificationreports'),
]
