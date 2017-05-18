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

from .models import Cart, ShippingDetail
from .mixins import CartMixin
from .forms import LoginForm, ShippingDetailUpdateForm


class CartView(TemplateView, CartMixin):
	template_name = "cart/cart.html"

	def get(self, request, *args, **kwargs):
		return super(self.__class__, self).get(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(self.__class__, self).get_context_data(**kwargs)
		self.getCartObject()
		context.update({
			"cart_items": self.get_cart_items(),
		})
		return context


class AddToCartView(View, CartMixin):

	def post(self, request, *args, **kwargs):
		if request.is_ajax():
			data = {"status": -1}
			cart_type = request.POST.get('cart_type')
			if cart_type == 'enrol_cart':
				prod_id = request.POST.get('product_id', '')
				try:
					product = Product.objects.get(id=prod_id, active=True)
					data['status'] = self.createExpressCart(product)
				except Exception as e:
					data['error_message'] = str(e)

				if data['status'] == 1:
					data['redirect_url'] = reverse('cart:payment-login')

				return HttpResponse(json.dumps(data), content_type="application/json")

			elif cart_type == 'add_cart':
				prod_id = request.POST.get('product_id', '')
				try:
					product = Product.objects.get(id=prod_id, active=True)
					data['status'] = self.updateCart(product)
				except Exception as e:
					data['error_message'] = str(e)

				return HttpResponse(json.dumps(data), content_type="application/json")

		return HttpResponseForbidden()


class RemoveFromCartView(View, CartMixin):

	def post(self, request, *args, **kwargs):
		if request.is_ajax():
			data = {"status": -1}
			reference = request.POST.get('reference_id')
			try:
				if not self.request.session.get('cart_pk'):
					self.getCartObject()

				cart_pk = self.request.session.get('cart_pk')
				if cart_pk:
					cart_obj = Cart.objects.get(pk=cart_pk)
					line_obj = cart_obj.lineitems.get(reference=reference)
					line_obj.delete()
					data['status'] = 1
				else:
					data['error_message'] = 'this cart item alredy removed.'

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
		if self.request.session.get('cart_pk') and self.request.session.get('checkout_type') == 'express':
			context.update({
				"cart_items": self.get_cart_items(),
			})
		else:
			self.getCartObject()
			context.update({
				"cart_items": self.get_cart_items(),
			})
		return context