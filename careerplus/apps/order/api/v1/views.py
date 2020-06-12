# python imports

# django imports
import json

# local imports
from .serializers import OrderSerializer,LTVReportSerializer,OrderShineCandidateSerializer

#in app imports
from order.api.core.mixins import OrderItemViewMixin
from order.models import Order,MonthlyLTVRecord,OrderItemOperation,Message,OrderItem
from order.api.v1.serializers import OrderItemSerializer
from order.api.core.serializers import OrderItemOperationsSerializer,\
    MessageCommunincationSerializer
from core.api_mixin import ShineCandidateDetail
from emailers.utils import BadgingMixin

# 3rd party imports
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView,UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from shared.rest_addons.mixins import FieldFilterMixin,\
    ListSerializerContextMixin,ListSerializerDataMixin
from shared.rest_addons.permissions import OrderItemAccessPermission,IsObjectOwnerOrConsoleUser
from rest_framework.authentication import SessionAuthentication
from shared.rest_addons.pagination import LearningCustomPagination
from shared.permissions import IsObjectOwner
from shared.rest_addons.authentication import ShineUserAuthentication
from rest_framework import status
from rest_framework.views import APIView


class OrderItemViewSet(OrderItemViewMixin, ModelViewSet):
    """
        CRUD Viewset for `OrderItem` model.
    """


class OrderItemsListView(ListAPIView):
    serializer_class = OrderItemSerializer
    authentication_classes = ()
    permission_classes = ()

    def get_queryset(self):
        order_id = self.kwargs.get('pk')
        order = Order.objects.filter(id=order_id).first()
        queryset = order.orderitems.filter(
            oi_status=2, no_process=False) if order else None
        return queryset


class OrderUpdateView(UpdateAPIView):
    authentication_classes = (SessionAuthentication, ShineUserAuthentication)
    permission_classes = (IsAuthenticated, IsObjectOwnerOrConsoleUser)
    queryset = Order.objects.all()
    lookup_field = "id"
    lookup_url_kwarg = "pk"

    def patch(self, request, *args, **kwargs):
        body = json.loads(request.body)
        if body.get('check_primary'):
            order_id = self.kwargs.get('pk')
            order = Order.objects.filter(id=order_id).first()
            old_candidate_id = order.candidate_id
            details = ShineCandidateDetail().get_status_detail(body.get('alt_email'))
            badging_details = BadgingMixin().get_badging_data(
                candidate_id=order.candidate_id, feature=True)
            if badging_details:
                BadgingMixin().update_badging_data(candidate_id=old_candidate_id, data={})
                BadgingMixin().update_badging_data(
                    candidate_id=details.get('candidate_id'), data=badging_details)
            order.email = details.get('email')
            order.candidate_id = details.get('candidate_id')
            order.save(update_fields=['email', 'candidate_id'])
        return super(OrderUpdateView, self).patch(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.request._request.session.get('candidate_id'):
            return OrderShineCandidateSerializer
        return OrderSerializer


class OrderItemOperationApiView(FieldFilterMixin, ListAPIView):
    """
    To get the order item operations for particular order include
    &oi='OrderItemId'

    """
    authentication_classes = [SessionAuthentication]
    permission_classes = [OrderItemAccessPermission, ]
    serializer_class = OrderItemOperationsSerializer
    pagination_class = LearningCustomPagination

    def get_queryset(self):
        filter_dict = {}
        # query_params = self.request.query_params
        # oi_id = query_params.get('oi')
        oi_id = self.kwargs.get('oi_id')
        if oi_id:
            filter_dict.update({'oi__id': oi_id})
        return OrderItemOperation.objects.filter(**filter_dict).order_by('-modified')


class MessageCommunicationListApiView(FieldFilterMixin, ListAPIView):
    """
    To get the messages for particular order items include &oi='OrderItemId'
    """

    authentication_classes = [SessionAuthentication]
    permission_classes = (OrderItemAccessPermission,)
    serializer_class = MessageCommunincationSerializer
    pagination_class = LearningCustomPagination

    def get_queryset(self):
        filter_dict = {}
        # query_params = self.request.query_params
        oi_id = self.kwargs.get('oi_id')
        if oi_id:
            filter_dict.update({'oi__id': oi_id})
        return Message.objects.filter(**filter_dict).order_by('-created')

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


class OrderItemUpdateView(UpdateAPIView):
    authentication_classes = (ShineUserAuthentication,)
    permission_classes = (IsAuthenticated, IsObjectOwner,)
    serializer_class = OrderItemSerializer
    queryset = OrderItem.objects.all()
    lookup_field = "id"
    lookup_url_kwarg = "pk"
    owner_fields = ['order.candidate_id']


class OrderItemPatchView(APIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = None

    def patch(self, request, *args, **kwargs):
        candidate_id = request.data.get('candidate_id')
        order_item_id = request.data.get('order_item_id')
        oi_status = request.data.get('oi_status')
        missing_list = []
        if not candidate_id:
            missing_list.append('candidate_id')
        if not order_item_id:
            missing_list.append('order_item_id')
        if not oi_status:
            missing_list.append('oi_status')

        if len(missing_list):
            return Response({"error_message": ', '.join(missing_list)
                             + ' are missing.'if len(missing_list) > 1
                             else ', '.join(missing_list) + ' is missing.'},
                            status=status.HTTP_400_BAD_REQUEST)

        order_item = OrderItem.objects.filter(id=order_item_id).first()
        if not order_item:
            return Response({'error_message': 'No order item available with id {}'.format(order_item_id)},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            if order_item.order.candidate_id != candidate_id:
                return Response({'error_message': 'Unauthorised.'},
                                status=status.HTTP_401_UNAUTHORIZED)

            order_item.oi_status = oi_status

            order_item.save()
            return Response({'status': 1},
                            status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error_message': 'Something went wrong. {}'.format(e)},
                            status=status.HTTP_400_BAD_REQUEST)
