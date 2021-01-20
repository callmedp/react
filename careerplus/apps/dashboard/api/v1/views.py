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
from dashboard.api.v1.serializers import OrderSerializer,OrderItemSerializer
from wallet.models import Wallet
from core.common import APIResponse
from search.helpers import get_recommendations

# Other Import
from haystack.query import SearchQuerySet
from order.choices import OI_OPS_STATUS
from .helpers import offset_paginator


class DashboardMyorderApi(DashboardInfo, APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def get(self, request, *args, **kwargs):
        candidate_id = self.request.session.get('candidate_id', None)
        order_list=[]
        # candidate_id='568a0b20cce9fb485393489b'
        # candidate_id='5c94a7b29cbeea2c1f27fda2'
        page = request.GET.get("page", 1)

        if candidate_id:         
            orders = Order.objects.filter(
            status__in=[0, 1, 3],
            candidate_id=candidate_id)
            excl_txns = PaymentTxn.objects.filter(
                status__in=[0, 2, 3, 4, 5],
                payment_mode__in=[6, 7],
                order__candidate_id=candidate_id)
            # excl_txns = PaymentTxn.objects.filter(status=0, ).exclude(payment_mode__in=[1, 4])
            excl_order_list = excl_txns.all().values_list('order_id', flat=True)
            orders = orders.exclude(
                id__in=excl_order_list).order_by('-date_placed')
            order_list = []
            paginated_data = offset_paginator(page, orders)
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
                order_list.append({'page':
                {'current_page':paginated_data['current_page'],
                'total':paginated_data['total_pages'],
                'has_prev': True if paginated_data['current_page'] >1 else False,
                'has_next':True if (paginated_data['total_pages']-paginated_data['current_page'])>0 else False
                }})
                
        return APIResponse(data=order_list, message='Order data Success', status=status.HTTP_200_OK)

class MyCoursesApi(DashboardInfo, APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def get(self, request, *args, **kwargs):
        candidate_id = self.request.session.get('candidate_id', None)
        data = []
        page = request.GET.get("page", 1)
        # candidate_id='568a0b20cce9fb485393489b'
        # candidate_id='5fed060d9cbeea482331ec4b'
        if candidate_id:
            orders = Order.objects.filter(
                status__in=[0, 1, 3],
                candidate_id=candidate_id)
                
            excl_txns = PaymentTxn.objects.filter(
                status__in=[0, 2, 3, 4, 5],
                payment_mode__in=[6, 7],
                order__candidate_id=candidate_id)
            excl_order_list = excl_txns.all().values_list('order_id', flat=True)

            orders = orders.exclude(
                id__in=excl_order_list).order_by('-date_placed')

            courses = OrderItem.objects.filter(order__in=orders,product__type_flow=2)
            paginated_data = offset_paginator(page, courses)
            data = OrderItemSerializer(paginated_data["data"],many=True,context= {"get_details": True}).data
            #pagination info
            data.append({'page':
            {'current_page':paginated_data['current_page'],
            'total':paginated_data['total_pages'],
            'has_prev': True if paginated_data['current_page'] >1 else False,
            'has_next':True if (paginated_data['total_pages']-paginated_data['current_page'])>0 else False
            }})
        return APIResponse(data=data,message='Courses data Success',status=status.HTTP_200_OK)


class MyServicesApi(DashboardInfo, APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def get(self, request, *args, **kwargs):
        candidate_id = self.request.session.get('candidate_id', None)
        email = request.GET.get('email', None)
        data = []
        page = request.GET.get("page", 1)
        # candidate_id='568a0b20cce9fb485393489b'
        # candidate_id='5fed060d9cbeea482331ec4b'
        if candidate_id:
            orders = Order.objects.filter(
                status__in=[0, 1, 3],
                candidate_id=candidate_id)

            excl_txns = PaymentTxn.objects.filter(
                status__in=[0, 2, 3, 4, 5],
                payment_mode__in=[6, 7],
                order__candidate_id=candidate_id)
            excl_order_list = excl_txns.all().values_list('order_id', flat=True)

            orders = orders.exclude(
                id__in=excl_order_list).order_by('-date_placed')
            

            services = OrderItem.objects.filter(order__in=orders,product__product_class__slug__in=settings.SERVICE_SLUG)
            paginated_data = offset_paginator(page, services)
            pending_resume_items = DashboardInfo().get_pending_resume_items(candidate_id=candidate_id,
                                                                        email=email)

            pending_resume_items = [{'id': oi.id, 'product_name': oi.product.get_name if oi.product else ''
                                    , 'product_get_exp_db': oi.product.get_exp_db() if oi.product else ''
                                    } for oi in
                                pending_resume_items]
            data = OrderItemSerializer(paginated_data["data"],many=True,context= {"get_details": True}).data
            data.append({'pending_resume_items':pending_resume_items})

            #pagination info
            data.append({'page':
            {'current_page':paginated_data['current_page'],
            'total':paginated_data['total_pages'],
            'has_prev': True if paginated_data['current_page'] >1 else False,
            'has_next':True if (paginated_data['total_pages']-paginated_data['current_page'])>0 else False
            }})
        return APIResponse(data=data,message='Services data Success', status=status.HTTP_200_OK)


class DashboardMyWalletAPI(DashboardInfo, APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def get(self, request):
        """
        API to return the shine loyality points or called as Wallet
        """
        page = request.GET.get('page', 1)
        data = {}

        # attempting to get candidate from session
        candidate_id = self.request.session.get('candidate_id')
        candidate_id = '568a0b20cce9fb485393489b'
        if candidate_id is None:
            return APIResponse(data=data, message='Candidate Details required', status=status.HTTP_400_BAD_REQUEST)

        # wallet object according to candidate
        wal_obj, created = Wallet.objects.get_or_create(owner=candidate_id)
        data['wal_total'] = wal_obj.get_current_amount()

        # filter the wallet according to txns
        wal_txns = wal_obj.wallettxn.filter(point_value__gt=0). \
            select_related('order', 'cart').order_by('-created')

        # pagination for large queryset
        try:
            page_obj = Paginator(wal_txns, 10)
            wal_txns_page_obj = page_obj.page(page)
        except PageNotAnInteger:
            wal_txns_page_obj = page_obj.page(1)
        except EmptyPage:
            wal_txns_page_obj = page_obj.page(1)
        data['page'] = [{'total_page': page_obj.num_pages, 'current_page': wal_txns_page_obj.number,
                         'has_next': wal_txns_page_obj.has_next(),
                         'has_prev': wal_txns_page_obj.has_previous()}]

        # -------------------------------------------------------------------------------------------------------------#
        data['loyality_txns'] = [{'date': obj.created.strftime('%b. %d, %Y'), 'description': obj.get_txn_type(),
                                  'order_id': None if obj.order is None else obj.order.number,
                                  'loyality_points': obj.point_value,
                                  'expiry_date': obj.added_point_expiry().strftime(
                                      '%b. %d, %Y') if obj.txn_type == 1 or obj.txn_type == 5 else '',
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
