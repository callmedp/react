from django.conf.urls import url

from .views import AjaxCommentLoadMoreView
urlpatterns = [
    url(r'^page/load-more/$',
    	AjaxCommentLoadMoreView.as_view(), name='comment-load-more'),
    
]