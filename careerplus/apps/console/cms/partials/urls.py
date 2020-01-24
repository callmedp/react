# from django.conf.urls import url
from django.urls import re_path

from . import views

app_name = 'console'

urlpatterns = [
	re_path(r'^indexerwidget/$', views.IndexerWidgetListPartial.as_view(), name='indexerwidget-list-partial'),
	re_path(r'^columnheading/$', views.ColumnHeadingListPartial.as_view(), name='columnheading-list-partial'),
	re_path(r'^indexcolumn/$', views.IndexColumnListPartial.as_view(), name='indexcolumn-list-partial'),
	re_path(r'^widget/$', views.WidgetListPartial.as_view(), name='widget-list-partial'),
	re_path(r'^page/$', views.PageListPartial.as_view(), name='page-list-partial'),
	re_path(r'^pagewidget/$', views.PageWidgetListPartial.as_view(), name='pagewidget-list-partial'),
	re_path(r'^document/$', views.DocumentListPartial.as_view(), name='document-list-partial'),
	re_path(r'^comment/$', views.CommentListPartial.as_view(), name='comment-list-partial'),
	re_path(r'^pagecounter/$', views.PageCounterListPartial.as_view(), name='pagecounter-list-partial'),
	re_path(r'^indexerwidget/add/$', views.IndexerWidgetAddPartial.as_view(), name='indexerwidget-add-partial'),
	re_path(r'^columnheading/add/$', views.ColumnHeadingAddPartial.as_view(), name='columnheading-add-partial'),
	re_path(r'^indexcolumn/add/$', views.IndexColumnAddPartial.as_view(), name='indexcolumn-add-partial'),
	re_path(r'^widget/add/$', views.WidgetAddPartial.as_view(), name='widget-add-partial'),
	re_path(r'^page/add/$', views.PageAddPartial.as_view(), name='page-add-partial'),
	re_path(r'^pagewidget/add/$', views.PageWidgetAddPartial.as_view(), name='pagewidget-add-partial'),
	re_path(r'^document/(?P<pk>\d+)/add/$', views.DocumentAddPartial.as_view(), name='document-add-partial'),
	re_path(r'^comment/add/$', views.CommentAddPartial.as_view(), name='comment-add-partial'),
	re_path(r'^pagecounter/add/$', views.PageCounterAddPartial.as_view(), name='pagecounter-add-partial'),
	re_path(r'^indexerwidget/(?P<pk>\d+)/$', views.IndexerWidgetDetailPartial.as_view(), name='indexerwidget-detail-partial'),
	re_path(r'^columnheading/(?P<pk>\d+)/$', views.ColumnHeadingDetailPartial.as_view(), name='columnheading-detail-partial'),
	re_path(r'^indexcolumn/(?P<pk>\d+)/$', views.IndexColumnDetailPartial.as_view(), name='indexcolumn-detail-partial'),
	re_path(r'^widget/(?P<pk>\d+)/$', views.WidgetDetailPartial.as_view(), name='widget-detail-partial'),
	re_path(r'^page/(?P<pk>\d+)/$', views.PageDetailPartial.as_view(), name='page-detail-partial'),
	re_path(r'^pagewidget/(?P<pk>\d+)/$', views.PageWidgetDetailPartial.as_view(), name='pagewidget-detail-partial'),
	re_path(r'^document/(?P<pk>\d+)/$', views.DocumentDetailPartial.as_view(), name='document-detail-partial'),
	re_path(r'^comment/(?P<pk>\d+)/$', views.CommentDetailPartial.as_view(), name='comment-detail-partial'),
	re_path(r'^pagecounter/(?P<pk>\d+)/$', views.PageCounterDetailPartial.as_view(), name='pagecounter-detail-partial'),
]
