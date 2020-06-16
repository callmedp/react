# python imports

# django imports
import json
from decimal import Decimal
from django.utils import timezone
import datetime
from datetime import timedelta
import time


# local imports
from .serializers import OrderSerializer, LTVReportSerializer, OrderShineCandidateSerializer

# in app imports
from order.api.core.mixins import OrderItemViewMixin
from order.models import Order, MonthlyLTVRecord, OrderItemOperation, Message, OrderItem
from order.api.v1.serializers import OrderItemSerializer
from order.api.core.serializers import OrderItemOperationsSerializer,\
    MessageCommunincationSerializer
from core.api_mixin import ShineCandidateDetail
from emailers.utils import BadgingMixin
from shop.models import (Product)
from order.mixins import OrderMixin
from cart.models import (Cart, LineItem)
from cart.mixins import CartMixin
from payment.mixin import PaymentMixin
from payment.models import PaymentTxn
from geolocation.models import Country
from wallet.models import (Wallet, WalletTransaction,
                           PointTransaction, ProductPoint)

# 3rd party imports
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from shared.rest_addons.mixins import FieldFilterMixin,\
    ListSerializerContextMixin, ListSerializerDataMixin
from shared.rest_addons.permissions import OrderItemAccessPermission, IsObjectOwnerOrConsoleUser
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


