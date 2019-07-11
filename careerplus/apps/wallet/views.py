from decimal import Decimal
from django.utils import timezone
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from cart.models import Cart
from cart.mixins import CartMixin
import logging
from .models import (
    Wallet, RewardPoint, ECash,
    WalletTransaction, ECashTransaction, PointTransaction)
from cart.mixins import CartMixin
from rest_framework.authentication import SessionAuthentication, BasicAuthentication 

class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


class WalletRedeemView(APIView, CartMixin):
    permission_classes = (AllowAny,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request, format=None):
        point = request.data.get('point')
        if not point:
            return Response(
                {'success': 0,
                 'error': 'Redeem point is required.'
                 }, status=400, content_type='application/json')
        
        if not request.session.get('cart_pk'):
            self.getCartObject()
        cart_obj = None
        cart_pk = request.session.get('cart_pk')
        try:
            cart_obj = Cart.objects.select_related('coupon').get(pk=cart_pk)
        except Cart.DoesNotExist:
            return Response(
                {'success': 0,
                 'error': 'Something went wrong, Please login to continue.'
                 }, status=400, content_type='application/json')
        if cart_obj.coupon:
            return Response(
                {'success': 0,
                 'error': 'Coupon already applied, You cannot redeem point now.'
                 }, status=400, content_type='application/json')
        wal_txn = cart_obj.wallettxn.filter(
            txn_type=2).order_by('-created').select_related('wallet')
        if wal_txn:
            return Response(
                {'success': 0,
                 'error': 'Points already applied!.'
                 }, status=400, content_type='application/json')
        owner = cart_obj.owner_id
        owner_email = cart_obj.email
        if not owner:
            return Response(
                {'success': 0,
                 'error': 'Session Expired, Please login to continue.'
                 }, status=400, content_type='application/json')
        try:
            wal_obj = Wallet.objects.get(owner=owner)
        except Wallet.DoesNotExist:
            return Response(
                {'success': 0,
                 'error': 'Something went wrong, Try after some time.'
                 }, status=400, content_type='application/json')
        try:
            point = Decimal(point)
            if point <= Decimal(0):
                return Response(
                    {'success': 0,
                     'error': 'Redeem Point should be positive, Cannot Redeem!.'
                     }, status=400, content_type='application/json')
            line_item = cart_obj.lineitems.filter(parent=None)[0]
            type_flow = int(line_item.product.type_flow)
            if type_flow == 17:
                cart_dict = CartMixin.get_local_cart_items(self,cart_obj=cart_obj)
            else:
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
                return Response(
                    {'success': 0,
                     'error': 'You have less points in wallet, Cannot Redeem!.'
                     }, status=400, content_type='application/json')
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
                {'success': True,'msg': 'Successfully Redeemed'
                 }, status=200, content_type='application/json')
        except Exception as e:
            logging.getLogger('error_log').error('unable to redeem the points %s' % str(e))
            return Response(
                {'success': 0,
                 'error': 'Try after some Time'
                 }, status=400, content_type='application/json')    
 


class WalletRemoveView(APIView, CartMixin):
    permission_classes = (AllowAny,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request, format=None):
        try:
            if not request.session.get('cart_pk'):
                self.getCartObject()
            cart_obj = None
            cart_pk = request.session.get('cart_pk')
            try:
                cart_obj = Cart.objects.get(pk=cart_pk)
            except Cart.DoesNotExist:
                return Response(
                    {'success': 0,
                     'error': 'Something went wrong, Please login to continue.'
                     }, status=400, content_type='application/json')
            owner = cart_obj.owner_id
            if not owner:
                return Response(
                    {'success': 0,
                     'error': 'Session Expired, Please login to continue.'
                     }, status=400, content_type='application/json')
            wal_txn = cart_obj.wallettxn.filter(
                txn_type=2).order_by('-created').select_related('wallet')
            if not wal_txn:
                return Response(
                    {'success': 0,
                     'error': 'No Redeemed Points found!.'
                     }, status=400, content_type='application/json')
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
                {'success': True,'msg': 'Successfully Removed'
                 }, status=200, content_type='application/json')
        
               
        except Exception as e:
            logging.getLogger('error_log').error('unable to remove %s' % str(e))
            return Response(
            {'success': 0,
             'error': 'Try after some Time'
             }, status=400, content_type='application/json')
