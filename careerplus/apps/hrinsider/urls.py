from django.conf.urls import url

from .views import HRLandingView, HRBlogDetailView, HrConclaveLandingView,\
    HrJobFairLandingView, HrConclaveDetailView, HrJobFairDetailView

urlpatterns = [
    url(r'^$', HRLandingView.as_view(), name='hr-landing'),
    url(r'^blog/$', HRLandingView.as_view(), {'list': True},
        name='hr-listing'),
    url(r'^blog/(?P<slug>[-\w]+)/$',
        HRBlogDetailView.as_view(), name='hr-articles-detail'),

    url(r'^hr-conclave/$', HrConclaveLandingView.as_view(),
        name='hr-conclave'),
    url(r'^hr-conclave/(?P<slug>[-\w]+)/$', HrConclaveDetailView.as_view(),
        name='conclave-detail'),

    url(r'^jobfair/$', HrJobFairLandingView.as_view(),
        name='jobfair'),
    url(r'^jobfair/(?P<slug>[-\w]+)/$', HrJobFairDetailView.as_view(),
        name='jobfair-detail'),
]


# mobile page url

urlpatterns += [
    
]