from django.conf.urls import url

from .views import AjaxCommentLoadMoreView, CmsShareView, \
CheckLoginStatus, AjaxProductLoadMoreView

urlpatterns = [
    url(r'^page/load-more/$',
    	AjaxCommentLoadMoreView.as_view(), name='comment-load-more'),

    url(r'^page/cms-share/$',
    	CmsShareView.as_view(), name='cms-share'),

    url(r'^login-status/$',
    	CheckLoginStatus.as_view(), name='login-status'),

    url(r'^product/load-more/$',
        AjaxProductLoadMoreView.as_view(), name='product-load-more'),
    
]