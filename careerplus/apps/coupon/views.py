from decimal import Decimal
from django.utils import timezone
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from cart.models import Cart
from .models import Coupon, CouponUser
from cart.mixins import CartMixin
from rest_framework.authentication import SessionAuthentication, BasicAuthentication 


class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


class CouponRedeemView(APIView, CartMixin):
    permission_classes = (AllowAny,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request, format=None):
        code = request.data.get('code')
        try:
            coupon = Coupon.objects.get(code=code)
        except Coupon.DoesNotExist:
            return Response(
                {'success': 0,
                 'error': 'This code is not valid.'
                 }, status=400, content_type='application/json')

        if coupon.is_redeemed:
            return Response(
                {'success': 0,
                 'error': 'This code has already been used.'
                 }, status=400, content_type='application/json')
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
        wal_txn = cart_obj.wallettxn.filter(
            txn_type=2).order_by('-created').select_related('wallet')
        if wal_txn:
            return Response(
                {'success': 0,
                 'error': 'Points already applied!.'
                 }, status=400, content_type='application/json')
        
        user_email = cart_obj.email
        old_coupon = cart_obj.coupon

        if old_coupon:
            return Response(
                {'success': 0,
                 'error': 'Another coupon is already applied.'
                 }, status=400, content_type='application/json')
        if not user_email:
            return Response(
                {'success': 0,
                 'error': 'Session Expired, Please login to continue.'
                 }, status=400, content_type='application/json')
        
        if coupon.expired():
            return Response(
            {'success': 0,
             'error': 'This code is expired.'
             }, status=400, content_type='application/json')
        
        if coupon.suspended():
            return Response(
            {'success': 0,
             'error': 'This code is suspended.'
             }, status=400, content_type='application/json')

        if coupon.site not in [0, 1]:
            return Response(
                {'success': 0,
                 'error': 'This code is not valid.'
                 }, status=400, content_type='application/json')

        if not coupon.is_valid_coupon(site=1, source=None, cart_obj=cart_obj):
            if coupon.coupon_scope == 2:
                error = 'This code is valid on particular sources.'
            else:
                error = 'This code is valid on particular products.'

            return Response(
                {'success': 0,
                 'error': error
                }, status=400, content_type='application/json')

        try:
            user_coupon = coupon.users.get(user=user_email)
            if user_coupon.redeemed_at is not None:
                return Response(
                {'success': 0,
                 'error': 'This code has already been used by your account.'
                 }, status=400)
        except CouponUser.DoesNotExist:
            if coupon.user_limit is not 0:  # zero means no limit of user count
                # only user bound coupons left and you don't have one
                if coupon.user_limit is coupon.users.filter(user__isnull=False).count():
                    return Response(
                    {'success': 0,
                     'error': 'This code is not valid for your account.'
                     }, status=400)
                if coupon.user_limit is coupon.users.filter(redeemed_at__isnull=False).count():  # all coupons redeemed
                    return Response(
                    {'success': 0,
                     'error': 'This code has already been used.'
                     }, status=400)
        try:
            total = Decimal(0)
            lis = cart_obj.lineitems.all().select_related('product')
            for li in lis:
                total += li.product.get_price()
            if coupon.min_purchase:
                if total < coupon.min_purchase:
                    return Response(
                        {'success': 0,
                         'error': 'This cart total is below minimum purchase.'
                         }, status=400, content_type='application/json')
            try:
                coupon_user = coupon.users.get(user=user_email)
            except CouponUser.DoesNotExist:
                try:  # silently fix unbouned or nulled coupon users
                    coupon_user = coupon.users.get(user__isnull=True)
                    coupon_user.user = user_email
                except CouponUser.DoesNotExist:
                    coupon_user = CouponUser(coupon=coupon, user=user_email)
            cart_obj.coupon = coupon
            cart_obj.save()
            coupon_user.redeemed_at = timezone.now()
            coupon_user.save()
            
            return Response(
                {'success': True, 'msg': 'Successfully Redeemed'
                 }, status=200, content_type='application/json')
           
        except:
            return Response(
            {'success': 1,
             'error': 'Try after some Time'
             }, status=400, content_type='application/json')
        

class CouponRemoveView(APIView, CartMixin):
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
            user_email = cart_obj.email
            coupon = cart_obj.coupon

            if not coupon:
                return Response(
                    {'success': 0,
                     'error': 'No coupon is associated.'
                     }, status=400, content_type='application/json')
            if not user_email:
                return Response(
                    {'success': 0,
                     'error': 'Session Expired, Please login to continue.'
                     }, status=400, content_type='application/json')
            
            try:  
                user_coupon = coupon.users.get(user=user_email)
                user_coupon.redeemed_at = None
                user_coupon.save()
                cart_obj.coupon = None
                cart_obj.save()
                return Response(
                    {'success': True,'msg': 'Successfully Removed'
                    }, status=200, content_type='application/json')
            except CouponUser.DoesNotExist:
                cart_obj.coupon = None
                cart_obj.save()
                return Response(
                    {'success': True,'msg': 'Successfully Removed'
                    }, status=200, content_type='application/json')
   
        except:
            return Response(
            {'success': 0,
             'error': 'Try after some Time'
             }, status=400, content_type='application/json')
        
