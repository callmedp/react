from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.shortcuts import render

from cart.mixins import CartMixin
from cart.models import Cart
from order.mixins import OrderMixin

from .forms import StateForm


class PaymentOptionView(TemplateView, OrderMixin):
	template_name = "payment/payment-option.html"

	def get(self, request, *args, **kwargs):
		candidate_id = request.session.get('candidate_id')
		if not candidate_id:
			return HttpResponseRedirect(reverse('cart:payment-login'))
		return super(self.__class__, self).get(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		candidate_id = request.session.get('candidate_id')
		if not candidate_id:
			return HttpResponseRedirect(reverse('cart:payment-login'))

		payment_type = request.POST.get('payment_type', '').strip()
		if payment_type == 'cash':
			form = StateForm(request.POST)
			if form.is_valid():
				cart_pk = request.session.get('cart_pk')
				if cart_pk:
					cart_obj = Cart.objects.get(pk=cart_pk)
					cart_obj.date_submitted = timezone.now()
					cart_obj.is_submitted = True
					cart_obj.save()
					order_status = 2
					self.createOrder(cart_obj, order_status)
					return HttpResponseRedirect(reverse('payment:thank-you'))
				else:
					return HttpResponseRedirect(reverse('cart:cart-product-list'))
			else:
				return render(request, self.template_name, {"state_form": form})
		else:
			HttpResponseRedirect(reverse('cart:cart-product-list'))

	def get_context_data(self, **kwargs):
		context = super(self.__class__, self).get_context_data(**kwargs)
		context.update({
			"state_form": StateForm(),
			"total_amount": self.getTotalAmount(),
		})
		return context


class ThankYouView(TemplateView):
	template_name = "payment/thank-you.html"

	def get(self, request, *args, **kwargs):
		candidate_id = request.session.get('candidate_id')
		if not candidate_id:
			return HttpResponseRedirect(reverse('cart:payment-login'))
		return super(self.__class__, self).get(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(self.__class__, self).get_context_data(**kwargs)
		return context