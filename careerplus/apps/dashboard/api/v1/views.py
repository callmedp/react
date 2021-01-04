from dashboard.dashboard_mixin import DashboardInfo
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.views import APIView
from payment.models import PaymentTxn
from order.models import Order, OrderItem
from dashboard.api.v1.serializers import OrderSerializer,OrderItemSerializer
from haystack.query import SearchQuerySet

from django.conf import settings

class DashboardMyorderApi(DashboardInfo, APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def get(self, request, *args, **kwargs):
        candidate_id = self.request.session.get('candidate_id', None)
        data=[]
        if candidate_id:
        # candidate_id='5fed060d9cbeea482331ec4b'
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
                    "orderitems": OrderItemSerializer(orderitems).data,
                }
                order_list.append(data)
        return Response(order_list,status=status.HTTP_200_OK)

class MyCoursesApi(DashboardInfo, APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def get(self, request, *args, **kwargs):
        candidate_id = self.request.session.get('candidate_id', None)
        data = []
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

            courses = OrderItem.objects.filter(order__in=orders,product__type_flow=2).values_list('product',flat=True)
            tsrvcs = SearchQuerySet().filter(id__in=courses, pTP__in=[0, 1, 3]).exclude(
                id__in=settings.EXCLUDE_SEARCH_PRODUCTS
            )
            data = [
                    {'id': tsrvc.id, 'heading': tsrvc.pHd, 'name': tsrvc.pNm, 'url': tsrvc.pURL, 'img': tsrvc.pImg, \
                    'img_alt': tsrvc.pImA, 'rating': tsrvc.pARx, 'price': tsrvc.pPinb, 'vendor': tsrvc.pPvn, 'stars': tsrvc.pStar,
                    'provider': tsrvc.pPvn} for tsrvc in tsrvcs]
        return Response(data=data, status=status.HTTP_200_OK)

class MyServicesApi(DashboardInfo, APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def get(self, request, *args, **kwargs):
        candidate_id = self.request.session.get('candidate_id', None)
        data = []
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

            services = OrderItem.objects.filter(order__in=orders,product__product_class__slug__in=settings.SERVICE_SLUG).values_list('product',flat=True)
            tsrvcs = SearchQuerySet().filter(id__in=services, pTP__in=[0, 1, 3]).exclude(
                id__in=settings.EXCLUDE_SEARCH_PRODUCTS
            )
            data = [
                    {'id': tsrvc.id, 'heading': tsrvc.pHd, 'name': tsrvc.pNm, 'url': tsrvc.pURL, 'img': tsrvc.pImg, \
                    'img_alt': tsrvc.pImA, 'rating': tsrvc.pARx, 'price': tsrvc.pPinb, 'vendor': tsrvc.pPvn, 'stars': tsrvc.pStar,
                    'provider': tsrvc.pPvn} for tsrvc in tsrvcs]
        return Response(data=data, status=status.HTTP_200_OK)