from decimal import Decimal
from django.utils import timezone
from datetime import datetime
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from cart.models import Cart
from shop.models import Product
from coupon.models import Coupon, CouponUser
from cart.mixins import CartMixin
import logging
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import (IsAuthenticated, IsAdminUser, )
from oauth2_provider.contrib.rest_framework import OAuth2Authentication


class CouponRedeemView(APIView, CartMixin):
	authentication_classes = ()
	permission_classes = ()
	serializer_class = None

	def post(self, request, *args, **kwargs):
		code = request.data.get('code', None)
		candidate_id = request.data.get('candidate_id', None)
		cart_pk = request.data.get('cart_pk', None)

		missing_list = []

		if code is None or not code:
			missing_list.append('code')
		if candidate_id is None or not candidate_id:
			missing_list.append('candidate_id')
		if cart_pk is None or not cart_pk:
			missing_list.append('cart_pk')

		if len(missing_list):
			return Response({"error_message": ', '.join(
				missing_list) + ' are missing.' if len(
				missing_list) > 1 else ', '.join(missing_list) + ' is missing.',
			                 'success': ''},
			                status=status.HTTP_400_BAD_REQUEST)

		coupon = Coupon.objects.filter(code=code).first()

		if not coupon:
			logging.getLogger('error_log').error(
				'Not valid code id {}'.format(code))
			return Response({'success': '', 'error_message': 'Not valid '
			                                                 'code.'},
			                status=status.HTTP_400_BAD_REQUEST)

		if coupon.is_redeemed:
			return Response(
				{'success': '', 'error_message': 'Coupon already redeemed!.'},
				status=status.HTTP_400_BAD_REQUEST)
		#  TODO commenting it for future use case.
		# if not request.session.get('cart_pk'):
		#     self.getCartObject()
		cart_obj = None

		cart_obj = Cart.objects.select_related('coupon').filter(
			pk=cart_pk).first()
		if not cart_obj:
			logging.getLogger('error_log').error(
				'Something went wrong, Please login to continue for candidate '
				'id {}'.format(candidate_id))
			return Response(
				{'success': '', 'error_message': 'Something went wrong, '
				                                 'Please '
				                                 'login to continue.'},
				status=status.HTTP_400_BAD_REQUEST)
		wal_txn = cart_obj.wallettxn.filter(txn_type=2).order_by(
			'-created').select_related('wallet')
		if wal_txn:
			logging.getLogger('error_log').error(
				'Points already applied! for candidate id {}'.format(
					candidate_id))
			return Response(
				{'success': '', 'error_message': 'Points already applied!.'},
				status=status.HTTP_400_BAD_REQUEST)

		user_email = cart_obj.email
		old_coupon = cart_obj.coupon

		if old_coupon:
			logging.getLogger('error_log').error(
				'Another coupon is already applied for candidate id {}'.format(
					candidate_id))
			return Response(
				{'success': '', 'error_message': 'Another coupon is already '
				                                 'applied.'},
				status=status.HTTP_400_BAD_REQUEST)
		if not user_email:
			logging.getLogger('error_log').error(
				'Session Expired, Please login to continue for candidate id {'
				'}'.format(candidate_id))
			return Response({'success': '',
			                 'error_message': 'Session Expired, Please login '
			                                  'to continue.'},
			                status=status.HTTP_400_BAD_REQUEST)

		if coupon.expired():
			logging.getLogger('error_log').error(
				'This code is expired for candidate id {}'.format(
					candidate_id))
			return Response(
				{'success': '', 'error_message': 'Coupon has been expired.'},
				status=status.HTTP_400_BAD_REQUEST)

		if coupon.suspended():
			logging.getLogger('error_log').error(
				'This code is suspended for candidate id {}'.format(
					candidate_id))
			return Response(
				{'success': '', 'error_mesage': 'This code is suspended.'},
				status=status.HTTP_400_BAD_REQUEST)

		if not coupon.active:
			logging.getLogger('error_log').error(
				'This code is Inactive for candidate id {}'.format(
					candidate_id))
			return Response(
				{'success': '', 'error_message': 'This code is Inactive.'},
				status=status.HTTP_400_BAD_REQUEST)

		if coupon.site not in [0, 1, 3]:
			logging.getLogger('error_log').error(
				'This code is not valid for candidate id {}'.format(
					candidate_id))
			return Response({'success': '', 'error': 'This code is not '
			                                         'valid.'},
			                status=status.HTTP_400_BAD_REQUEST)

		if not coupon.is_valid_coupon(site=coupon.site, source=None,
		                              cart_obj=cart_obj):
			if coupon.coupon_scope == 2:
				error = 'This code is valid on particular sources.'
			else:
				error = 'This code is valid on particular products.'
			logging.getLogger('error_log').error(str(error))
			return Response({'success': '', 'error_message': error},
			                status=status.HTTP_400_BAD_REQUEST)

		try:
			user_coupon = coupon.users.get(user=user_email)
			if user_coupon.redeemed_at is not None:
				logging.getLogger('error_log').error(
					'This code has already been used by your account for '
					'candidate id {}'.format(candidate_id))
				return Response({'success': '',
				                 'error_message': 'This code has already been '
				                                  'used by your account.'},
				                status=status.HTTP_400_BAD_REQUEST)
		except CouponUser.DoesNotExist:
			if coupon.user_limit is not 0:  # zero means no limit of user count
				# only user bound coupons left and you don't have one
				if coupon.user_limit is coupon.users.filter(
						user__isnull=False).count():
					logging.getLogger('error_log').error(
						'This code is not valid for your account for candidate'
						' id {}'.format(candidate_id))
					return Response({'success': '',
					                 'error_message': 'This code is not valid '
					                                  'for your account.'},
					                status=status.HTTP_400_BAD_REQUEST)
				# all coupons redeemed
				if coupon.user_limit is coupon.users.filter(
						redeemed_at__isnull=False).count():
					logging.getLogger('error_log').error(
						'This code has already been used for candidate id {'
						'}'.format(candidate_id))
					return Response({'success': '',
					                 'error_message': 'This code has already '
					                                  'been used.'},
					                status=status.HTTP_400_BAD_REQUEST)
		try:
			total = Decimal(0)
			lis = cart_obj.lineitems.all().select_related('product')
			for li in lis:
				total += li.product.get_price()
			if coupon.min_purchase:
				if total < coupon.min_purchase:
					logging.getLogger('error_log').error(
						'This cart total is below minimum purchase for '
						'candidate id {}'.format(candidate_id))
					return Response(
						{'success': '', 'error_message': 'This cart total is '
						                                 'below minimum '
						                                 'purchase.'},
						status=status.HTTP_400_BAD_REQUEST)
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

			return Response({'success': True, 'msg': 'Successfully Redeemed'},
			                status=status.HTTP_200_OK)

		except Exception as e:
			logging.getLogger('error_log').error(str(e))
			return Response(
				{'success': '', 'error_message': 'Try after some Time'},
				status=status.HTTP_400_BAD_REQUEST)


