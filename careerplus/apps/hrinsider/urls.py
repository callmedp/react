from django.conf.urls import url
from django.urls import reverse,reverse_lazy
from django.views.generic import RedirectView

from .views import HRLandingView, HRBlogDetailView, HrConclaveLandingView,\
    HrJobFairLandingView, HrConclaveDetailView, HrJobFairDetailView, \
    HRBlogTagView, HRTagLoadArticleView, HRArticleLoadMoreView
app_name = 'hrinsider'
urlpatterns = [
    url(r'^$', HRLandingView.as_view(), name='hr-landing'),
    url(r'^blog/$', HRLandingView.as_view(), {'list': True},
        name='hr-listing'),

    url(r'^tags/$', RedirectView.as_view(
        url=reverse_lazy('hrinsider:hr-landing'), permanent=True)),

    url(r'^tags/loadmore-article/$', HRTagLoadArticleView.as_view(),
        name='hr-tag-article-load'),

    url(r'^article/loadmore-article/$', HRArticleLoadMoreView.as_view(),
        name='hr-article-load-more'),

    url(r'^tags/(?P<slug>[-\w]+)/$', HRBlogTagView.as_view(),
        name='hr-tag-article'),

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