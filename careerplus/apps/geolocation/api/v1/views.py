from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models.query import QuerySet

from geolocation.api.core import serializers
from geolocation import models


class CurrencyViewSet(ReadOnlyModelViewSet):
    """
        R Viewset for `Currency` model.
    """
    queryset = models.Currency.objects.all()
    serializer_class = serializers.CurrencySerializer
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    filter_fields = ('id', 'name', 'active', 'value')
    search_fields = ('^name',)
    order_fields = ('id', 'name', 'active', 'value', 'exchange_rate')
    ordering = ('-id',)
    pagination_class = None

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs, limit_fields=((self.request.GET.get('id', None) != None) or (self.request.GET.get('name', None) != None) or (self.request.GET.get('value', None) != None)))


class CityViewSet(ReadOnlyModelViewSet):
    """
        R Viewset for `City` model.
    """
    queryset = models.City.objects.all()
    serializer_class = serializers.CitySerializer
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    filter_fields = ('id', 'code_city', 'country')
    search_fields = ('^name', '^country')
    order_fields = ('id', 'name', 'country', 'code_city', 'timezone')
    ordering = ('-id',)
    pagination_class = None

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs, limit_fields=(self.request.GET.get('country', None) != None))
