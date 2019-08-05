from rest_framework.generics import ListAPIView,RetrieveAPIView
from rest_framework.views import APIView
from shop.models import (Product, ProductScreen)
from .serializers import ProductListSerializerForAuditHistory,ProductDetailSerializer
from rest_framework.authentication import SessionAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from shared.rest_addons.mixins import FieldFilterMixin
from rest_framework.response import Response
from .tasks import delete_from_solr
from shared.permissions import HasGroupOrHasPermissions
from shop.api.core.permissions import IsVendorAssociated
import subprocess, os
from django.conf import settings


class ProductListView(FieldFilterMixin, ListAPIView):
    serializer_class = ProductListSerializerForAuditHistory
    authentication_classes = (SessionAuthentication,)
    # filter_backends = (DjangoFilterBackend,)
    permission_classes = (HasGroupOrHasPermissions,IsVendorAssociated,)
    permission_groups = []
    permission_code_name = []

    def get_queryset(self):
        """
        Return product List only if any of filter fields is present in
        query params.

        category_id = Category id to be added
        vendor_id = Multiple vendor to be added with ',' separated
        type_flow = enter the product type flow

        """
        filter_dict = {}
        category_id = self.request.GET.get('category')
        vendor_id = self.request.GET.get('vendor')
        type_flow = self.request.GET.get('type_flow')
        type_query = self.request.GET.get('type')
        user = self.request.user
        vendor_id = vendor_id if vendor_id else user.vendor_set.values_list('id',flat=True)
        if category_id:
            filter_dict.update({'categories__id': category_id})
        if vendor_id :
            vendor_id = vendor_id.split(',') if isinstance(vendor_id,str) else vendor_id
            filter_dict.update({'vendor__id__in': vendor_id})
        # else:
        #     return Product.objects.none()
        if type_flow:
            filter_dict.update({'type_flow': type_flow})

        if type_query and self.request.GET.get(type_query):
            if type_query == 'name':
                filter_dict.update({type_query + '__icontains': self.request.GET.get(type_query)})
            else:
                filter_dict.update({type_query: self.request.GET.get(type_query)})

        return Product.objects.filter(**filter_dict)


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
        type_query = self.request.GET.get('type')

        if category_id:
            filter_dict.update({'categories__id': category_id})
        if vendor_id:
            vendor_id = vendor_id.split(',')
            filter_dict.update({'vendor__id__in': vendor_id})
        if type_flow:
            filter_dict.update({'type_flow': type_flow})

        if type_query and self.request.GET.get(type_query):
            if type_query == 'name':
                filter_dict.update({type_query + '__icontains': self.request.GET.get(type_query)})
            else:
                filter_dict.update({type_query: self.request.GET.get(type_query)})

        return Product.objects.filter(**filter_dict)
#