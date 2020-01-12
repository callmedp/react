from django.conf.urls import url

from .views import BlogLandingPageView, BlogLandingAjaxView,\
    BlogDetailView, BlogDetailAjaxView,\
    LoginToCommentView, ShowCommentBoxView, LoadMoreCommentView,\
    BlogTagListView, RegisterToCommentView

from . import mobile_view

app_name ='blog'
urlpatterns = [
    url(r'^$', BlogLandingPageView.as_view(), name='blog-landing'),

    url(r'^category-wise-loading/$', BlogLandingAjaxView.as_view(),
        name='blog-landing-load'),

    url(r'^tags/(?P<slug>[-\w]+)/$', BlogTagListView.as_view(),
        name='articles-by-tag'),

    url(r'^ajax/article-detail-loading/$', BlogDetailAjaxView.as_view(),
        name='article-detail-loading'),

    url(r'^show-comment-box/$', ShowCommentBoxView.as_view(),
        name='article-show-comment-box'),

    url(r'^load-more-comment/$', LoadMoreCommentView.as_view(),
        name='article-load-more-comment'),

    url(r'^(?P<slug>[-\w]+)/(?P<pk>\d+)/$',
        BlogDetailView.as_view(), name='articles-deatil'),

    url(r'^login-to-comment/$',
        LoginToCommentView.as_view(), name='login-to-comment'),

    url(r'^register-to-comment/$',
        RegisterToCommentView.as_view(), name='register-to-comment'),

]


# mobile page url

urlpatterns += [
    url(r'^categories/$', mobile_view.ArticleCategoryListMobile.as_view(),
        name='article-mobile-categories'),
    url(r'^lodemore-articlebycategory/$',
        mobile_view.ArticleLoadMoreMobileView.as_view(),
        name='lodemore-articlebycategory'),

    url(r'^lodemore-articlebytag/$',
        mobile_view.ArticleLoadMoreTagView.as_view(),
        name='lodemore-articlebytag'),
]