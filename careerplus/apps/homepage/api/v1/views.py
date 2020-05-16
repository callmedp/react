import logging
from rest_framework.generics import RetrieveAPIView ,ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from shared.rest_addons.mixins import FieldFilterMixin
import datetime
from django.utils import timezone

from .serializers import StaticSiteContentSerializer, OrderItemDetailSerializer, DashboardCancellationSerializer
from homepage.models import StaticSiteContent,TestimonialCategoryRelationship,Testimonial
from shop.models import Category
from order.models import Order, OrderItem
from dashboard.dashboard_mixin import DashboardInfo, DashboardCancelOrderMixin
from core.api_mixin import ShineCandidateDetail

logger = logging.getLogger('error_log')


class StaticSiteView(RetrieveAPIView):
    # queryset = TermAndAgreement.objects.all()
    serializer_class = StaticSiteContentSerializer
    authentication_classes = ()
    permission_classes = ()
    lookup_field = 'page_type'

    def get_queryset(self):
        page_type = int(self.kwargs['page_type'])
        if page_type:
            return StaticSiteContent.objects.filter(page_type=page_type)
        return StaticSiteContent.objects.all()


class TestimonialCategoryMapping(APIView):
    authentication_classes = ()
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        category_ids = eval(request.POST.get('categories','[]'))
        if not category_ids:
            return HttpResponse("No Changes")
        testimonial_id = request.POST.get('testimonial','')
        prev_category_mapping_ids = set(TestimonialCategoryRelationship.objects.\
            filter(testimonial=testimonial_id).values_list('category',flat=True))
        category_ids = set(category_ids)
        # mapping testimonial to category ids and delete some relations
        category_ids_to_delete = prev_category_mapping_ids - category_ids
        category_ids_to_add = category_ids - prev_category_mapping_ids 
        categories = Category.objects.filter(id__in=category_ids_to_add).only('id')
        testimonial = Testimonial.objects.filter(id=testimonial_id).first()

        if not testimonial:
            return HttpResponse("Failed")

        if category_ids_to_delete:
            TestimonialCategoryRelationship.objects.filter(category__in=category_ids_to_delete,testimonial=testimonial_id).delete()

        for category in categories:
            TestimonialCategoryRelationship.objects.get_or_create(category=category,testimonial=testimonial)

        return HttpResponse("Successful")


class UserDashboardApi(FieldFilterMixin, ListAPIView):
    """
     This api gives all the the order items.
    """
    # authentication_classes = (IsAuthenticated)
    permission_classes = ()
    authentication_classes = ()
    serializer_class = OrderItemDetailSerializer

    def get_queryset(self, *args, **kwargs):
        email = self.request.GET.get("email", None)
        candidate_id = self.request.GET.get("candidate_id", None)
        select_type = self.request.GET.get("select_type", 0)
        days = 0

        last_month_from = self.request.GET.get("last_month_from", 18)
        try:
            days = int(last_month_from) * 30
            select_type = int(select_type)
        except:
            days = 18*30
            select_type = 0

        last_payment_date = timezone.now() - datetime.timedelta(days=days)
        queryset_list = OrderItem.objects.filter(no_process=False, order__site=2,
                                                 product__type_flow__in=[1, 12, 13, 4, 5, 8])

        if select_type == 1:
            queryset_list = queryset_list.exclude(oi_status=4)
        elif select_type == 2:
            queryset_list = queryset_list.filter(oi_status=4)

        if not email and not candidate_id:
            return queryset_list.none()

        queryset_list = queryset_list.prefetch_related('product', 'product__product_class', 'delivery_service',
                                                       'order', 'product__attributes'
                                                       ).order_by('-order__payment_date')

        if candidate_id and not email:
            return queryset_list.filter(order__candidate_id=candidate_id, order__status__in=[1, 3],
                                        order__payment_date__gte=last_payment_date)

        if email and not candidate_id:
            return queryset_list.filter(order__email=email, order__payment_date__gte=last_payment_date,
                                        order__status__in=[1, 3])

        if email and candidate_id:
            queryset_list = queryset_list.filter(order__candidate_id=candidate_id, order__status__in=[1, 3],
                                                 order__payment_date__gte=last_payment_date)
            if not queryset_list.exists():
                queryset_list = queryset_list.filter(order__email=email, order__status__in=[1, 3])

            queryset_list = queryset_list.filter(order__email=email, order__status__in=[1, 3], no_process=False,
                                                 order__site=2)

            return queryset_list