class DirectOrderCreateApiView(OrderMixin, CartMixin, PaymentMixin, APIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = ()

    def getNewCartObject(self):
        prod_id = self.request.data.get('prod_id', None)
        candidate_id = self.request.session.get('candidate_id', None)
        email = self.request.session.get('email', '')
        mobile = self.request.session.get('mobile_no', '')
        country_code = self.request.session.get('country_code', '91')
        first_name = self.request.session.get('first_name', '')

        product = Product.objects.filter(id=int(prod_id)).first()
        if not product:
            return Response({'errror_message': 'No Product with given id ' + prod_id}, status=status.HTTP_400_BAD_REQUEST)
        addons = self.request.data.get('addons', [])
        req_options = self.request.data.get('req_options', [])
        cv_id = self.request.data.get('cv_id')
        cart_obj = None
        session_id = self.request.session.session_key

        country_obj = Country.objects.filter(
            phone=country_code, active=True).first()

        cart_obj = Cart.objects.create(
            owner_id=candidate_id,
            session_id=session_id,
            status=2,
            site=0,
            email=email,
            owner_email=email,
            first_name=first_name,
            country_code=country_obj.phone,
            mobile=mobile,
        )

        utm_params = self.request.session.get('utm')
        try:
            if utm_params and isinstance(utm_params, dict):
                utm_params = json.dumps(utm_params)
                cart_obj.utm_params = utm_params
            cart_obj.save()
        except Exception as e:
            logging.getLogger('error_log').error(str(e))

        if (product.is_course or product.type_flow == 17) and cv_id:
            # courses
            try:
                cv_prod = Product.objects.get(id=cv_id, active=True)
                parent = cart_obj.lineitems.create(
                    product=product, no_process=True)
                parent.reference = str(
                    cart_obj.pk) + '_' + str(parent.pk)
                parent.price_excl_tax = product.get_price()
                parent.save()
                child = cart_obj.lineitems.create(
                    product=cv_prod, parent=parent)
                child.reference = str(
                    cart_obj.pk) + '_' + str(child.pk)
                child.price_excl_tax = cv_prod.get_price()
                child.parent_deleted = True
                child.save()

                # for addons
                child_products = product.related.filter(
                    secondaryproduct__active=True)
                addons = Product.objects.filter(id__in=addons)
                for child in addons:
                    if child in child_products:
                        li = LineItem.objects.create(
                            cart=cart_obj, parent=parent, product=child)
                        li.reference = str(
                            cart_obj.pk) + '_' + str(li.pk)
                        li.price_excl_tax = child.get_price()
                        li.save()
            except Exception as e:
                logging.getLogger('error_log').error(str(e))
        else:
            # standalone/Combo/coutry-specific
            parent = LineItem.objects.create(
                cart=cart_obj, product=product)
            parent.reference = str(cart_obj.pk) + '_' + str(parent.pk)
            parent.price_excl_tax = product.get_price()
            parent.save()
            child_products = product.related.filter(
                secondaryproduct__active=True)
            addons = Product.objects.filter(id__in=addons)
            for child in addons:
                if child in child_products:
                    li = LineItem.objects.create(
                        cart=cart_obj, parent=parent, product=child)
                    li.reference = str(cart_obj.pk) + '_' + str(li.pk)
                    li.price_excl_tax = child.get_price()
                    li.save()

            req_products = Product.objects.filter(id__in=req_options)
            if req_products.exists():
                parent.no_process = True
                parent.save()
                for prd in req_products:
                    li = LineItem.objects.create(
                        cart=cart_obj, parent=parent, product=prd)
                    li.reference = str(cart_obj.pk) + '_' + str(li.pk)
                    li.price_excl_tax = prd.get_price()
                    li.parent_deleted = True
                    li.save()

        return cart_obj

    def addWalletPoints(self, total_amount):

        owner = self.request.session.get('candidate_id', None)
        email = self.request.session.get('email', '')
        points = total_amount
        action = 'addpoints'

        wal_obj = None
        if owner:
            wal_obj = Wallet.objects.filter(owner=owner).first()

        if email and not wal_obj:
            wal_obj = Wallet.objects.filter(owner_email=email).count()
            if wal_obj != 1:
                wal_obj = None
            elif wal_obj == 1:
                wal_obj = Wallet.objects.filter(owner_email=email)[0]

        if not wal_obj:
            return False

        expiry = timezone.now() + datetime.timedelta(days=30)

        point_obj = wal_obj.point.create(
            original=points,
            current=points,
            expiry=expiry,
            status=1
        )

        wal_txn = wal_obj.wallettxn.create(
            txn_type=1,
            status=1,
            point_value=points
        )

        point_obj.wallettxn.create(
            transaction=wal_txn,
            point_value=points,
            txn_type=1
        )

        wal_txn.current_value = wal_obj.get_current_amount()

        try:
            wal_txn.save()
            return True
        except Exception as e:
            logging.getLogger('error_log').error(str(e))
            return False

    def redeemWalletPoints(self, cart_obj, total_amount):
        owner = cart_obj.owner_id
        owner_email = cart_obj.email
        try:
            wal_obj = Wallet.objects.get(owner=owner)
            point = Decimal(total_amount)
            points = wal_obj.point.filter(status=1).order_by('created')
            total = Decimal(0)
            for pts in points:
                if pts.expiry >= timezone.now():
                    total += pts.current
            wal_total = total
            wal_obj.owner_email = owner_email
            wal_obj.save()
            wallettxn = WalletTransaction.objects.create(
                wallet=wal_obj, cart=cart_obj, txn_type=2, point_value=point)
            for pts in points:
                if pts.expiry >= timezone.now():
                    if point > Decimal(0):
                        if pts.current >= point:
                            pts.current -= point
                            pts.last_used = timezone.now()
                            if pts.current == Decimal(0):
                                pts.status = 1
                            try:
                                pts.save()
                                PointTransaction.objects.create(
                                    transaction=wallettxn,
                                    point=pts,
                                    point_value=point,
                                    txn_type=2)
                                point = Decimal(0)
                            except Exception as e:
                                logging.getLogger('error_log').error(str(e))

                        else:
                            point -= pts.current
                            pts.last_used = timezone.now()
                            pts.status = 2
                            PointTransaction.objects.create(
                                transaction=wallettxn,
                                point=pts,
                                point_value=pts.current,
                                txn_type=2)
                            pts.current = Decimal(0)
                            try:
                                pts.save()
                            except Exception as e:
                                logging.getLogger('error_log').error(str(e))

            wallettxn.status = 1
            wallettxn.notes = 'Redeemed from cart'
            wallettxn.current_value = wal_obj.get_current_amount()
            try:
                wallettxn.save()
            except Exception as e:
                logging.getLogger('error_log').error(str(e))
        except Exception as e:
            logging.getLogger('error_log').error(str(e))

    def post(self, request, *args, **kwargs):
        # before order, get cart object
        # paas the cart object to order and create order
        # change the status of order by making payemnt. Payment method should be redeem option.
        data = {"status": -1}
        cart_obj = self.getNewCartObject()
        cart_items = self.get_solr_cart_items(cart_obj)
        total_amount = cart_items.get('total_amount', Decimal(0))
        redeem_opt = request.data.get('redeem_option', 'practice_test')
        wallet_status = self.addWalletPoints(total_amount)

        if wallet_status:
            self.redeemWalletPoints(cart_obj, total_amount)
            order = self.createOrder(cart_obj)
            self.closeCartObject(cart_obj)
            if order:
                txn = 'CP%d%s' % (order.pk, int(time.time()))
                pay_txn = PaymentTxn.objects.create(
                    txn=txn,
                    order=order,
                    cart=cart_obj,
                    status=0,
                    payment_mode=15,
                    currency=order.currency,
                    txn_amount=order.total_incl_tax,
                )
                payment_type = "REDEEMED"
                return_parameter = self.process_payment_method(
                    payment_type, request, pay_txn)

                candidate_id = request.session.get('candidate_id', '')
                if candidate_id:
                    product_point = ProductPoint.objects.filter(
                        candidate_id=candidate_id).first()

                    if product_point:
                        ref_order = Order.objects.filter(id=product_point.order_id).first()
                        order.ref_order = ref_order
                        try:
                            order.save()
                        except Exception as e:
                            logging.getLogger(
                                'error_log').error(str(e))

                        updated_options = []
                        for redeem_option in eval(product_point.redeem_options):
                            if redeem_option['type'] == redeem_opt and redeem_option['product_redeem_count'] > 0:
                                redeem_option['product_redeem_count'] = redeem_option['product_redeem_count'] - 1
                            updated_options.append(redeem_option)

                        product_point.redeem_options = str(updated_options)
                        try:
                            product_point.save()
                        except Exception as e:
                            logging.getLogger(
                                'error_log').error(str(e))

                return Response({'status': 1, 'redirectUrl': '/dashboard'},
                                status=status.HTTP_200_OK)
            else:
                return Response({'error_message': "Could not able  to create Order!"},
                                status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({'error_message': "Could not able  to use wallet Points!"},
                            status=status.HTTP_400_BAD_REQUEST)
