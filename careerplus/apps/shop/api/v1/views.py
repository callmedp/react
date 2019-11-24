
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.views import APIView
from rest_framework import status
from shop.models import (Product, ProductScreen, PracticeTestInfo)
from .serializers import (
    ProductListSerializerForAuditHistory,
    ProductDetailSerializer,
    PracticeTestInfoCreateSerializer,
    UpdateProductScreenSkillSerializer,
    UpdateProductSkillSerializer
)
from rest_framework.authentication import SessionAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from shared.rest_addons.mixins import FieldFilterMixin
from rest_framework.response import Response
from .tasks import delete_from_solr, update_practice_test_info
from shared.permissions import HasGroupOrHasPermissions
from shop.api.core.permissions import IsVendorAssociated

import subprocess, os
from rest_framework.generics import RetrieveAPIView
from django.core.cache import cache
from django.conf import settings
from shared.rest_addons.authentication import ShineUserAuthentication
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import PermissionDenied
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from shop.helpers import get_inferred_skills
from rest_framework.response import Response
from rest_framework import status

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
        if vendor_id and not user.is_superuser:
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

        return Product.objects.filter(**filter_dict).exclude(type_flow=14)


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


class CreatePracticeTestInfoAPIView(CreateAPIView):
    serializer_class = PracticeTestInfoCreateSerializer
    authentication_classes = ()
    permission_classes = ()

    @method_decorator(csrf_protect)
    def dispatch(self, request, *args, **kwargs):
        return super(CreatePracticeTestInfoAPIView, self).dispatch(request, *args, **kwargs)


class UpdatePracticeInfoApiView(APIView):
    authentication_classes = ()
    permission_classes = ()

    @method_decorator(csrf_protect)
    def dispatch(self, request, *args, **kwargs):
        return super(UpdatePracticeInfoApiView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        email = request.query_params.get('email', None)
        if email:
            self.kwargs['email'] = email
        else:
            return Response({'email: Provide this field'}, status=status.HTTP_400_BAD_REQUEST)
        data = update_practice_test_info(email)
        if data:
            if data.get('status', None) != 400:
                if data['status'] == 'done':
                    session_id = request.session.session_key
                    cache.set('{}_neo_email_done'.format(session_id), email, 3600 * 24 * 30)
                    from .tasks import create_neo_lead
                    create_neo_lead.delay(email)
                return Response(data)
            else:
                return Response({'message': 'Already Registered'.format(email)}, status=status.HTTP_404_NOT_FOUND)
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
                if not self.oi.neo_mail_sent:
                    boarding_type = board_user_on_neo([self.oi.id])
                    msg = 'Please check you mail to confirm boarding on Neo'
                    if boarding_type == 'already_trial':
                        msg = 'You Account has been Updated from Trial To Regular'
                    return Response({'msg': msg})

        raise PermissionDenied


class ParseSkillFromTextApiView(APIView):
    """
    This APIView takes text as input and return
    parsed skills from text.
    """

    authentication_classes = ()
    permission_classes = ()


    def post(self, request, *args, **kwargs):
        text = request.data.get('text', '')
        k = get_inferred_skills(text)
        return Response(data=k, status=status.HTTP_200_OK)


class UpdateScreenProductSkillView(CreateAPIView):
    """
    This API endpoint takes data in the format of
    {
        "user_type": [<skill_name1>,<skill_name2>],
        "product_type": [<skill_name3>,<skill_name4>],
        "product_id": <product_id>
    }
    and update skill for productscreen
    """
    serializer_class = UpdateProductScreenSkillSerializer
    permission_classes = (IsAuthenticated, )
    authentication_classes = (SessionAuthentication, )

class UpdateProductSkillView(CreateAPIView):
    """
    This API endpoint takes data in the format of
    {
        "user_type": [<skill_name1>,<skill_name2>],
        "product_type": [<skill_name3>,<skill_name4>],
        "product_id": <product_id>
    }
    and update skill for product
    """
    serializer_class = UpdateProductSkillSerializer
    permission_classes = (IsAuthenticated, )
    authentication_classes = (SessionAuthentication, )