class DashboardDetailApi(APIView):
    permission_classes = ()
    authentication_classes = ()
    serializer_class = None

    def get(self, request):
        candidate_id = request.GET.get('candidate_id', '')
        orderitem_id = request.GET.get('orderitem_id')

        if not candidate_id:
            return Response({'status': 'Failure', 'error': 'candidate_id is required'},
                            status=status.HTTP_400_BAD_REQUEST)
        if not orderitem_id:
            return Response({'status': 'Failure', 'error': 'orderitem_id is required'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            order_item = OrderItem.objects.select_related('order', 'product').get(
                pk=orderitem_id, order__candidate_id=candidate_id, order__status__in=[1, 3])
        except OrderItem.DoesNotExist:
            logger.error('OrderItem for candidate_id %s and pk %s with order status in [1, 3] does not exist' %(
                candidate_id, orderitem_id))
            return Response({'status': 'Failure', 'error': 'OrderItem does not exists.'})

        ops = []

        if order_item.product.type_flow in [1, 12, 13]:
            ops = order_item.orderitemoperation_set.filter(oi_status__in=[2, 5, 24, 26, 27, 161, 162, 163, 164, 181])

        elif order_item.product.vendor.slug == 'neo':
            ops = order_item.orderitemoperation_set.filter(oi_status__in=[5, 33, 4, 161, 162, 163, 164])

        elif order_item.product.type_flow in [2, 14]:
            ops = order_item.orderitemoperation_set.filter(oi_status__in=[5, 6, 161, 162, 163, 164])

        elif order_item.product.type_flow == 3:
            ops = order_item.orderitemoperation_set.filter(oi_status__in=[2, 5, 121, 161, 162, 163, 164])
        elif order_item.product.type_flow == 4:
            ops = order_item.orderitemoperation_set.filter(oi_status__in=[2, 5, 6, 61, 161, 162, 163, 164])
        elif order_item.product.type_flow == 5:
            ops = order_item.orderitemoperation_set.filter(oi_status__in=[2, 5, 6, 61, 161, 162, 163, 164])
        elif order_item.product.type_flow == 6:
            ops = order_item.orderitemoperation_set.filter(oi_status__in=[6, 81, 82, 161, 162, 163, 164])
        elif order_item.product.type_flow in [7, 15]:
            ops = order_item.orderitemoperation_set.filter(oi_status__in=[2, 4, 5, 6, 61, 161, 162, 163, 164])
        elif order_item.product.type_flow == 8:
            oi_status_list = [2, 49, 5, 46, 48, 27, 4, 161, 162, 163, 181, 164]
            ops = order_item.orderitemoperation_set.filter(oi_status__in=oi_status_list)
        elif order_item.product.type_flow == 10:
            ops = order_item.orderitemoperation_set.filter(oi_status__in=[5, 6, 101, 161, 162, 163, 164])
        elif order_item.product.type_flow == 16:
            ops = order_item.orderitemoperation_set.filter(oi_status__in=[5, 6, 4])

        # ops = ops.values_list('id', 'oi_status', 'draft_counter', 'get_user_oi_status', 'created__date',
        #                       'oi_draft__name')

        ops = [{"id" : op.id, "oi_status" : op.oi_status, "draft_counter" : op.draft_counter,
                "get_user_oi_status" : op.get_user_oi_status, "created__date" : op.created.strftime("%b %d, ""%Y"),
                "oi_draft__name" : op.oi_draft.url if op.oi_draft else ""
                } for op in ops]


        resp_dict = {'status': 'Success', 'error': None, 'data': {'oi': {
            'oi_status': order_item.oi_status,
            'product_id': order_item.product_id,
            'product_type_flow': order_item.product.type_flow,
            'oi_resume': order_item.oi_resume.url,
            'product_sub_type_flow': order_item.product.sub_type_flow,
            'custom_operations': list(order_item.get_item_operations().values() if order_item.get_item_operations()
            else ''),
            'order_id': order_item.order_id,
            'oi_id': order_item.pk,
            'order_number': order_item.order.number,
            'product_name': order_item.product.get_name,
            'product_exp_db': order_item.product.get_exp_db(),
            'ops': ops,
        }}}

        return Response(resp_dict, status=status.HTTP_200_OK)


class DashboardNotificationBoxApi(APIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = None

    def get(self, request):
        candidate_id = request.GET.get('candidate_id', None)
        email = request.GET.get('email', None)

        if not candidate_id:
            return Response({'status': 'Failure', 'error': 'candidate_id is required.'},
                            status=status.HTTP_400_BAD_REQUEST)

        if not email:
            return Response({'status': 'Failure', 'error': 'email is required.'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            # this is order__site=2 is required to get the data for resume.shine
            pending_resume_items = DashboardInfo().get_pending_resume_items(candidate_id=candidate_id,
                                                                            email=email).filter(order__site=2)

            pending_resume_items = [{'id':oi.id,'product_name':oi.product.get_name if oi.product else ''
                                     ,'product_get_exp_db':oi.product.get_exp_db() if oi.product else ''
                                     } for oi in
                                    pending_resume_items]
            res = ShineCandidateDetail().get_candidate_detail(email=None, shine_id=candidate_id)
            resumes = res['resumes']
            default_resumes = [resume for resume in resumes if resume['is_default']][0]
        except Exception as exc:
            logger.error('Error in getting notifications %s' % exc)
            return Response({'status': 'Failure', 'error': 'Default resume does not exist'},
                            status=status.HTTP_417_EXPECTATION_FAILED)

        resp_dict = {'status': 'Success', 'error': None, 'data': {
            "resume_id": default_resumes.get('id', ''),
            "shine_resume_name": default_resumes.get('resume_name', ''),
            "resume_extn": default_resumes.get('extension', ''),
            "pending_resume_items": list(pending_resume_items)
        }}

        return Response(resp_dict, status=status.HTTP_200_OK)


class DashboardCancellationApi(APIView):

    serializer_class = DashboardCancellationSerializer

    def post(self, request):
        serializer = DashboardCancellationSerializer(request.data)
        if serializer.is_valid():
            candidate_id = serializer.data.get('candidate_id')
            email = serializer.data.get('email')
            order_id = serializer.data.get('order_id')
            try:
                order = Order.objects.get(pk=order_id)
            except Order.DoesNotExist:
                return Response({'status': 'Failure', 'error': 'Order not found against id'},
                                status=status.HTTP_417_EXPECTATION_FAILED)
            try:
                cancellation = DashboardCancelOrderMixin().perform_cancellation(candidate_id=candidate_id, email=email,
                                                                                order=order)
            except Exception as exc:
                logger.error('Dashboard cancellation error %s' % exc)
                return Response({'status': 'Failure', 'error': exc}, status=status.HTTP_417_EXPECTATION_FAILED)
            if cancellation:
                return Response({'status': 'Success', 'error': None, 'cancelled': True}, status=status.HTTP_200_OK)
            return Response({'status': 'Failure', 'error': None, 'cancelled': False},
                            status=status.HTTP_417_EXPECTATION_FAILED)
        return Response(serializer.errors, status=status.HTTP_200_OK)

