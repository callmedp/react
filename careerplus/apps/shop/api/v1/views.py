from rest_framework.generics import ListAPIView,RetrieveAPIView
from rest_framework.views import APIView
from shop.models import (Product, ProductScreen)
from .serializers import ProductListSerializerForAuditHistory,ProductDetailSerializer
from rest_framework.authentication import SessionAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from shared.rest_addons.mixins import FieldFilterMixin
from rest_framework.response import Response
from .tasks import delete_from_solr
import subprocess, os
from django.conf import settings


class ProductListView(FieldFilterMixin, ListAPIView):
    serializer_class = ProductListSerializerForAuditHistory
    authentication_classes = (SessionAuthentication,)
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('vendor',)

    def get_queryset(self):
        """
        Return product List only if any of filter fields is present in
        query params.
        """
        for fltr in self.filter_fields:
            val = self.request.GET.get(fltr, None)
            if val is not None:
                return Product.objects.all()
        return Product.objects.none()


class ProductDeleteView(APIView):
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        id_list = request.data.get('data', '')
        products = Product.objects.filter(slug__in=id_list)
        product_screens = ProductScreen.objects.filter(slug__in=id_list)
        product_count = 0
        product_screen_count = 0

        if products.exists() or product_screens.exists():
            # get product count
            product_count = len(products)

            # get product screen count
            product_screen_count = len(product_screens)

            # bulk deletion of the products

            if product_screen_count > 0:
                product_screens.delete()

            if product_count > 0:
                products.delete()

            delete_from_solr.delay()

        return Response({'message': '{} products deleted and {} product screens deleted'.format(product_count,
                                                                                                product_screen_count)},
                        status=200)


class ProductDetailView(FieldFilterMixin, ListAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = ProductDetailSerializer

    def get_queryset(self):
        filter_dict = {}
        category_id = self.request.GET.get('category')
        vendor_id = self.request.GET.get('vendor')
        type_flow = self.request.GET.get('type_flow')
        if category_id:
            filter_dict.update({'categories__id': category_id})
        if vendor_id:
            filter_dict.update({'vendor__id': vendor_id})
        if type_flow:
            filter_dict.update({'type_flow': type_flow})

        return Product.objects.filter(**filter_dict)