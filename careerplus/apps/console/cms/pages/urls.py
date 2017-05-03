from django.conf.urls import url
from .views import PageListView, PageDetailView, PageAddView, CommentListView

urlpatterns = [
	url(r'^page/$', PageListView.as_view(), name='page-list'),
	url(r'^page/$', PageListView.as_view(), name='page-list'),
	url(r'^comment/$', CommentListView.as_view(), name='comment-list'),
	url(r'^page/add/$', PageAddView.as_view(), name='page-add'),
	url(r'^page/(?P<pk>\d+)/$', PageDetailView.as_view(), name='page-detail'),
]
