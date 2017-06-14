import logging

from django.utils import timezone
from django.conf import settings

from decimal import Decimal

from shop.models import Product

from .models import Cart, LineItem


class CartMixin(object):
	def mergeCart(self, fromcart, tocart):

		try:
			from_parent_lines = fromcart.lineitems.filter(parent=None).select_related('product')
			to_parent_pks = tocart.lineitems.filter(parent=None).values_list('product__pk', flat=True)

			for main_p in from_parent_lines:
				if main_p.product.pk in to_parent_pks:
					parent_product = tocart.lineitems.get(product=main_p.product)
					to_child_pks = tocart.lineitems.filter(parent=parent_product).values_list('product__pk', flat=True)
					from_child_lines = fromcart.lineitems.filter(parent=main_p).select_related('product')

					for child in from_child_lines:
						if child.product.pk not in to_child_pks:
							li = tocart.lineitems.create(product=child.product)
							li.reference = str(tocart.pk) + '_' + str(li.pk)
							li.price_excl_tax = child.product.get_price()
							li.save()

				else:
					parent_product = tocart.lineitems.create(product=main_p.product)
					parent_product.reference = str(tocart.pk) + '_' + str(parent_product.pk)
					parent_product.price_excl_tax = main_p.product.get_price()
					parent_product.save()
					from_child_lines = fromcart.lineitems.filter(parent=main_p).select_related('product')

					for child in from_child_lines:
						li = tocart.lineitems.create(parent=parent_product, product=child.product)
						li.reference = str(tocart.pk) + '_' + str(li.pk)
						li.price_excl_tax = child.product.get_price()
						li.save()
				main_p.delete()

			fromcart.status = 1
			fromcart.date_merged = timezone.now()
			fromcart.save()
		except Exception as e:
			logging.getLogger('error_log').error(str(e))

	def updateCart(self, product, addons, cv_id, add_type, req_options):
		flag = -1
		try:
			flag = 1
			candidate_id = self.request.session.get('candidate_id')
			if add_type == "cart":
				self.getCartObject()
				cart_pk = self.request.session.get('cart_pk')
				session_id = self.request.session.session_key
				
				if cart_pk:
					cart_obj = Cart.objects.get(pk=cart_pk)
				elif candidate_id:
					cart_obj = Cart.objects.create(owner_id=candidate_id, session_id=session_id, status=2)
				elif session_id:
					cart_obj = Cart.objects.create(session_id=session_id, status=0)
			elif add_type == "express":
				if not self.request.session.session_key:
					self.request.session.create()
				session_id = self.request.session.session_key
				if candidate_id:
					cart_obj = Cart.objects.create(owner_id=candidate_id, session_id=session_id, status=3)
				elif session_id:
					cart_obj = Cart.objects.create(session_id=session_id, status=3)

			if cart_obj:
				cart_obj.lineitems.filter(product=product).delete()

				if product.type_service == 3 and cv_id:
					# courses
					try:
						cv_prod = Product.objects.get(id=cv_id, active=True)
						parent = cart_obj.lineitems.create(product=product, no_process=True)
						parent.reference = str(cart_obj.pk) + '_' + str(parent.pk)
						parent.price_excl_tax = product.get_price()
						parent.save()
						child = cart_obj.lineitems.create(product=cv_prod, parent=parent)
						child.reference = str(cart_obj.pk) + '_' + str(child.pk)
						child.price_excl_tax = cv_prod.get_price()
						child.parent_deleted = True
						child.save()

						# for addons
						child_products = product.related.filter(
				            secondaryproduct__active=True,
				            secondaryproduct__type_relation=1)
						addons = Product.objects.filter(id__in=addons, active=True)
						for child in addons:
							if child in child_products:
								li = LineItem.objects.create(cart=cart_obj, parent=parent, product=child)
								li.reference = str(cart_obj.pk) + '_' + str(li.pk)
								li.price_excl_tax = child.get_price()
								li.save()
					except Exception as e:
						logging.getLogger('error_log').error(str(e))
				else:
					# standalone/Combo/coutry-specific
					parent = LineItem.objects.create(cart=cart_obj, product=product)
					parent.reference = str(cart_obj.pk) + '_' + str(parent.pk)
					parent.price_excl_tax = product.get_price()
					parent.save()
					child_products = product.related.filter(
			            secondaryproduct__active=True,
			            secondaryproduct__type_relation=1)
					addons = Product.objects.filter(id__in=addons, active=True)
					for child in addons:
						if child in child_products:
							li = LineItem.objects.create(cart=cart_obj, parent=parent, product=child)
							li.reference = str(cart_obj.pk) + '_' + str(li.pk)
							li.price_excl_tax = child.get_price()
							li.save()

					req_products = Product.objects.filter(id__in=req_options, active=True)
					if req_products.exists():
						parent.no_process = True
						parent.save()
						for prd in req_products:
							li = LineItem.objects.create(cart=cart_obj, parent=parent, product=prd)
							li.reference = str(cart_obj.pk) + '_' + str(li.pk)
							li.price_excl_tax = prd.get_price()
							li.parent_deleted = True
							li.save()

				self.request.session.update({
					"cart_pk": cart_obj.pk,
					"checkout_type": add_type,
				})

			return flag

		except Exception as e:
			logging.getLogger('error_log').error(str(e))
		return flag

	def getCartObject(self):
		try:
			cart_obj = None
			request = self.request
			candidate_id = request.session.get('candidate_id')
			if not request.session.session_key:
				request.session.create()
			sessionid = request.session.session_key

			cart_users = Cart.objects.filter(owner_id=candidate_id, status=2)
			cart_sessions = Cart.objects.filter(session_id=sessionid, status=0)
			cart_user, cart_session = None, None
			if cart_users:
				for cart in cart_users:
					if cart_user:
						self.mergeCart(cart, cart_user)
					else:
						cart_user = cart
				# cart_user = cart_users[0]
			if cart_sessions:
				for cart in cart_sessions:
					if cart_session:
						self.mergeCart(cart, cart_session)
					else:
						cart_session = cart
				# cart_session = cart_sessions[0]

			if cart_user and cart_session and (cart_user != cart_session):
				self.mergeCart(cart_session, cart_user)

			if cart_user:
				cart_obj = cart_user
			elif cart_session and candidate_id:
				cart_session.owner_id = candidate_id
				cart_session.status = 2
				cart_session.save()
				cart_obj = cart_session
			elif cart_session:
				cart_obj = cart_session

			# update cart_obj in session
			if cart_obj:
				self.request.session.update({
					"cart_pk": cart_obj.pk,
					"checkout_type": 'cart',
				})

			elif request.session.get('cart_pk'):
				del request.session['cart_pk']
				del request.session['checkout_type']
				request.session.modified = True
			return cart_obj

		except Exception as e:
			logging.getLogger('error_log').error(str(e))

	def get_cart_items(self, cart_obj=None):
		cart_items = []
		try:
			if not cart_obj:
				if not self.request.session.get('cart_pk'):
					self.getCartObject()
				cart_pk = self.request.session.get('cart_pk')
				cart_obj = Cart.objects.get(pk=cart_pk)
			if cart_obj:
				main_products = cart_obj.lineitems.filter(parent=None).select_related('product', 'product__vendor')
				for m_prod in main_products:
					data = {}
					data['li'] = m_prod
					data['addons'] = cart_obj.lineitems.filter(parent=m_prod, parent_deleted=False).select_related('product')
					data['variations'] = cart_obj.lineitems.filter(parent=m_prod, parent_deleted=True).select_related('product')
					cart_items.append(data)
			return cart_items
		except Exception as e:
			logging.getLogger('error_log').error(str(e))
		return cart_items

	def getTotalAmount(self, cart_obj=None):
		total = Decimal(0)
		try:
			if not cart_obj:
				if not self.request.session.get('cart_pk'):
					self.getCartObject()
				cart_pk = self.request.session.get('cart_pk')
				cart_obj = Cart.objects.get(pk=cart_pk)
			if cart_obj:
				lis = cart_obj.lineitems.filter(no_process=False).select_related('product')
				for li in lis:
					total += li.product.get_price()
				lis = cart_obj.lineitems.filter(no_process=True).select_related('product')
				for li in lis:
					if li.product.type_service == 3 and li.no_process == True:
						pass
					else:
						total += li.product.get_price()
			return round(total, 0)
		except Exception as e:
			logging.getLogger('error_log').error(str(e))
		return round(total, 0)

	def getSelectedProduct(self, product):
		data = {'selected_products': []}
		if not self.request.session.get('cart_pk'):
			self.getCartObject()
		cart_pk = self.request.session.get('cart_pk')
		if cart_pk:
			cart_obj = Cart.objects.get(pk=cart_pk)
			try:
				parent_li = cart_obj.lineitems.get(product=product)
			except:
				parent_li = None
			if parent_li:
				selected_product = cart_obj.lineitems.filter(parent=parent_li).values_list('product__pk', flat=True)
				data['selected_products'] = selected_product
		return data

	def getSelectedProductPrice(self, product):
		data = {}
		total = Decimal(0)
		fake_total = Decimal(0)
		if not self.request.session.get('cart_pk'):
			self.getCartObject()
		cart_pk = self.request.session.get('cart_pk')
		if cart_pk:
			cart_obj = Cart.objects.get(pk=cart_pk)
			try:
				parent_li = cart_obj.lineitems.get(product=product)
				if parent_li.product.type_service == 3 and parent_li.no_process == True:
					pass
				else:
					total += parent_li.product.get_price()
					if parent_li.product.get_fakeprice():
						fake_total += parent_li.product.get_fakeprice()[0]
					else:
						fake_total += parent_li.product.get_price()
			except:
				parent_li = None
			if parent_li:
				lis = cart_obj.lineitems.filter(parent=parent_li).select_related('product')
				for li in lis:
					total += li.product.get_price()
					if li.product.get_fakeprice():
						fake_total += li.product.get_fakeprice()[0]
					else:
						fake_total += li.product.get_price()
		if fake_total > Decimal(0.00):
			diff = fake_total - total
			percent_diff = round((diff / fake_total) * 100, 0)
			data.update({'percent_diff': percent_diff, })

		data.update({
        	"product_total_price": round(total, 0),
        	"fake_total": round(fake_total, 0)})
		return data

	def get_cart_count(self, request=None):
		total_count = 0
		try:
			if not request:
				request = self.request
			if not request.session.get('cart_pk'):
				self.getCartObject()
			cart_pk = request.session.get('cart_pk')

			if cart_pk:
				cart_obj = Cart.objects.get(pk=cart_pk)
				total_count += cart_obj.lineitems.all().count()
				total_count -= cart_obj.lineitems.filter(
					parent=None, product__type_service=3,
					no_process=True).count()
				
		except Exception as e:
			logging.getLogger('error_log').error(str(e))
		return total_count