# python imports
import base64, json, logging
import random, string
from datetime import datetime, date

# django imports
from django.conf import settings
from django.template.loader import get_template
from django.core.files.uploadedfile import SimpleUploadedFile
from django_redis import get_redis_connection
from django.db.models import Q

# local imports
from geolocation.models import Country

# inter app imports

# third party imports
from rest_framework.generics import (ListAPIView)
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from django.db.models.query import QuerySet
from geolocation.api.core.serializers import (CurrencySerializer, CitySerializer, CountrySerializer)
from geolocation import models
from rest_framework import status


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
            return Country.objects.only('id', 'name','phone', ).filter(active=True).\
                    filter(Q(name__icontains=search_text)| Q(phone__icontains=search_text) )

        else:
            return Country.objects.only('id', 'name', ).filter(active=True)



class CountryValidationView(APIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = None


    def extract_phone_number(self, phone_number):
        if not phone_number:
            return ''

        phone_number = ''.join([digit for digit in phone_number if digit in string.digits + '+'])

        if phone_number.startswith('00'): #international number
            phone_number = '+' + phone_number[2:]
        elif phone_number.startswith('+91') and len(phone_number) != 13:
            phone_number = ''
        elif phone_number.startswith('91') and len(phone_number) == 12:
            phone_number = phone_number[2:]
        elif phone_number.startswith('0') and len(phone_number) == 11:
            phone_number = phone_number[1:]

        if not phone_number.startswith('+') and not len(phone_number) == 10:
            phone_number = ''

        phone_number = '+91' + phone_number if len(phone_number) == 10 and not phone_number.startswith('+') else phone_number

        return phone_number


    def validate_phone_number(self, data):
        self.cell_phone = data['cell_phone']
        self.country_code = data['country_code']
        def is_digit(character):
            return character.isdigit()

        cell_phone = self.extract_phone_number(
            self.cell_phone)[-10:] if '91' in self.country_code else \
            ''.join(filter(is_digit, self.cell_phone))

        if not self.country_code or not cell_phone:
            return False

        if self.country_code in ['91', '44', '1'] and \
                len(cell_phone) > 10 and not cell_phone.startswith('0'):
            return False

        if len(cell_phone) + len(self.country_code) > 16:
            return False

        if len(cell_phone) < 6:
            return False

        if cell_phone in ['9999999999', '8888888888', '9876543210',
                        '7777777777', '9000000000', '8000000000',
                        '9898989898',
                        '6666666666']:
            return False

        if self.country_code == '91' and cell_phone[0] in ['0', '1', '2', '3',
                                                        '4', '5']:
            return False
        
        return True


    def get(self, request, *args, **kwargs):
        country_code = request.GET.get('country_code','')
        mobile = request.GET.get('mobile','')
        data = {"cell_phone": mobile, "country_code": country_code}
        is_valid = self.validate_phone_number(data)

        return Response(
            data={'result': is_valid},
            status=status.HTTP_200_OK
        )
    


    

