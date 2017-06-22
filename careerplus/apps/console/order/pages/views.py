from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from console.order.partials.views import NewOrdersListPartial, ClosedOrdersListPartial, HeldOrdersListPartial, NewOrdersDetailPartial, ClosedOrdersDetailPartial, HeldOrdersDetailPartial, NewOrdersUpdatableDetailPartial, ClosedOrdersUpdatableDetailPartial, HeldOrdersUpdatableDetailPartial
from order.models import Order, OrderItem
from order.api.core.serializers import OrderSerializer
from partner.api.core.permissions import IsEmployeeOfVendor

class NewOrdersListView(NewOrdersListPartial):

    template_name = 'console/order/pages/console-page.html'


class ClosedOrdersListView(ClosedOrdersListPartial):

    template_name = 'console/order/pages/console-page.html'


class HeldOrdersListView(HeldOrdersListPartial):

    template_name = 'console/order/pages/console-page.html'


class NewOrdersDetailView(NewOrdersDetailPartial):

    template_name = 'console/order/pages/console-page.html'


class ClosedOrdersDetailView(ClosedOrdersDetailPartial):

    template_name = 'console/order/pages/console-page.html'


class HeldOrdersDetailView(HeldOrdersDetailPartial):

    template_name = 'console/order/pages/console-page.html'


class NewOrdersUpdatableDetailView(NewOrdersUpdatableDetailPartial):

    template_name = 'console/order/pages/console-page.html'


class ClosedOrdersUpdatableDetailView(ClosedOrdersUpdatableDetailPartial):

    template_name = 'console/order/pages/console-page.html'


class HeldOrdersUpdatableDetailView(HeldOrdersUpdatableDetailPartial):

    template_name = 'console/order/pages/console-page.html'


class ChangeOrderStatusAPIMixin(APIView):
    permission_classes = (IsEmployeeOfVendor, )
    order_status = None
    def get_object(self, order_id=None, orderitem_id=None):
        try:
            if order_id:
                return Order.objects.get(pk=order_id)
            elif orderitem_id:
                return OrderItem.objects.get(pk=orderitem_id).order
            else:
                raise Http404
        except Order.DoesNotExist:
            raise Http404

    def put(self, request, order_id=None, orderitem_id=None, format=None):
        order = self.get_object(order_id=order_id, orderitem_id=orderitem_id)

        serializer = OrderSerializer(order, data={'status': self.order_status})
        if serializer.is_valid():
            serializer.save()
            return Response({'operation_reflected': True})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CloseOrderAPI(ChangeOrderStatusAPIMixin):
    permission_classes = (IsAdminUser, )
    order_status = 3

class HoldOrderAPI(ChangeOrderStatusAPIMixin):
    order_status = 2

class ArchiveOrderAPI(ChangeOrderStatusAPIMixin):
    order_status = 4

class UnholdOrderAPI(ChangeOrderStatusAPIMixin):
    order_status = 1
