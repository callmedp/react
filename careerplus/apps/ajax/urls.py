from django.conf.urls import url

from .views import AjaxCommentLoadMoreView, CmsShareView,\
   ArticleShareView, ArticleCommentView


urlpatterns = [
    url(r'^page/load-more/$',
    	AjaxCommentLoadMoreView.as_view(), name='comment-load-more'),

    url(r'^page/cms-share/$',
    	CmsShareView.as_view(), name='cms-share'),

    url(r'^article-share/$',
    	ArticleShareView.as_view(), name='article-share'),

    url(r'^article-comment/$',
    	ArticleCommentView.as_view(), name='article-comment-post'),

]