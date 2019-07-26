from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.views import APIView
from rest_framework import status
from shop.models import (Product, ProductScreen, PracticeTestInfo)
from .serializers import (
    ProductListSerializerForAuditHistory,
    PracticeTestInfoCreateSerializer
)
from rest_framework.authentication import SessionAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from shared.rest_addons.mixins import FieldFilterMixin
from rest_framework.response import Response
from .tasks import delete_from_solr, update_practice_test_info
import subprocess, os
from rest_framework.generics import RetrieveAPIView

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


class CreatePracticeTestInfoAPIView(CreateAPIView):
    serializer_class = PracticeTestInfoCreateSerializer
    authentication_classes = ()
    permission_classes = ()

class UpdatePracticeInfoApiView(APIView):
    authentication_classes = ()
    permission_classes = ()


    def get(self, request, *args, **kwargs):
        email = request.query_params.get('email', None)
        if email:
            self.kwargs['email'] = email
        else:
            return Response({'email: Provide this field'}, status=status.HTTP_400_BAD_REQUEST)
        data = update_practice_test_info(email)
        if data:
            return Response(data)
        else:
            return Response({'message': 'Invalid Email'.format(email)}, status=status.HTTP_400_BAD_REQUEST)

