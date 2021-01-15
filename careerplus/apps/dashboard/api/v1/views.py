# DRF Import
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.views import APIView

# Django Core Import
from django.conf import settings
from django.core.cache import cache

# Inter-App Import
from dashboard.dashboard_mixin import DashboardInfo
from payment.models import PaymentTxn
from order.models import Order, OrderItem,OrderItemOperation
from dashboard.api.v1.serializers import OrderSerializer,OrderItemSerializer
from wallet.models import Wallet
from core.common import APIResponse

# Other Import
from haystack.query import SearchQuerySet
from order.choices import OI_OPS_STATUS


class DashboardMyorderApi(DashboardInfo, APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def get(self, request, *args, **kwargs):
        candidate_id = self.request.session.get('candidate_id', None)
        order_list=[]
        # candidate_id='5fed060d9cbeea482331ec4b'
        if candidate_id:        
            if cache.get('dashboard_my_orders'):
                order_list = cache.get('dashboard_my_orders')
            else:
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
                for obj in orders:
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
                    cache.set('dashboard_my_orders',order_list,86400)
        return Response(order_list,status=status.HTTP_200_OK)

class MyCoursesApi(DashboardInfo, APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def get(self, request, *args, **kwargs):
        candidate_id = self.request.session.get('candidate_id', None)
        data = []
        if candidate_id:
            if cache.get('dashboard_my_courses'):
                data = cache.get('dashboard_my_courses')
            else:
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

                courses = OrderItem.objects.filter(order__in=orders,product__type_flow=2).values_list('product',flat=True)
                tsrvcs = SearchQuerySet().filter(id__in=courses, pTP__in=[0, 1, 3]).exclude(
                    id__in=settings.EXCLUDE_SEARCH_PRODUCTS
                )
                data = [
                        {'id': tsrvc.id, 'heading': tsrvc.pHd, 'name': tsrvc.pNm, 'url': tsrvc.pURL, 'img': tsrvc.pImg, \
                        'img_alt': tsrvc.pImA, 'rating': tsrvc.pARx, 'price': tsrvc.pPinb, 'vendor': tsrvc.pPvn, 'stars': tsrvc.pStar,
                        'provider': tsrvc.pPvn} for tsrvc in tsrvcs]
                cache.set('dashboard_my_courses',data,86400)
        return Response(data=data, status=status.HTTP_200_OK)


class MyServicesApi(DashboardInfo, APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def get(self, request, *args, **kwargs):
        candidate_id = self.request.session.get('candidate_id', None)
        data = []
        candidate_id='5fed060d9cbeea482331ec4b'
        if candidate_id:
            # if cache.get('dashboard_my_services'):
            #     data = cache.get('dashboard_my_services')
            # else:
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
            # tsrvcs = SearchQuerySet().filter(id__in=services, pTP__in=[0, 1, 3]).exclude(
            #     id__in=settings.EXCLUDE_SEARCH_PRODUCTS
            # )
            data = []
            for service in services:
                tsrvc = SearchQuerySet().filter(id=service.id, pTP__in=[0, 1, 3]).exclude(
                id__in=settings.EXCLUDE_SEARCH_PRODUCTS
                )[0]
                x = {'id': tsrvc.id, 'heading': tsrvc.pHd, 'name': tsrvc.pNm, 'url': tsrvc.pURL, 'img': tsrvc.pImg, \
                    'img_alt': tsrvc.pImA, 'rating': tsrvc.pARx, 'price': tsrvc.pPinb, 'vendor': tsrvc.pPvn, 'stars': tsrvc.pStar,
                    'provider': tsrvc.pPvn,'duration':service.product.get_duration_in_day(),'status':OI_OPS_STATUS[service.oi_status][1]}
                data.append(x)
            #  cache.set('dashboard_my_services',data,86400)
        return Response(data=data, status=status.HTTP_200_OK)


class DashboardMyWalletAPI(DashboardInfo, APIView):
    
    permission_classes = (permissions.AllowAny, )
    authentication_classes = ()

    def get(self, request):
        """
        API to return the shine loyality points specifically
        """
        candidate_id = '568a0b20cce9fb485393489b'
        # candidate_id = self.request.session.get('candidate_id')
        if candidate_id is None:
            return APIResponse(message='Candidate Details required', status=status.HTTP_400_BAD_REQUEST)

        wal_obj, created = Wallet.objects.get_or_create(owner=candidate_id)
        wal_total = wal_obj.get_current_amount()
        wal_txns = wal_obj.wallettxn.filter(txn_type__in=[1, 2, 3, 4, 5], point_value__gt=0).order_by('-created')
        wal_txns = wal_txns.select_related('order', 'cart')

        print(wal_txns)



