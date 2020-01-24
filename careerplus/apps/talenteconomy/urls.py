# from django.conf.urls import url
from django.urls import re_path,reverse_lazy
from django.views.generic import RedirectView

from .views import TalentEconomyLandingView, TEBlogCategoryListView,\
    TEBlogDetailView, AuthorListingView, AuthorDetailView,\
    TECategoryArticleLoadView, TETagArticleView, TETagLoadmoreArticleView,TalentEconomyLoadMoreView
#     LoginToCommentView, ShowCommentBoxView, LoadMoreCommentView,\
#     BlogTagListView, RegisterToCommentView

app_name = 'talenteconomy'
urlpatterns = [
    re_path(r'^$', TalentEconomyLandingView.as_view(), name='talent-landing'),
    re_path(r'^load-more-article/$', TalentEconomyLoadMoreView.as_view(),
        name='talent-landing-more'),

    re_path(r'^authors/$', AuthorListingView.as_view(), name='authors-listing'),
    re_path(r'^authors/(?P<slug>[-\w]+)/$', AuthorDetailView.as_view(), name='authors-detail'),
    re_path(r'^ajax/te-category-article-load/$', TECategoryArticleLoadView.as_view(),
        name='te-cat-article-load'),

    re_path(r'^tags/$', RedirectView.as_view(
        url=reverse_lazy('talent:talent-landing'), permanent=True)),
    re_path(r'^tags/loadmore-article/$', TETagLoadmoreArticleView.as_view(),
        name='te-tag-loadmore-article'),


    re_path(r'^tags/(?P<slug>[-\w]+)/$', TETagArticleView.as_view(),
        name='te-articles-by-tag'),

    re_path(r'^(?P<cat_slug>[-\w]+)/(?P<slug>[-\w]+)/$',
        TEBlogDetailView.as_view(), name='te-articles-detail'),
    re_path(r'^(?P<slug>[-\w]+)/$', TEBlogCategoryListView.as_view(),
        name='te-articles-by-category'),

]


# mobile page url

urlpatterns += [

]
