import logging

from django.utils import timezone

from decimal import Decimal

from cart.models import ShippingDetail

from .models import Order, OrderItem


class OrderMixin(object):

	def createOrder(self, cart_obj, status):
		try:
			candidate_id = self.request.session.get('candidate_id')
			if candidate_id and cart_obj:
				if cart_obj.lineitems.all().exists():
					order = Order.objects.create(cart=cart_obj, candidate_id=candidate_id,
						status=status, date_placed=timezone.now())
					order.number = str(order.pk)
					try:
						shipping_obj = ShippingDetail.objects.filter(candidate_id=candidate_id)[0]
					except:
						shipping_obj = None

					if shipping_obj:
						order.email = shipping_obj.email
						order.first_name = shipping_obj.first_name
						order.last_name = shipping_obj.last_name
						order.country_code = shipping_obj.get_country_code()
						order.mobile = shipping_obj.mobile
						order.address = shipping_obj.address
						order.pincode = shipping_obj.pincode
						order.state = shipping_obj.state
						order.country = shipping_obj.get_country()
					order.save()
					cart_obj.date_frozen = timezone.now()
					cart_obj.status = 4
					cart_obj.save()
					self.createOrderitems(order, cart_obj)
				return order
		except Exception as e:
			logging.getLogger('error_log').error(str(e))

	def createOrderitems(self, order, cart_obj):
		try:
			if order and cart_obj:
				cart_items = cart_obj.lineitems.all().select_related('product')
				for item in cart_items:
					OrderItem.objects.create(order=order, product=item.product,
						title=item.product.title)
		except Exception as e:
			logging.getLogger('error_log').error(str(e))