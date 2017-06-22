from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAdminUser

from . import serializers
from partner import models


class VendorViewMixin(object):

    queryset = models.Vendor.objects.all()
    serializer_class = serializers.VendorSerializer
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    filter_fields = ('email', 'country', 'state', 'city')
    search_fields = ('name', '^email', '^country', '^state', '^city', '^pan', 'website')
    order_fields = ('id', 'email', 'country', 'state', 'city', 'created', 'modified')
    ordering = ('-id')
    pagination_class = PageNumberPagination
    permission_classes = (IsAdminUser,)

class VendorHierarchyViewMixin(object):

    queryset = models.VendorHierarchy.objects.all()
    serializer_class = serializers.VendorHierarchySerializer
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    filter_fields = ('vendee', 'employee', 'designation')
    search_fields = ('=designation', '=vendee_id', '^vendee_name', '=employee__id', '^employee_name')
    order_fields = ('id', 'vendee', 'employee', 'created', 'modified')
    ordering = ('-id')
    pagination_class = PageNumberPagination
    permission_classes = (IsAdminUser,)
