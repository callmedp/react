from django.conf.urls import url
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView

from .views import TalentEconomyLandingView, TEBlogCategoryListView,\
    TEBlogDetailView, AuthorListingView, AuthorDetailView,\
    TalentDetailAjaxView, TETagArticleView
#     LoginToCommentView, ShowCommentBoxView, LoadMoreCommentView,\
#     BlogTagListView, RegisterToCommentView


urlpatterns = [
    url(r'^$', TalentEconomyLandingView.as_view(), name='talent-landing'),

    url(r'^authors/$', AuthorListingView.as_view(), name='authors-listing'),
    url(r'^authors/(?P<slug>[-\w]+)/$', AuthorDetailView.as_view(), name='authors-detail'),
    url(r'^ajax/talent-detail-loading/$', TalentDetailAjaxView.as_view(),
        name='talent-detail-loading'),

    url(r'^tags/$', RedirectView.as_view(
        url=reverse_lazy('talent:talent-landing'), permanent=True)),
    url(r'^tags/(?P<slug>[-\w]+)/$', TETagArticleView.as_view(),
        name='te-articles-by-tag'),

    url(r'^(?P<cat_slug>[-\w]+)/(?P<slug>[-\w]+)/$',
        TEBlogDetailView.as_view(), name='te-articles-detail'),
    url(r'^(?P<slug>[-\w]+)/$', TEBlogCategoryListView.as_view(),
        name='te-articles-by-category'),

]


# mobile page url

urlpatterns += [

]