class CouponRemoveView(APIView, CartMixin):
	permission_classes = ()
	authentication_classes = ()

	def post(self, request, *args, **kwargs):
		try:
			#  TODO handle if needed
			# if not request.GET.get('cart_pk'):
			#     self.getCartObject()
			cart_obj = None
			cart_pk = request.POST.get('cart_pk')
			if not cart_pk:
				cart_pk = request.data.get('cart_pk')
			try:
				cart_obj = Cart.objects.select_related('coupon').get(
					pk=cart_pk)
			except Cart.DoesNotExist:
				return Response(
					{'success': 0, 'error_message': 'Something went wrong, '
					                                'Please login to '
					                                'continue.'},
					status=status.HTTP_400_BAD_REQUEST)
			user_email = cart_obj.email
			coupon = cart_obj.coupon

			if not coupon:
				return Response({'success': 0, 'error_message': 'No coupon is '
				                                                'associated.'},
				                status=status.HTTP_400_BAD_REQUEST)
			if not user_email:
				return Response(
					{'success': 0, 'error_message': 'Session Expired, Please '
					                                'login to continue.'},
					status=status.HTTP_400_BAD_REQUEST)

			try:
				user_coupon = coupon.users.get(user=user_email)
				user_coupon.redeemed_at = None
				user_coupon.save()
				cart_obj.coupon = None
				cart_obj.save()
				return Response(
					{'success': True, 'msg': 'Successfully Removed'},
					status=status.HTTP_200_OK)
			except CouponUser.DoesNotExist:
				cart_obj.coupon = None
				cart_obj.save()
				return Response(
					{'success': True, 'msg': 'Successfully Removed'},
					status=status.HTTP_200_OK)

		except Exception as e:
			logging.getLogger('error_log').error(str(e))
			return Response({'success': 0, 'error': 'Try after some Time'},
			                status=status.HTTP_400_BAD_REQUEST)


class ProductCouponDetail(APIView):
	authentication_classes = [OAuth2Authentication]
	permission_classes = [IsAuthenticated, IsAdminUser]

	@csrf_exempt
	def get(self, request, *args, **kwargs):
		prod_id = request.GET.get('pid')
		prod = None
		if not prod_id:
			return Response({'error': 'No Product id found'},
			                status=status.HTTP_400_BAD_REQUEST)
		try:
			prod = Product.objects.get(id=prod_id)
		except Exception as e:
			logging.getLogger('error_log').error("No product found ")
			return Response({'error': 'No Product id found', },
			                status=status.HTTP_400_BAD_REQUEST)
		coupons = prod.couponproducts.filter(active=True,
		                                     valid_until__gte=datetime.now())
		if not coupons:
			return Response({'error': 'No active coupon found', },
			                status=status.HTTP_400_BAD_REQUEST)

		if coupons.count() > 1:
			return Response({'error': 'Multiple Coupon found', },
			                status=status.HTTP_400_BAD_REQUEST)
		coupons = coupons[0]
		data = {'code': coupons.code,
		        'coupon_type': coupons.get_coupon_type_display(),
		        'min_purchase': coupons.min_purchase,
		        'product_price_before_coupon': prod.inr_price,}
		if coupons.coupon_type == 'flat':
			data.update({'product_price_after_coupon': (
					prod.inr_price - coupons.value) if prod.inr_price >
					coupons.value else 0,'coupon_value':coupons.value
					})
			return Response(data,status=status.HTTP_200_OK)
		else:
			discount = (prod.inr_price * coupons.value) / 100
			data.update({'product_price_after_coupon': (prod.inr_price -
			discount) if prod.inr_price > discount else 0,
			'coupon_value': coupons.value})

			return Response(data,status=status.HTTP_200_OK)

