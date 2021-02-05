# DRF Import
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.views import APIView

# Django Core Import
from django.conf import settings
from django.core.cache import cache
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Inter-App Import
from dashboard.dashboard_mixin import DashboardInfo
from payment.models import PaymentTxn
from order.models import Order, OrderItem,OrderItemOperation
from dashboard.api.v1.serializers import OrderSerializer,OrderItemSerializer,ReviewSerializer
from wallet.models import Wallet
from core.common import APIResponse
from search.helpers import get_recommendations
from shop.models import Product

# Other Import
from haystack.query import SearchQuerySet
from order.choices import OI_OPS_STATUS
from .helpers import offset_paginator, get_history
from django.contrib.contenttypes.models import ContentType
from review.models import Review
from emailers.email import SendMail
import logging
logger = logging.getLogger('error_log')
from datetime import datetime
from dateutil.relativedelta import relativedelta
from emailers.tasks import send_email_task

class DashboardMyorderApi(DashboardInfo, APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def get(self, request, *args, **kwargs):
        data = []
        page = request.GET.get("page", 1)
        candidate_id = self.request.session.get('candidate_id', None)
        order_list = []
        page_info={}
        if candidate_id:         
            orders = Order.objects.filter(
            status__in=[0, 1, 3],
            candidate_id=candidate_id)
            
            paginated_data = offset_paginator(page, orders,size=7)
            for obj in paginated_data["data"]:
                orderitems = OrderItem.objects.select_related(
                    'product').filter(no_process=False, order=obj)
                product_type_flow = None
                product_id = None
                item_count = len(orderitems)
                if item_count > 0:
                    item_order = orderitems[0]
                    product_type_flow = item_order and item_order.product_id and item_order.product.type_flow or 0
                    product_id = item_order and item_order.product_id
                data = {
                    "order": OrderSerializer(obj).data,
                    "item_count": item_count,
                    'product_type_flow': product_type_flow,
                    "product_id": product_id,
                    "orderitems": OrderItemSerializer(orderitems,many=True).data,
                }
                order_list.append(data)
                #pagination info
                page_info ={
                'current_page':paginated_data['current_page'],
                'total':paginated_data['total_pages'],
                'has_prev': True if paginated_data['current_page'] >1 else False,
                'has_next':True if (paginated_data['total_pages']-paginated_data['current_page'])>0 else False
                }
                
        return APIResponse(data={'data':order_list,'page':page_info}, message='Order data Success', status=status.HTTP_200_OK)

class MyCoursesApi(DashboardInfo, APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def get(self, request, *args, **kwargs):
        data = []
        page = request.GET.get("page", 1)
        candidate_id = self.request.session.get('candidate_id', None)
        last_month_from = request.GET.get("last_month_from",'all' )
        select_type = request.GET.get('select_type','all')
        page_info = {}

        #time filter
        if not last_month_from=='all':
            from_datetime = datetime.utcnow() - relativedelta(months=int(last_month_from))
            modified_from_datetime = from_datetime.replace(day=1, hour=0, minute=0, second=0, microsecond=0) 

        # candidate_id='601b8120ca3f418906a889a8'
        page_info={}
        if candidate_id:
            courses_oi = OrderItem.objects.filter(product__type_flow=2,no_process=False,order__candidate_id=candidate_id,order__status__in=[1, 3])
            courses = courses_oi.prefetch_related('product','order', 'product__attributes')
            if not last_month_from=='all':
                courses = courses.filter(order__date_placed__gte=modified_from_datetime)
            if select_type == 'in_process':
                courses = courses.exclude(oi_status=4)
            elif select_type == 'closed':
                courses = courses.filter(oi_status=4)
            paginated_data = offset_paginator(page, courses,size=7)
            data = OrderItemSerializer(paginated_data["data"],many=True,context= {"get_details": True, "candidate_id":candidate_id}).data
            #pagination info
            page_info ={
            'current_page':paginated_data['current_page'],
            'total':paginated_data['total_pages'],
            'has_prev': True if paginated_data['current_page'] >1 else False,
            'has_next':True if (paginated_data['total_pages']-paginated_data['current_page'])>0 else False
            }
        return APIResponse(data={'data':data,'page':page_info},message='Courses data Success',status=status.HTTP_200_OK)

class MyServicesApi(DashboardInfo, APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def get(self, request, *args, **kwargs):
        data = []
        page = request.GET.get("page", 1)
        candidate_id = self.request.session.get('candidate_id', None)
        last_month_from = request.GET.get("last_month_from",'all' )
        select_type = request.GET.get('select_type','all')
        page_info = {}

        #time filter
        # print(last_month_from)
        if not last_month_from=='all':
            from_datetime = datetime.utcnow() - relativedelta(months=int(last_month_from))
            modified_from_datetime = from_datetime.replace(day=1, hour=0, minute=0, second=0, microsecond=0) 

        if candidate_id:
            excl_txns = PaymentTxn.objects.filter(
                status__in=[0, 2, 3, 4, 5,6],
                payment_mode__in=[6, 7],
                order__candidate_id=candidate_id)
            excl_order_list = excl_txns.all().values_list('order_id', flat=True)
            services = OrderItem.objects.filter(order__candidate_id=candidate_id, no_process=False,order__status__in=[1, 3],product__product_class__slug__in=['writing','service','other']).exclude(order__in=excl_order_list)
            if not last_month_from=='all':
                services = services.filter(order__date_placed__gte=modified_from_datetime)
            if select_type == 'in_process':
                services = services.exclude(oi_status=4)
            elif select_type == 'closed':
                services = services.filter(oi_status=4)
            paginated_data = offset_paginator(page, services,size=7)
            data = OrderItemSerializer(paginated_data["data"],many=True,context= {"get_details": True, "candidate_id":candidate_id}).data
            #pagination info
            page_info ={
            'current_page':paginated_data['current_page'],
            'total':paginated_data['total_pages'],
            'has_prev': True if paginated_data['current_page'] >1 else False,
            'has_next':True if (paginated_data['total_pages']-paginated_data['current_page'])>0 else False
            }
        return APIResponse(data={'data':data,'page':page_info},message='Services data Success', status=status.HTTP_200_OK)

class DashboardMyWalletAPI(DashboardInfo, APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def get(self, request):
        """
        API to return the shine loyality points or called as Wallet
        """
        page = request.GET.get('page', 1)
        data = {}
        reward_type = ['Added', 'Refund', 'Reverted']

        # attempting to get candidate from session
        candidate_id = self.request.session.get('candidate_id')
        # candidate_id='5c94a7b29cbeea2c1f27fda2'

        if candidate_id is None:
            return APIResponse(data=data, message='Candidate Details required', status=status.HTTP_400_BAD_REQUEST)

        # wallet object according to candidate
        wal_obj, created = Wallet.objects.get_or_create(owner=candidate_id)
        data['wal_total'] = wal_obj.get_current_amount()

        # filter the wallet according to txns
        wal_txns = wal_obj.wallettxn.filter(point_value__gt=0). \
            select_related('order', 'cart').order_by('-created')

        # pagination for large queryset
        page_obj = Paginator(wal_txns, 10)
        try:
            page_obj = Paginator(wal_txns, 10)
            wal_txns_page_obj = page_obj.page(page)
        except PageNotAnInteger:
            wal_txns_page_obj = page_obj.page(1)
        except EmptyPage:
            wal_txns_page_obj = page_obj.page(1)
        data['page'] = {'total': page_obj.num_pages, 'current_page': wal_txns_page_obj.number,
                         'has_next': wal_txns_page_obj.has_next(),
                         'has_prev': wal_txns_page_obj.has_previous()}

        # -------------------------------------------------------------------------------------------------------------#
        data['loyality_txns'] = [{'date': obj.created.strftime('%b. %d, %Y'), 'description': obj.get_txn_type(),
                                  'order_id': None if obj.order is None else obj.order.number,
                                  'loyality_points': obj.point_value,
                                  'expiry_date': obj.added_point_expiry().strftime(
                                       '%b. %d, %Y') if obj.txn_type == 1 or obj.txn_type == 5 else '', 'get_txn_type': obj.get_txn_type(), 'txn_sign': '+' if obj.get_txn_type() in reward_type else '-',

                                    #   '%b. %d, %Y') if obj.txn_type == 1 or obj.txn_type == 5 else '',
                                  'balance': obj.current_value} for obj in wal_txns_page_obj.object_list]
        # -------------------------------------------------------------------------------------------------------------#
        rcourses = get_recommendations(
            self.request.session.get('func_area', None),
            self.request.session.get('skills', None)
        )
        # if and only if rcourse_skill is in session
        if rcourses:
            rcourses = rcourses[:6]
            data['recommended_products'] = rcourses

        return APIResponse(data=data, message='Loyality Points Success', status=status.HTTP_200_OK)

class DashboardReviewApi(APIView):
    permission_classes = ()
    authentication_classes = ()
    serializer_classes = None

    def get(self,request):
        # page = request.GET.get('page', 1)
        product_id = request.GET.get('product_id',None)
        data=[]
        candidate_id = self.request.session.get('candidate_id', None)
        if candidate_id is None:
            return APIResponse(data=data, message='Candidate Details required', status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return APIResponse(error='Product not found', status=status.HTTP_404_NOT_FOUND)
        product_type = ContentType.objects.get(
            app_label='shop', model='product')
        prd_list = []
        if product.type_product in [0, 2, 4, 5]:
            prd_list = [product.pk]
        elif product.type_product == 1:
            prd_id = product.variation.filter(
                siblingproduct__active=True,
                active=True).values_list('id', flat=True)
            prd_list = list(prd_id)
            prd_list.append(product.pk)
        elif product.type_product == 3:
            prd_id = product.childs.filter(
                childrenproduct__active=True,
                active=True).values_list('id', flat=True)
            prd_list = list(prd_id)
            prd_list.append(product.pk)
        review_list = Review.objects.filter(
            content_type__id=product_type.id,
            object_id__in=prd_list, status=1,user_id=candidate_id)

        review_list.update({'no_review':len(review_list)})
        # paginated_data = offset_paginator(page, review_list)
        data = ReviewSerializer(review_list, many=True).data
        # page_info ={
        # 'current_page':paginated_data['current_page'],
        # 'total':paginated_data['total_pages'],
        # 'has_prev': True if paginated_data['current_page'] >1 else False,
        # 'has_next':True if (paginated_data['total_pages']-paginated_data['current_page'])>0 else False
        # }
        return APIResponse(data={'data':data},message='Review data Success',status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        email_dict = {}
        candidate_id = request.data.get('candidate_id', None) or self.request.session.get('candidate_id', None)
        # candidate_id='568a0b20cce9fb485393489b'

        oi_pk = request.data.get('oi_pk')
        email = request.data.get('email') or self.request.session.get('email', None)
        data = {
            "display_message": 'Thank you for sharing your valuable feedback',
        }
        if oi_pk and candidate_id:
            try:
                oi = OrderItem.objects.select_related("order").get(id=oi_pk)
                review = request.data.get('review', '').strip()
                rating = int(request.data.get('rating', 1))
                title = request.data.get('title', '').strip()
                name = request.data.get('full_name') or self.request.session.get('name', email)
                error_msg = ''
                if not name:
                    error_msg + 'name missing,'
                if not oi:
                    error_msg + 'order_item missing ,'
                if not (oi.order.candidate_id == candidate_id):
                    error_msg + 'order_item candidate id and candidate id not matched,'
                if not (oi.order.status in [1, 3]):
                    error_msg + "order item's order status not matched"
                if rating and oi and oi.order.candidate_id == candidate_id and oi.order.status in [1, 3]:
                    content_type = ContentType.objects.get(app_label="shop", model="product")
                    review_obj = Review.objects.create(
                        content_type=content_type,
                        object_id=oi.product_id,
                        user_name=name,
                        user_email=email,
                        user_id=candidate_id,
                        content=review,
                        average_rating=rating,
                        title=title
                    )

                    extra_content_obj = ContentType.objects.get(app_label="order", model="OrderItem")

                    review_obj.extra_content_type = extra_content_obj
                    review_obj.extra_object_id = oi.id
                    review_obj.save()

                    oi.user_feedback = True
                    oi.save()
                    # send mail for coupon
                    if oi.user_feedback:
                        mail_type = "FEEDBACK_COUPON"
                        to_emails = [oi.order.get_email()]
                        email_dict.update({
                            "username": oi.order.first_name if oi.order.first_name else oi.order.candidate_id,
                            "subject": 'You earned a discount coupon worth Rs. <500>',
                            "coupon_code": '',
                            'valid': '',
                        })

                        try:
                            SendMail().send(to_emails, mail_type, email_dict)
                        except Exception as e:
                            logging.getLogger('error_log').error(
                                "%s - %s - %s" % (str(to_emails), str(e), str(mail_type)))

                else:
                    if not error_msg:
                        data['display_message'] = "select valid input for feedback"
                    data['display_message'] = error_msg
                    return Response(data, status=status.HTTP_400_BAD_REQUEST)


            except Exception as e:
                logging.getLogger('error_log').error(str(e))
                data['display_message'] = str(e)
                return Response(data, status=status.HTTP_400_BAD_REQUEST)

            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Something went Wrong'}, status=status.HTTP_400_BAD_REQUEST)

class DashboardPendingResumeItemsApi(APIView):
    permission_classes = ()
    authentication_classes = ()
    serializer_classes = None

    def get(self,request):
        candidate_id = self.request.session.get('candidate_id', None)
        email = request.GET.get('email', None)
        pending_resume_items = []
        # candidate_id='5c6661f7a9da9b3891e72729'

        try:
            pending_resume_items = DashboardInfo().get_pending_resume_items(candidate_id=candidate_id,
                                                                            email=email)

            pending_resume_items = [{'id': oi.id, 'product_name': oi.product.get_name if oi.product else ''
                                        , 'product_get_exp_db': oi.product.get_exp_db() if oi.product else ''
                                        } for oi in
                                    pending_resume_items]
        except Exception as e:
            logging.getLogger('error_log').error(str(e))
            pending_resume_items = []
            return APIResponse(data={'data': pending_resume_items},
                               message="We can't retrieve pending resumes at moment.", error=True,
                               status=status.HTTP_400_BAD_REQUEST)

        return APIResponse(data={'data':pending_resume_items},message='Pending resume items data Success', status=status.HTTP_200_OK)


class ViewOrderDetailsApi(APIView):
    permission_classes = ()
    authentication_classes = ()
    serializer_classes = None

    def get(self,request):
        candidate_id = self.request.session.get('candidate_id', None)
        oi_id = request.GET.get('oi_id',None)
        if candidate_id is None:
            return APIResponse(data='', error='Candidate Details required', status=status.HTTP_400_BAD_REQUEST)
        if oi_id is None:
            return APIResponse(data='', error='Order Item required', status=status.HTTP_400_BAD_REQUEST)

        try:
            oi= OrderItem.objects.get(id=oi_id)
        except OrderItem.DoesNotExist:
            return APIResponse(data='',error='Order item not found', status=status.HTTP_404_NOT_FOUND)
        datalist = get_history(oi)
        return APIResponse(data=datalist,message='Details data loaded', status=status.HTTP_200_OK)