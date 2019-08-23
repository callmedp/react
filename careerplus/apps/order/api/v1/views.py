from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView,ListAPIView
from order.api.core.mixins import OrderItemViewMixin
from order.models import Order
from order.api.v1.serializers import OrderItemListSerializer
import json


class OrderItemViewSet(OrderItemViewMixin, ModelViewSet):
    """
        CRUD Viewset for `OrderItem` model.
    """


class OrderItemsListView(ListAPIView):
    serializer_class = OrderItemListSerializer
    authentication_classes = ()
    permission_classes = ()

    
    def get_queryset(self):
        order_id = self.kwargs.get('pk')
        order = Order.objects.filter(id=order_id).first()
        queryset = order.orderitems.filter(oi_status=2,no_process=False) if order else None
        return queryset
    
        



