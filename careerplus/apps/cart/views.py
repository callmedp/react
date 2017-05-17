import json

from django.shortcuts import render
from django.views.generic import TemplateView, View, UpdateView
from django.forms.forms import NON_FIELD_ERRORS
from django.http import HttpResponseForbidden, HttpResponse,\
	HttpResponseRedirect, Http404
from django.urls import reverse

from shine.core import ShineCandidateDetail
from shop.models import Product
from users.mixins import RegistrationLoginApi

from .models import Cart, LineItem, ShippingDetail
from .mixins import CartMixin
from .forms import LoginForm, ShippingDetailUpdateForm


class CartView(TemplateView, CartMixin):
	template_name = "cart/cart.html"

	def get(self, request, *args, **kwargs):
		# print ("sessionid", request.session.session_key
		return super(self.__class__, self).get(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(self.__class__, self).get_context_data(**kwargs)
		cart_obj = self.getCartObject(self.request)
		context.update({
			"cart_items": self.get_cart_items(cart_obj),
		})
		return context


class AddToCartView(View, CartMixin):

	def post(self, request, *args, **kwargs):
		if request.is_ajax():
			data = {"status": -1}
			prod_id = request.POST.get('product_id', '')
			try:
				product = Product.objects.get(id=prod_id, active=True)
				candidate_id = request.session.get('candidate_id')
				if not request.session.session_key:
					request.session.create()
				sessionid = request.session.session_key

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

				else:
					data['error_message'] = 'Your session doesn\'t exist.'

			except Exception as e:
				data['error_message'] = str(e)

			return HttpResponse(json.dumps(data), content_type="application/json")

		return HttpResponseForbidden()


class RemoveFromCartView(View,):

	def post(self, request, *args, **kwargs):
		if request.is_ajax():
			data = {"status": -1}
			line_id = request.POST.get('line_item', '')
			try:
				line_obj = LineItem.objects.get(id=line_id)
				line_obj.delete()
				data['status'] = 1
			except Exception as e:
				data['error_message'] = str(e)

			return HttpResponse(json.dumps(data), content_type="application/json")

		return HttpResponseForbidden()


class PaymentLoginView(TemplateView, RegistrationLoginApi, ShineCandidateDetail):
	template_name = "cart/payment-login.html"

	def get(self, request, *args, **kwargs):
		candidate_id = request.session.get('candidate_id')
		if candidate_id:
			return HttpResponseRedirect(reverse('cart:payment-shipping'))
		return super(self.__class__, self).get(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		try:
			email = request.POST.get('email', '').strip()
			password = request.POST.get('password', '').strip()
			loginform = LoginForm(request.POST)
			if loginform.is_valid() and email and password:
				login_resp = self.user_login(self.request)
				if login_resp['response'] == 'login_user':
					resp_status = self.get_status_detail(email=None, shine_id=login_resp['candidate_id'])
					if resp_status:
						request.session.update(resp_status)
					return HttpResponseRedirect(reverse('cart:payment-shipping'))
				elif login_resp['response'] == 'error_pass':
					non_field_error = login_resp.get("non_field_errors")[0]
					return render(request, self.template_name, {'non_field_error': non_field_error})
		except Exception as e:
			non_field_error = str(e)
		non_field_err = non_field_error
		return render(request, self.template_name, {'non_field_error': non_field_err})

	def get_context_data(self, **kwargs):
		context = super(self.__class__, self).get_context_data(**kwargs)
		context.update({
			"login_form": LoginForm(),
		})
		return context


# class PaymentShippingView(TemplateView):
# 	template_name = "cart/payment-shipping.html"

# 	def get(self, request, *args, **kwargs):
# 		candidate_id = request.session.get('candidate_id')
# 		if not candidate_id:
# 			return HttpResponseRedirect(reverse('cart:payment-login'))
# 		return super(self.__class__, self).get(request, *args, **kwargs)

# 	def get_context_data(self, **kwargs):
# 		context = super(self.__class__, self).get_context_data(**kwargs)
# 		return context


class PaymentShippingView(UpdateView):
	model = ShippingDetail
	template_name = "cart/payment-shipping.html"
	success_url = "/cart/payment-summary/"
	http_method_names = [u'get', u'post']
	form_class = ShippingDetailUpdateForm

	def get_object(self):
		candidate_id = self.request.session.get('candidate_id')
		if candidate_id:
			try:
				obj, created = ShippingDetail.objects.get_or_create(candidate_id=candidate_id)
			except:
				raise Http404
			return obj
		raise Http404

	def get(self, request, *args, **kwargs):
		self.object = self.get_object()
		return super(self.__class__, self).get(request, args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(self.__class__, self).get_context_data(**kwargs)
		return context

	def post(self, request, *args, **kwargs):
		self.object = self.get_object()
		form = self.get_form()

		if form.is_valid():
			try:
				valid_form = self.form_valid(form)
				return valid_form
			except Exception as e:
				non_field_error = 'Persional detail not updated. due to %s' % (str(e))
				form._errors[NON_FIELD_ERRORS] = form.error_class([non_field_error])
				return self.form_invalid(form)
		return self.form_invalid(form)


class PaymentSummaryView(TemplateView, CartMixin):
	template_name = "cart/payment-summary.html"

	def get(self, request, *args, **kwargs):
		candidate_id = request.session.get('candidate_id')
		if not candidate_id:
			return HttpResponseRedirect(reverse('cart:payment-login'))

		return super(self.__class__, self).get(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(self.__class__, self).get_context_data(**kwargs)
		cart_obj = self.getCartObject(self.request)
		context.update({
			"cart_items": self.get_cart_items(cart_obj),
		})
		return context