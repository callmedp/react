# python imports
import logging
from datetime import datetime, date
from decimal import Decimal

# django imports

# local imports
from cart.api.core.serializers import CartSerializer

# inter app imports
from users.mixins import UserMixin
from cart.mixins import CartMixin
from cart.models import Cart
from coupon.api.core.serializers import CouponSerializer
from wallet.models import Wallet
from wallet.api.core.serializers import (
    WalletSerializer, WalletTransactionSerializer)

# third party imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from cart.mixins import CartMixin


class PaymentSummaryView(CartMixin, UserMixin, APIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = None

    def get(self, request, *args, **kwargs):
        data = {}
        resume_shine_cart = request.GET.get('resume_shine', False)

        cart_obj = self.getCartObject()

        # TODO create api to save info in to the cart when some one logged in as guest or with credentials
        if not cart_obj:
            logging.getLogger('error_log').error(
                "Unable to create cart object.")
            return Response({'errror_message': 'Unable to create cart object'},
                            status=status.HTTP_400_BAD_REQUEST)
        wal_obj = None
        cart_coupon, cart_wallet, type_flow = None, None, None
        wal_txn, wal_total, wal_point = None, None, None
        cart_dict = self.get_solr_cart_items(cart_obj=cart_obj)
        cart_items = cart_dict.get('cart_items', [])
        data['cart_items'] = cart_items
        payment_dict = self.getPayableAmount(
            cart_obj, cart_dict.get('total_amount'))
        data['payment_dict'] = payment_dict

        if cart_obj and len(cart_items):
            wal_txn = cart_obj.wallettxn.filter(txn_type=2).order_by(
                '-created').select_related('wallet')
            cart_coupon = cart_obj.coupon
            if cart_coupon:
                wal_obj = None
            elif wal_txn.exists():
                wal_obj = None
                wal_txn = wal_txn[0]
                points = wal_txn.point_txn.all()
                points_active = points.filter(expiry__gte=timezone.now())
                points_used = wal_txn.usedpoint.all()

                if len(points_active) == len(points):
                    cart_wallet = wal_txn
                    wal_point = wal_txn.point_value
                else:
                    points_used = wal_txn.usedpoint.all().order_by('point__pk')
                    for pts in points_used:
                        point = pts.point
                        point.current += pts.point_value
                        point.last_used = timezone.now()
                        pts.txn_type = 5
                        if point.expiry <= timezone.now():
                            point.status = 3
                        else:
                            if point.current > Decimal(0):
                                point.status = 1
                            else:
                                point.status = 2
                        point.save()
                        pts.save()
                    wal_txn.txn_type = 5
                    wal_txn.notes = 'Auto Reverted From Cart'
                    wal_txn.status = 1
                    wal_txn.save()
                    wal_obj = wal_txn.wallet
                    wal_total = wal_obj.get_current_amount()
                    if wal_total <= Decimal(0):
                        wal_obj = None
            elif cart_obj.owner_id:
                wal_obj, created = Wallet.objects.get_or_create(
                    owner=cart_obj.owner_id)
                if cart_obj.owner_email:
                    wal_obj.owner_email = cart_obj.owner_email
                    wal_obj.save()
                wal_total = wal_obj.get_current_amount()
                if wal_total <= Decimal(0):
                    wal_obj = None

        data.update({
            'cart_coupon': CouponSerializer(cart_coupon).data,
            'cart_wallet': WalletTransactionSerializer(cart_wallet).data,
            'wallet': WalletSerializer(wal_obj).data, 'type_flow': type_flow,
            'cart': CartSerializer(cart_obj).data, 'wallet_total': wal_total, 'wallet_point': wal_point
        })

        return Response(data, status=status.HTTP_201_CREATED)
