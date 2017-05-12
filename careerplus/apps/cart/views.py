import json

from django.views.generic import TemplateView, View
from django.http import HttpResponseForbidden, HttpResponse

from shop.models import Product

from .models import Cart, LineItem
from .mixins import CartMixin


class CartView(TemplateView, CartMixin):
	template_name = "cart/cart.html"

	def get(self, request, *args, **kwargs):
		# print ("sessionid", request.COOKIES['sessionid'])\
		cart_obj = self.getCartObject(request)

		return super(self.__class__, self).get(request, *args, **kwargs)


class AddToCartView(View, CartMixin):

	def post(self, request, *args, **kwargs):
		if request.is_ajax():
			data = {"status": -1}
			prod_id = request.POST.get('product_id', '')
			try:
				product = Product.objects.get(id=prod_id, active=True)
				candidate_id = request.session.get('candidate_id')
				sessionid = request.COOKIES['sessionid']
				if candidate_id:
					cart_users = Cart.objects.filter(owner_id=candidate_id, status=2)
					if cart_users:
						cart_user = cart_users[0]

						try:
							cart_session = Cart.objects.get(session_id=sessionid, status=0)
						except:
							cart_session = None
						if cart_session:
							self.mergeCart(cart_session, cart_user)

						data['status'] = self.updateCart(cart_user, product)

					else:
						cart_session, created = Cart.objects.get_or_create(session_id=sessionid, status=0)
						cart_session.owner_id = candidate_id
						cart_session.status = 2
						cart_session.save()
						data['status'] = self.updateCart(cart_session, product)
					
				elif sessionid:
					cart_session, created = Cart.objects.get_or_create(session_id=sessionid, status=0)
					data['status'] = self.updateCart(cart_session, product)

			except Exception as e:
				data['error_message'] = str(e)

			return HttpResponse(json.dumps(data), content_type="application/json")

		return HttpResponseForbidden()
