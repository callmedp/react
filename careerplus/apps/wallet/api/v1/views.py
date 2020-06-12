from decimal import Decimal
from django.utils import timezone
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from cart.models import Cart
from cart.mixins import CartMixin
from shared.rest_addons.authentication import ShineUserAuthentication
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt


import logging
from wallet.models import (
    Wallet, RewardPoint, ECash,
    WalletTransaction, ECashTransaction, PointTransaction)
from cart.mixins import CartMixin
from rest_framework.authentication import SessionAuthentication, BasicAuthentication


class WalletRedeemView(APIView, CartMixin):
    permission_classes = ()
    authentication_classes = ()
    
    def post(self, request, *args, **qwargs):

        candidate_id = request.data.get('candidate_id')
        if not candidate_id:
            return Response(
                {'success': '',
                 'error_message': 'Candidate Id is required.'
                 },  status=status.HTTP_400_BAD_REQUEST)

        point = request.data.get('point', '')
        if not point:
            logging.getLogger('error_log').error(
                'Redeem point is required for candidate_id {}.'.format(candidate_id))
            return Response(
                {'success': '',
                 'error_message': 'Redeem point is required.'
                 },  status=status.HTTP_400_BAD_REQUEST)

        if not request.data.get('cart_pk'):
            return Response(
                {'success': '',
                 'error_message': 'Cart pk is required.'
                 },  status=status.HTTP_400_BAD_REQUEST)

            # self.getCartObject()
        cart_obj = None
        cart_pk = request.data.get('cart_pk', None)
        try:
            cart_obj = Cart.objects.select_related('coupon').get(pk=cart_pk)
        except Cart.DoesNotExist:
            logging.getLogger('error_log').error(
                'Something went wrong, Please login to continue for candidate_id {}.'.format(candidate_id))
            return Response(
                {'success': '',
                 'error_message': 'Something went wrong, Please login to continue.'
                 },  status=status.HTTP_400_BAD_REQUEST)
        if cart_obj.coupon:
            logging.getLogger('error_log').error(
                'Coupon already applied, You cannot redeem point now for candidate_id {}.'.format(candidate_id))
            return Response(
                {'success': '',
                 'error_message': 'Coupon already applied, You cannot redeem point now.'
                 },  status=status.HTTP_400_BAD_REQUEST)
        wal_txn = cart_obj.wallettxn.filter(
            txn_type=2).order_by('-created').select_related('wallet')
        if wal_txn:
            logging.getLogger('error_log').error(
                'Points already applied! for candidate_id {}.'.format(candidate_id))
            return Response(
                {'success': '',
                 'error_message': 'Points already applied!.'
                 },  status=status.HTTP_400_BAD_REQUEST)
        owner = cart_obj.owner_id
        owner_email = cart_obj.email
        if not owner:
            logging.getLogger('error_log').error(
                'Session Expired, Please login to continue for candidate_id {}.'.format(candidate_id))
            return Response(
                {'success': '',
                 'error_message': 'Session Expired, Please login to continue.'
                 },  status=status.HTTP_400_BAD_REQUEST)
        try:
            wal_obj = Wallet.objects.get(owner=owner)
        except Wallet.DoesNotExist:
            logging.getLogger('error_log').error(
                'Something went wrong, Try after some time for candidate_id {}.'.format(candidate_id))
            return Response(
                {'success': '',
                 'error_message': 'Something went wrong, Try after some time.'
                 },  status=status.HTTP_400_BAD_REQUEST)
        try:
            point = Decimal(point)
            if point <= Decimal(0):
                logging.getLogger('error_log').error(
                    'Redeem Point should be positive, Cannot Redeem! for candidate_id {}.'.format(candidate_id))
                return Response(
                    {'success': '',
                     'error_message': 'Redeem Point should be positive, Cannot Redeem!.'
                     },  status=status.HTTP_400_BAD_REQUEST)
            # line_item = cart_obj.lineitems.filter(parent=None)[0]
            # type_flow = int(line_item.product.type_flow)
            # if type_flow == 17:
            #     cart_dict = CartMixin.get_local_cart_items(self,cart_obj=cart_obj)
            # else:
            cart_dict = self.get_solr_cart_items(cart_obj=cart_obj)
            total_amount = cart_dict.get('total_amount')
            if point >= total_amount:
                point = total_amount
            points = wal_obj.point.filter(status=1).order_by('created')
            total = Decimal(0)
            for pts in points:
                if pts.expiry >= timezone.now():
                    total += pts.current
            wal_total = total
            if wal_total < point:
                logging.getLogger('error_log').error(
                    'You have less points in wallet, Cannot Redeem! for candidate_id {}.'.format(candidate_id))
                return Response(
                    {'success': '',
                     'error_message': 'You have less points in wallet, Cannot Redeem!.'
                     },  status=status.HTTP_400_BAD_REQUEST)
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
                            pts.save()
                            PointTransaction.objects.create(
                                transaction=wallettxn,
                                point=pts,
                                point_value=point,
                                txn_type=2)
                            point = Decimal(0)

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
                            pts.save()

            wallettxn.status = 1
            wallettxn.notes = 'Redeemed from cart'
            wallettxn.current_value = wal_obj.get_current_amount()
            wallettxn.save()
            return Response(
                {'success': True, 'msg': 'Successfully Redeemed'
                 }, status.HTTP_200_OK)
        except Exception as e:
            logging.getLogger('error_log').error(
                'unable to redeem the points %s' % str(e))
            return Response(
                {'success': '',
                 'error_message': 'Try after some Time'
                 },  status=status.HTTP_400_BAD_REQUEST)


