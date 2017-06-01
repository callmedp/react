import logging

from django.utils import timezone

from decimal import Decimal

from cart.models import ShippingDetail
from cart.mixins import CartMixin
from shop.views import ProductInformationMixin

from .models import Order, OrderItem


class OrderMixin(CartMixin, ProductInformationMixin):

	def createOrder(self, cart_obj, status):
		try:
			candidate_id = self.request.session.get('candidate_id')
			if candidate_id and cart_obj:
				if cart_obj.lineitems.all().exists():
					cart_obj.date_frozen = timezone.now()
					cart_obj.status = 4
					cart_obj.save()
					order = Order.objects.create(cart=cart_obj, candidate_id=candidate_id,
						status=status, date_placed=timezone.now())
					order.number = 'CP' + str(order.pk)
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
					order.total_excl_tax = self.getTotalAmount()
					order.save()
					self.createOrderitems(order, cart_obj)
				return order
		except Exception as e:
			logging.getLogger('error_log').error(str(e))

	def createOrderitems(self, order, cart_obj):
		# import ipdb; ipdb.set_trace()
		try:
			if order and cart_obj:
				cart_items = self.get_cart_items()
				for item in cart_items:
					parent_li = item.get('li')

					if parent_li and parent_li.product.type_product == 3:
						p_oi = OrderItem.objects.create(
							order=order,
							product=parent_li.product,
							title=parent_li.product.name,
							partner=parent_li.product.vendor,
							is_combo=True,
							no_process=True,
						)
						p_oi.upc = str(order.pk) + "_" + str(p_oi.pk)
						p_oi.oi_price_before_discounts_excl_tax = parent_li.price_excl_tax
						p_oi.save()

						combos = self.get_combos(parent_li.product).get('combos')

						for product in combos:
							oi = OrderItem.objects.create(
								order=order,
								product=product,
								title=product.pv_name,
								partner=product.vendor
							)
							oi.upc = str(order.pk) + "_" + str(oi.pk)
							oi.parent = p_oi
							oi.is_combo = True
							oi.oi_price_before_discounts_excl_tax = product.get_price()
							oi.save()

						addons = item.get('addons')
						for addon in addons:
							oi = OrderItem.objects.create(
								order=order,
								product=addon.product,
								title=addon.product.name,
								partner=addon.product.vendor
								)
							oi.upc = str(order.pk) + "_" + str(oi.pk)
							oi.parent = p_oi
							oi.oi_price_before_discounts_excl_tax = addon.price_excl_tax
							oi.save()

					elif parent_li:
						p_oi = OrderItem.objects.create(
							order=order,
							product=parent_li.product,
							title=parent_li.product.name,
							partner=parent_li.product.vendor,
							no_process=parent_li.no_process,
						)
						p_oi.upc = str(order.pk) + "_" + str(p_oi.pk)
						p_oi.oi_price_before_discounts_excl_tax = parent_li.price_excl_tax
						p_oi.save()

						addons = item.get('addons')
						for addon in addons:
							oi = OrderItem.objects.create(
								order=order,
								product=addon.product,
								title=addon.product.name,
								partner=addon.product.vendor
								)
							oi.upc = str(order.pk) + "_" + str(oi.pk)
							oi.parent = p_oi
							oi.oi_price_before_discounts_excl_tax = addon.price_excl_tax
							oi.save()

						variations = item.get('variations')
						for var in variations:
							oi = OrderItem.objects.create(
								order=order,
								product=var.product,
								title=var.product.name,
								partner=var.product.vendor
								)
							oi.upc = str(order.pk) + "_" + str(oi.pk)
							oi.parent = p_oi
							oi.oi_price_before_discounts_excl_tax = var.price_excl_tax
							oi.is_variation = True
							oi.save()
				self.request.session.update({
	                "order_pk": order.pk,
	            })
		except Exception as e:
			logging.getLogger('error_log').error(str(e))