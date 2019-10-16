# rest imports
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView,UpdateAPIView
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

#in app imports
from order.api.core.mixins import OrderItemViewMixin
from order.models import Order,MonthlyLTVRecord
from order.api.v1.serializers import OrderItemListSerializer
from shared.rest_addons.authentication import ShineUserAuthentication
from .serializers import OrderSerializer,LTVReportSerializer

# python imports
import json
from order.api.core.serializers import OrderItemOperationsSerializer,\
    MessageCommunincationSerializer
from order.models import OrderItemOperation,Message
from shared.rest_addons.mixins import FieldFilterMixin,\
    ListSerializerContextMixin,ListSerializerDataMixin
from shared.rest_addons.permissions import OrderAccessPermission
from rest_framework.authentication import SessionAuthentication
from shared.rest_addons.pagination import LearningCustomPagination


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


class OrderItemOperationApiView(FieldFilterMixin,ListAPIView):
    """
    To get the order item operations for particular order include
    &oi='OrderItemId'

    """
    authentication_classes = [SessionAuthentication]
    permission_classes = [OrderAccessPermission,]
    serializer_class = OrderItemOperationsSerializer
    pagination_class = LearningCustomPagination

    def get_queryset(self):
        filter_dict = {}
        query_params = self.request.query_params
        oi_id = query_params.get('oi')
        if oi_id:
            filter_dict.update({'oi__id':oi_id})
        return OrderItemOperation.objects.filter(**filter_dict)


class MessageCommunicationListApiView(FieldFilterMixin,ListAPIView):
    """
    To get the messages for particular order items include &oi='OrderItemId'
    """

    authentication_classes = []
    permission_classes = ()
    serializer_class = MessageCommunincationSerializer
    pagination_class = LearningCustomPagination

    def get_queryset(self):
        filter_dict = {}
        query_params = self.request.query_params
        oi_id = query_params.get('oi')
        if oi_id:
            filter_dict.update({'oi__id': oi_id})
        return Message.objects.filter(**filter_dict)

    #
    # def paginate_queryset(self, queryset):
    #     if 'nopage' in self.request.query_params:
    #         return None
    #     else:
    #         return super(MessageCommunicationListApiView,
    #                      self).paginate_queryset(queryset)


class LTVReportView(ListAPIView):
	serializer_class = LTVReportSerializer
	authentication_classes = (SessionAuthentication,)
	permission_classes = (IsAuthenticated,)

	def get_queryset(self):
		year = self.kwargs.get('year')
		month = self.kwargs.get('month')
		queryset = MonthlyLTVRecord.objects.filter(
			year=year, month=month)
		return queryset