class WalletRemoveView(APIView, CartMixin):
    permission_classes = ()
    authentication_classes = ()

    def post(self, request, format=None):
        try:
            if not request.data.get('cart_pk'):
                return Response(
                    {'success': 0,
                     'error_message': 'Cart pk is required.'
                     },  status=status.HTTP_400_BAD_REQUEST)
            cart_obj = None
            cart_pk = request.data.get('cart_pk', None)
            try:
                cart_obj = Cart.objects.get(pk=cart_pk)
            except Cart.DoesNotExist:
                return Response(
                    {'success': 0,
                     'error_message': 'Something went wrong, Please login to continue.'
                     },  status=status.HTTP_400_BAD_REQUEST)
            owner = cart_obj.owner_id
            if not owner:
                return Response(
                    {'success': 0,
                     'error_message': 'Session Expired, Please login to continue.'
                     },  status=status.HTTP_400_BAD_REQUEST)
            wal_txn = cart_obj.wallettxn.filter(
                txn_type=2).order_by('-created').select_related('wallet')
            if not wal_txn:
                return Response(
                    {'success': 0,
                     'error_message': 'No Redeemed Points found!.'
                     },  status=status.HTTP_400_BAD_REQUEST)
            wal_txn = wal_txn[0]
            points_used = wal_txn.usedpoint.all().order_by('point__pk')
            for pts in points_used:
                point = pts.point
                point.current += pts.point_value
                point.last_used = timezone.now()
                pts.txn_type = 5
                if point.expiry <= timezone.now():
                    point.status = 3
                else:
                    point.status = 1
                point.save()
                pts.save()
            wal_txn.txn_type = 5
            wal_txn.notes = 'Reverted From Cart'
            wal_txn.status = 1
            wal_txn.current_value = wal_txn.wallet.get_current_amount()
            wal_txn.save()
            return Response(
                {'success': True, 'msg': 'Successfully Removed'
                 }, status.HTTP_200_OK)

        except Exception as e:
            logging.getLogger('error_log').error(
                'unable to remove %s' % str(e))
            return Response(
                {'success': 0,
                 'error_message': 'Try after some Time'
                 },  status=status.HTTP_400_BAD_REQUEST)
