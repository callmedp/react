from django.conf.urls import url
from .views import PageListPartial, CommentListPartial, PageDetailPartial, PageAddPartial

urlpatterns = [
	url(r'^page/$', PageListPartial.as_view(), name='page-list-partial'),
	url(r'^comment/$', CommentListPartial.as_view(), name='comment-list-partial'),
	url(r'^page/(?P<pk>\d+)/$', PageDetailPartial.as_view(), name='page-detail-partial'),
	url(r'^page/(?P<pk>\d+)/add/$', PageAddPartial.as_view(), name='page-add-partial'),
]
