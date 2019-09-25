# rest imports
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView,UpdateAPIView
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

#in app imports
from order.api.core.mixins import OrderItemViewMixin
from order.models import Order,LTVMonthlyRecord
from order.api.v1.serializers import OrderItemListSerializer
from shared.rest_addons.authentication import ShineUserAuthentication
from .serializers import OrderSerializer,LTVReportSerializer

# python imports
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



class OrderUpdateView(UpdateAPIView):
    authentication_classes = (ShineUserAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    lookup_field = "id"
    lookup_url_kwarg = "pk"

class LTVReportView(ListAPIView):
    serializer_class = LTVReportSerializer
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        queryset = LTVMonthlyRecord.objects.filter(
                        year=year,month=month)
        return queryset
    
        



