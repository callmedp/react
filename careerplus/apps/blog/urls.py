# from django.conf.urls import url
from django.urls import re_path

from .views import BlogLandingPageView, BlogLandingAjaxView,\
    BlogDetailView, BlogDetailAjaxView,\
    LoginToCommentView, ShowCommentBoxView, LoadMoreCommentView,\
    BlogTagListView, RegisterToCommentView

from . import mobile_view

app_name ='blog'
urlpatterns = [
    re_path(r'^$', BlogLandingPageView.as_view(), name='blog-landing'),

    re_path(r'^category-wise-loading/$', BlogLandingAjaxView.as_view(),
        name='blog-landing-load'),

    re_path(r'^tags/(?P<slug>[-\w]+)/$', BlogTagListView.as_view(),
        name='articles-by-tag'),

    re_path(r'^ajax/article-detail-loading/$', BlogDetailAjaxView.as_view(),
        name='article-detail-loading'),

    re_path(r'^show-comment-box/$', ShowCommentBoxView.as_view(),
        name='article-show-comment-box'),

    re_path(r'^load-more-comment/$', LoadMoreCommentView.as_view(),
        name='article-load-more-comment'),

    re_path(r'^(?P<slug>[-\w]+)/(?P<pk>\d+)/$',
        BlogDetailView.as_view(), name='articles-deatil'),

    re_path(r'^login-to-comment/$',
        LoginToCommentView.as_view(), name='login-to-comment'),

    re_path(r'^register-to-comment/$',
        RegisterToCommentView.as_view(), name='register-to-comment'),

]


# mobile page url

urlpatterns += [
    re_path(r'^categories/$', mobile_view.ArticleCategoryListMobile.as_view(),
        name='article-mobile-categories'),
    re_path(r'^lodemore-articlebycategory/$',
        mobile_view.ArticleLoadMoreMobileView.as_view(),
        name='lodemore-articlebycategory'),

    re_path(r'^lodemore-articlebytag/$',
        mobile_view.ArticleLoadMoreTagView.as_view(),
        name='lodemore-articlebytag'),
]