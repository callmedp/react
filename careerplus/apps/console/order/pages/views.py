#python imports

#django imports
from django.http import Http404
from django.views.generic import TemplateView

#local imports

#inter app imports
from order.models import Order, OrderItem
from order.api.core.serializers import OrderItemSerializer
from partner.api.core.permissions import IsEmployeeOfVendor
from console.order.partials.views import NewOrdersListPartial, \
ClosedOrdersListPartial, HeldOrdersListPartial, NewOrdersDetailPartial, \
ClosedOrdersDetailPartial, HeldOrdersDetailPartial, NewOrdersUpdatableDetailPartial, \
ClosedOrdersUpdatableDetailPartial, HeldOrdersUpdatableDetailPartial

#third party imports
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser


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


class ChangeOrderItemStatusAPIMixin(APIView):
    permission_classes = (IsEmployeeOfVendor, )
    order_status = None
    def get_object(self, orderitem_id=None):
        try:
            if orderitem_id:
                return OrderItem.objects.get(pk=orderitem_id)
            else:
                raise Http404
        except OrderItem.DoesNotExist:
            raise Http404

    def put(self, request, orderitem_id=None, format=None):
        orderitem = self.get_object(orderitem_id=orderitem_id)

        serializer = OrderItemSerializer(orderitem, data={'oi_status': self.order_status if self.order_status >=0 else orderitem.last_oi_status, 'last_oi_status': orderitem.oi_status}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'operation_reflected': True})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CloseOrderAPI(ChangeOrderItemStatusAPIMixin):
    permission_classes = (IsAdminUser, )
    order_status = 9

class HoldOrderAPI(ChangeOrderItemStatusAPIMixin):
    order_status = 10

class ArchiveOrderAPI(ChangeOrderItemStatusAPIMixin):
    order_status = 11

class UnholdOrderAPI(ChangeOrderItemStatusAPIMixin):
    order_status = -1



