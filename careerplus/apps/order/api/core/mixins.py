from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

from . import serializers
from order import models


class OrderItemViewMixin(object):

    queryset = models.OrderItem.objects.all()
    serializer_class = serializers.OrderItemSerializer
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    filter_fields = ('order', 'partner', 'product', 'is_combo', 'is_variation')
    search_fields = ('=order__id', '^partner_name', '=product__id', '^product__name', 'title')
    order_fields = ('id', 'order', 'partner', 'product', 'is_combo', 'is_variation')
    ordering = ('-id')
    pagination_class = PageNumberPagination
