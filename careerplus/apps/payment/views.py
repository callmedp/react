from django.views.generic import TemplateView
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect
from django.urls import reverse
from django.utils import timezone
from django.shortcuts import render

from cart.models import Cart
from order.mixins import OrderMixin

from .forms import StateForm
from .mixin import PaymentMixin


class PaymentOptionView(TemplateView, OrderMixin, PaymentMixin):
    template_name = "payment/payment-option.html"

    def redirect_if_necessary(self):
        if not self.request.session.get('cart_pk'):
            self.getCartObject()
        cart_pk = self.request.session.get('cart_pk')
        if not cart_pk:
            return HttpResponsePermanentRedirect(reverse('cart:cart-product-list'))
        try:
            cart_obj = Cart.objects.get(pk=cart_pk)
        except:
            return HttpResponsePermanentRedirect(reverse('cart:cart-product-list'))

        if cart_obj and not (cart_obj.email or self.request.session.get('candidate_id')):
            return HttpResponsePermanentRedirect(reverse('cart:payment-login'))
        return None

    def get(self, request, *args, **kwargs):
        redirect = self.redirect_if_necessary()
        if redirect:
            return redirect
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
                    order_type = "CASH"
                    self.process_payment_method(order_type, request)
                    return HttpResponseRedirect(reverse('payment:thank-you'))
                else:
                    return HttpResponseRedirect(reverse('cart:cart-product-list'))
            else:
                context = self.get_context_data()
                context['state_form'] = form
                return render(request, self.template_name, context)
        else:
            HttpResponseRedirect(reverse('cart:cart-product-list'))

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        context.update({
            "state_form": StateForm(),
            "total_amount": self.getTotalAmount(),
            "cart_id": self.request.session.get('cart_pk'),
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