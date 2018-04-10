from django.conf.urls import url

from .views import HRLandingView, HRBlogDetailView, HrConclaveLandingView,\
    HrJobFairView

urlpatterns = [
    url(r'^$', HRLandingView.as_view(), name='hr-landing'),
    url(r'^articles/$', HRLandingView.as_view(), {'list': True},
        name='hr-listing'),
    url(r'^(?P<cat_slug>[-\w]+)/(?P<slug>[-\w]+)/$',
        HRBlogDetailView.as_view(), name='hr-articles-detail'),
    url(r'^hr-conclave/$', HrConclaveLandingView.as_view(),
        name='hr-conclave'),
    url(r'^jobfair/$', HrJobFairView.as_view(),
        name='jobfair'),
]


# mobile page url

urlpatterns += [
    
]