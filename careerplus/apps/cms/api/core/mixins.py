from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import PageSerializer, CommentSerializer
from cms.models import Page, Comment


# TODO: Will change field format for relations to avoid `__` in url. Ex: <>/?created_by__name=<>&ordering=-page__publish_date
# Keeping this way for now being.
# TODO: modify pagination as per requirement further
class PageViewMixin(object):

    queryset = Page.objects.all()
    serializer_class = PageSerializer
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    filter_fields = ('created_by', 'is_active', 'allow_comment', 'publish_date', 'expiry_date')
    search_fields = ('name', '^parent', 'slug', '^created_by', '^url', 'title', '^heading', '=publish_date')
    order_fields = ('id', 'name', 'slug', 'is_active', 'allow_comment', 'created_by', 'total_view', 'total_download', 'total_share', 'publish_date', 'expiry_date')
    ordering = ('-id')
    pagination_class = PageNumberPagination


# TODO: decide terminology on confict in page num and page attr
class CommentViewMixin(object):

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    filter_fields = ('page', 'is_published', 'is_removed')
    search_fields = ('page','^page__name', 'message', '=publish_date')
    order_fields = ('id', 'page', 'is_published', 'is_removed')
    ordering = ('-id')
    pagination_class = PageNumberPagination
