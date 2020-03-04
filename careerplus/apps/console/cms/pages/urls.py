# from django.conf.urls import url
from django.urls import re_path
from .import views

app_name = 'console'

urlpatterns = [
	re_path(r'^indexerwidget/$', views.IndexerWidgetListView.as_view(), name='indexerwidget-list'),
	re_path(r'^columnheading/$', views.ColumnHeadingListView.as_view(), name='columnheading-list'),
	re_path(r'^indexcolumn/$', views.IndexColumnListView.as_view(), name='indexcolumn-list'),
	re_path(r'^widget/$', views.WidgetListView.as_view(), name='widget-list'),
	re_path(r'^page/$', views.PageListView.as_view(), name='page-list'),
	re_path(r'^pagewidget/$', views.PageWidgetListView.as_view(), name='pagewidget-list'),
	re_path(r'^document/$', views.DocumentListView.as_view(), name='document-list'),
	re_path(r'^comment/$', views.CommentListView.as_view(), name='comment-list'),
	re_path(r'^pagecounter/$', views.PageCounterListView.as_view(), name='pagecounter-list'),
	re_path(r'^indexerwidget/add/$', views.IndexerWidgetAddView.as_view(), name='indexerwidget-add'),
	re_path(r'^columnheading/add/$', views.ColumnHeadingAddView.as_view(), name='columnheading-add'),
	re_path(r'^indexcolumn/add/$', views.IndexColumnAddView.as_view(), name='indexcolumn-add'),
	re_path(r'^widget/add/$', views.WidgetAddView.as_view(), name='widget-add'),
	re_path(r'^page/add/$', views.PageAddView.as_view(), name='page-add'),
	re_path(r'^pagewidget/add/$', views.PageWidgetAddView.as_view(), name='pagewidget-add'),
	re_path(r'^document/add/$', views.DocumentAddView.as_view(), name='document-add'),
	re_path(r'^comment/add/$', views.CommentAddView.as_view(), name='comment-add'),
	re_path(r'^pagecounter/add/$', views.PageCounterAddView.as_view(), name='pagecounter-add'),
	re_path(r'^indexerwidget/(?P<pk>\d+)/$', views.IndexerWidgetDetailView.as_view(), name='indexerwidget-detail'),
	re_path(r'^columnheading/(?P<pk>\d+)/$', views.ColumnHeadingDetailView.as_view(), name='columnheading-detail'),
	re_path(r'^indexcolumn/(?P<pk>\d+)/$', views.IndexColumnDetailView.as_view(), name='indexcolumn-detail'),
	re_path(r'^widget/(?P<pk>\d+)/$', views.WidgetDetailView.as_view(), name='widget-detail'),
	re_path(r'^page/(?P<pk>\d+)/$', views.PageDetailView.as_view(), name='page-detail'),
	re_path(r'^pagewidget/(?P<pk>\d+)/$', views.PageWidgetDetailView.as_view(), name='pagewidget-detail'),
	re_path(r'^document/(?P<pk>\d+)/$', views.DocumentDetailView.as_view(), name='document-detail'),
	re_path(r'^comment/(?P<pk>\d+)/$', views.CommentDetailView.as_view(), name='comment-detail'),
	re_path(r'^pagecounter/(?P<pk>\d+)/$', views.PageCounterDetailView.as_view(), name='pagecounter-detail'),
]
