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
from django.core.cache import cache
from django.conf import settings
from shared.rest_addons.authentication import ShineUserAuthentication
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import PermissionDenied

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
            if data['status'] == 'done':
                session_id = request.session.session_key
                cache.set('{}_neo_email_done'.format(session_id), email, 3600 * 24 * 30)
            return Response(data)
        else:
            return Response({'message': 'Invalid Email'.format(email)}, status=status.HTTP_400_BAD_REQUEST)

class BoardNeoProductApiView(APIView):
    authentication_classes = (ShineUserAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        from order.models import OrderItem
        from order.tasks import board_user_on_neo
        self.candidate_id = request.session.get('candidate_id', None)
        self.oi_pk = request.data.get('oi_pk')
        if self.oi_pk and self.candidate_id:
            self.oi = OrderItem.objects.select_related("order").filter(pk=self.oi_pk).first()
            if (
                self.oi and self.oi.product.vendor.slug == 'neo'\
                and self.oi.order.candidate_id == self.candidate_id\
                and self.oi.order.status in [1, 3]
            ):
                board_user_on_neo.delay([self.oi.id])
                return Response({'message': 'Mail sent fro verification on neo'})

        raise PermissionDenied


