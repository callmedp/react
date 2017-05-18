import logging

from django.utils import timezone
from django.conf import settings

from .models import Cart, LineItem


class CartMixin(object):
	def mergeCart(self, fromcart, tocart):
		from_items = fromcart.lineitems.all().select_related('product')
		for item in from_items:
			line_items = tocart.lineitems.filter(product=item.product)
			if line_items.count() < settings.CART_MAX_LIMIT:
				LineItem.objects.create(cart=tocart, product=item.product)
			item.delete()
		fromcart.status = 1
		fromcart.date_merged = timezone.now()
		fromcart.save()

	def updateCart(self, product):
		try:
			self.getCartObject()
			cart_pk = self.request.session.get('cart_pk')
			session_id = self.request.session.session_key
			candidate_id = self.request.session.get('candidate_id')
			if cart_pk:
				cart_obj = Cart.objects.get(pk=cart_pk)
			elif candidate_id:
				cart_obj = Cart.objects.create(owner_id=candidate_id, session_id=session_id, status=2)
			elif session_id:
				cart_obj = Cart.objects.create(session_id=session_id, status=0)

			if cart_obj:
				flag = 0  # already exist in cart
				line_items = cart_obj.lineitems.filter(product=product)
				if line_items.count() < settings.CART_MAX_LIMIT:
					li = LineItem.objects.create(cart=cart_obj, product=product)
					li.reference = str(cart_obj.pk) + '_' + str(li.pk)
					li.save()
					flag = 1   # added to cart
				return flag
		except Exception as e:
			logging.getLogger('error_log').error(str(e))

	def createExpressCart(self, product):
		try:
			flag = -1
			candidate_id = self.request.session.get('candidate_id')
			if not self.request.session.session_key:
				self.request.session.create()
			session_id = self.request.session.session_key
			if candidate_id:
				cart_obj = Cart.objects.create(owner_id=candidate_id, session_id=session_id, status=3)
			elif session_id:
				cart_obj = Cart.objects.create(session_id=session_id, status=3)

			if cart_obj:
				li = LineItem.objects.create(cart=cart_obj, product=product)
				li.reference = str(cart_obj.pk) + '_' + str(li.pk)
				li.save()
				flag = 1
				self.request.session.update({
					"cart_pk": cart_obj.pk,
					"checkout_type": 'express',
				})

			return flag

		except Exception as e:
			logging.getLogger('error_log').error(str(e))

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
				cart_user = cart_users[0]
			if cart_sessions:
				cart_session = cart_sessions[0]

			if cart_user and cart_session and (cart_user != cart_session):
				self.mergeCart(cart_session, cart_user)

			if cart_user:
				cart_obj = cart_user
			elif cart_session and candidate_id:
				cart_session.owner_id = candidate_id
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

		except Exception as e:
			logging.getLogger('error_log').error(str(e))

	def get_cart_items(self):

		if not self.request.session.get('cart_pk'):
			self.getCartObject()
		cart_pk = self.request.session.get('cart_pk')
		if cart_pk:
			cart_obj = Cart.objects.get(pk=cart_pk)
			if cart_obj:
				cart_items = cart_obj.lineitems.all().select_related('parent', 'product')
				return cart_items
		return None
