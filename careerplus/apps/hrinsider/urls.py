# from django.conf.urls import url
from django.urls import reverse,reverse_lazy,re_path
from django.views.generic import RedirectView

from .views import HRLandingView, HRBlogDetailView, HrConclaveLandingView,\
    HrJobFairLandingView, HrConclaveDetailView, HrJobFairDetailView, \
    HRBlogTagView, HRTagLoadArticleView, HRArticleLoadMoreView
app_name = 'hrinsider'
urlpatterns = [
    re_path(r'^$', HRLandingView.as_view(), name='hr-landing'),
    re_path(r'^blog/$', HRLandingView.as_view(), {'list': True},
        name='hr-listing'),

    re_path(r'^tags/$', RedirectView.as_view(
        url=reverse_lazy('hrinsider:hr-landing'), permanent=True)),

    re_path(r'^tags/loadmore-article/$', HRTagLoadArticleView.as_view(),
        name='hr-tag-article-load'),

    re_path(r'^article/loadmore-article/$', HRArticleLoadMoreView.as_view(),
        name='hr-article-load-more'),

    re_path(r'^tags/(?P<slug>[-\w]+)/$', HRBlogTagView.as_view(),
        name='hr-tag-article'),

    re_path(r'^blog/(?P<slug>[-\w]+)/$',
        HRBlogDetailView.as_view(), name='hr-articles-detail'),

    re_path(r'^hr-conclave/$', HrConclaveLandingView.as_view(),
        name='hr-conclave'),
    re_path(r'^hr-conclave/(?P<slug>[-\w]+)/$', HrConclaveDetailView.as_view(),
        name='conclave-detail'),

    re_path(r'^jobfair/$', HrJobFairLandingView.as_view(),
        name='jobfair'),
    re_path(r'^jobfair/(?P<slug>[-\w]+)/$', HrJobFairDetailView.as_view(),
        name='jobfair-detail'),
]


# mobile page url

urlpatterns += [
    
]