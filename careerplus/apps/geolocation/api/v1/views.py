# python imports
import base64, json, logging
import random
from datetime import datetime, date

# django imports
from django.conf import settings
from django.template.loader import get_template
from django.core.files.uploadedfile import SimpleUploadedFile
from django_redis import get_redis_connection

# local imports
from geolocation.models import Country

# inter app imports

# third party imports
from rest_framework.generics import (ListAPIView)
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models.query import QuerySet
from geolocation.api.core.serializers import (CurrencySerializer, CitySerializer, CountrySerializer)
from geolocation import models


class CurrencyViewSet(ReadOnlyModelViewSet):
    """
        R Viewset for `Currency` model.
    """
    queryset = models.Currency.objects.all()
    serializer_class = CurrencySerializer
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    filter_fields = ('id', 'name', 'active', 'value')
    search_fields = ('^name',)
    order_fields = ('id', 'name', 'active', 'value', 'exchange_rate')
    ordering = ('-id',)
    pagination_class = None

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        limit_fields = ((self.request.GET.get('id', None) != None) or (self.request.GET.get('name', None) != None) or (
                self.request.GET.get('value', None) != None))
        return serializer_class(*args, limit_fields=limit_fields, **kwargs)


class CityViewSet(ReadOnlyModelViewSet):
    """
        R Viewset for `City` model.
    """
    queryset = models.City.objects.all()
    serializer_class = CitySerializer
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    filter_fields = ('id', 'code_city', 'country')
    search_fields = ('^name', '^country')
    order_fields = ('id', 'name', 'country', 'code_city', 'timezone')
    ordering = ('-id',)
    pagination_class = None

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        limit_fields = (self.request.GET.get('country', None) != None)
        return serializer_class(*args, limit_fields=limit_fields, **kwargs)


class StandardResultSetPagination(PageNumberPagination):
    page_size_query_param = "page_size"
    max_page_size = 10000


class CountryListView(ListAPIView):
    authentication_classes = ()
    permission_classes = ()
    pagination_class = StandardResultSetPagination
    serializer_class = CountrySerializer

    def get_queryset(self):
        search_text = self.request.GET.get('search')
        query_value_list = []

        if search_text is not None:
            return Country.objects.only('id', 'name', ).filter(active=True, name__icontains=search_text)

        else:
            return Country.objects.only('id', 'name', ).filter(active=True)
