from django.views.generic import TemplateView
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect
from django.urls import reverse
from django.shortcuts import render

from cart.models import Cart
from order.mixins import OrderMixin
from order.models import Order

from .forms import StateForm, PayByCheckForm
from .mixin import PaymentMixin
from microsite.roundoneapi import RoundOneAPI


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

        if cart_obj and not (cart_obj.shipping_done):
            return HttpResponsePermanentRedirect(reverse('cart:payment-login'))
        return None

    def get(self, request, *args, **kwargs):
        redirect = self.redirect_if_necessary()
        if redirect:
            return redirect
        return super(self.__class__, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        payment_type = request.POST.get('payment_type', '').strip()
        if payment_type == 'cash':
            form = StateForm(request.POST)
            if form.is_valid():
                cart_pk = request.session.get('cart_pk')
                if cart_pk:
                    cart_obj = Cart.objects.get(pk=cart_pk)
                    self.fridge_cart(cart_obj)
                    self.createOrder(cart_obj)
                    order_type = "CASH"
                    return_parameter = self.process_payment_method(order_type, request)
                    return HttpResponseRedirect(return_parameter)
                else:
                    return HttpResponseRedirect(reverse('cart:cart-product-list'))
            else:
                context = self.get_context_data()
                context['state_form'] = form
                return render(request, self.template_name, context)
        elif payment_type == 'cheque':
            form = PayByCheckForm(request.POST)
            if form.is_valid():
                cart_pk = request.session.get('cart_pk')
                if cart_pk:
                    cart_obj = Cart.objects.get(pk=cart_pk)
                    self.fridge_cart(cart_obj)
                    self.createOrder(cart_obj)
                    order_type = "CHEQUE"
                    return_parameter = self.process_payment_method(order_type, request)
                    return HttpResponseRedirect(return_parameter)
                else:
                    return HttpResponseRedirect(reverse('cart:cart-product-list'))
            else:
                context = self.get_context_data()
                context['check_form'] = form
                return render(request, self.template_name, context)

        else:
           return HttpResponseRedirect(reverse('cart:cart-product-list'))

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        context.update({
            "state_form": StateForm(),
            "check_form": PayByCheckForm(),
            "total_amount": self.getTotalAmount(),
            "cart_id": self.request.session.get('cart_pk'),
        })
        return context


class ThankYouView(TemplateView):
    template_name = "payment/thank-you.html"

    def get(self, request, *args, **kwargs):
        if self.request.session.get('order_pk'):
            return super(self.__class__, self).get(request, *args, **kwargs)
        return HttpResponseRedirect('cart:cart-product-list')

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        order_pk = self.request.session.get('order_pk')
        if order_pk:
            order = Order.objects.get(pk=order_pk)
            order_items = []
            if order:
                parent_ois = order.orderitems.filter(parent=None).select_related('product', 'partner')
                for p_oi in parent_ois:
                    data = {}
                    data['oi'] = p_oi
                    data['addons'] = order.orderitems.filter(parent=p_oi, is_combo=False, is_variation=False, no_process=False).select_related('product', 'partner')
                    data['variations'] = order.orderitems.filter(parent=p_oi, is_variation=True).select_related('product', 'partner')
                    order_items.append(data)
                context.update({
                    'orderitems': order_items,
                    'order': order})

        return context


class PaymentOopsView(TemplateView):
    template_name = 'payment/payment-oops.html'

    def get(self, request, *args, **kwargs):
        return super(self.__class__, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        error_type = self.request.GET.get('error', '')
        txn_id = self.request.GET.get('txn_id', '')
        context = super(self.__class__, self).get_context_data(**kwargs)
        context.update({'error_type': error_type, 'txn_id': txn_id})
        context.update({'is_payment': True, })
        return context
