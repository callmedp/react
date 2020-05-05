from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

from . import serializers
from cms import models


class IndexerWidgetViewMixin(object):

    queryset = models.IndexerWidget.objects.all()
    serializer_class = serializers.IndexerWidgetSerializer
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    filter_fields = ('created_by',)
    search_fields = ('heading',)
    order_fields = ('id', 'heading', 'created_by', 'created_on')
    ordering = ('-id')
    pagination_class = PageNumberPagination


class ColumnHeadingViewMixin(object):

    queryset = models.ColumnHeading.objects.all()
    serializer_class = serializers.ColumnHeadingSerializer
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    filter_fields = ('column', 'indexer')
    search_fields = ('name', '=column', '=indexer__id', '^indexer__heading')
    order_fields = ('id', 'name', 'column', 'indexer')
    ordering = ('-id')
    pagination_class = PageNumberPagination


class IndexColumnViewMixin(object):

    queryset = models.IndexColumn.objects.select_related('indexer').all()
    serializer_class = serializers.IndexColumnSerializer
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    filter_fields = ('column', 'indexer')
    search_fields = ('name', '=column', '=indexer__id', '^indexer__heading', '^url')
    order_fields = ('id', 'name', 'column', 'indexer', 'url')
    ordering = ('-id')
    pagination_class = PageNumberPagination


class WidgetViewMixin(object):

    queryset = models.Widget.objects.all()
    serializer_class = serializers.WidgetSerializer
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    filter_fields = ('widget_type', 'created_by', 'writer_designation', 'iw', 'is_external', 'is_pop_up', 'is_active')
    search_fields = ('=widget_type', 'heading', '^display_name', '^writer_designation', '=iw__id')
    order_fields = ('id', 'widget_type', 'heading', 'display_name', 'writer_designation', 'iw', 'is_external', 'is_pop_up', 'is_active', 'created_by', 'created_on')
    ordering = ('-id')
    pagination_class = PageNumberPagination


# TODO: Will change field format for relations to avoid `__` in url. Ex: <>/?created_by__name=<>&ordering=-page__publish_date
# Keeping this way for now being.
# TODO: modify pagination as per requirement further
class PageViewMixin(object):

    queryset = models.Page.objects.all()
    serializer_class = serializers.PageSerializer
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    filter_fields = ('created_by', 'is_active', 'allow_comment', 'publish_date', 'expiry_date')
    search_fields = ('name', '^parent__name', '^slug', '^url', '^title', '^heading')
    order_fields = ('id', 'name', 'slug', 'is_active', 'allow_comment', 'created_by', 'total_view', 'total_download', 'total_share', 'publish_date', 'expiry_date')
    ordering = ('-id')
    pagination_class = PageNumberPagination


class PageWidgetViewMixin(object):

    queryset = models.PageWidget.objects.all()
    serializer_class = serializers.PageWidgetSerializer
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    filter_fields = ('section', 'page', 'widget', 'ranking')
    search_fields = ('section', '=ranking', '=page__id', '^page__name', 'widget__id', '^widget__name')
    order_fields = ('id', 'ranking', 'section', 'page', 'widget', 'created_by', 'created_on')
    ordering = ('-id')
    pagination_class = PageNumberPagination


class DocumentViewMixin(object):

    queryset = models.Document.objects.all()
    serializer_class = serializers.DocumentSerializer
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    filter_fields = ('page', 'is_active', 'priority')
    search_fields = ('page','^page__name')
    order_fields = ('id', 'is_active', 'priority', 'page')
    ordering = ('-id')
    pagination_class = PageNumberPagination


# TODO: decide terminology on confict in page num and page attr
class CommentViewMixin(object):

    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    filter_fields = ('page', 'is_published', 'is_removed')
    search_fields = ('page','^page__name', 'message', '=publish_date')
    order_fields = ('id', 'page', 'is_published', 'is_removed')
    ordering = ('-id')
    pagination_class = PageNumberPagination


class PageCounterViewMixin(object):

    queryset = models.PageCounter.objects.all()
    serializer_class = serializers.PageCounterSerializer
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    filter_fields = ('page', 'count_period', 'added_on')
    search_fields = ('=page__id', '^page__name')
    order_fields = ('id', 'page', 'count_period', 'no_views', 'no_downloads', 'no_shares', 'comment_count', 'added_on', 'modified_on')
    ordering = ('-id')
    pagination_class = PageNumberPagination
