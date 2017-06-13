import json
import logging

from django.shortcuts import render, render_to_response
from django.views.generic import TemplateView, View, UpdateView
from django.forms.forms import NON_FIELD_ERRORS
from django.http import HttpResponseForbidden, HttpResponse,\
    HttpResponseRedirect, Http404, HttpResponsePermanentRedirect
from django.urls import reverse
from django.core.validators import validate_email
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.template.response import TemplateResponse

from shine.core import ShineCandidateDetail
from shop.models import Product
from users.mixins import RegistrationLoginApi, UserMixin

from .models import Cart
from .mixins import CartMixin
from .forms import ShippingDetailUpdateForm


class CartView(TemplateView, CartMixin, UserMixin):
    template_name = "cart/cart.html"

    def get(self, request, *args, **kwargs):
        return super(self.__class__, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        self.getCartObject()
        context.update({
            "cart_items": self.get_cart_items(),
            "total_amount": self.getTotalAmount(),
            "country_obj": self.get_client_country(self.request),
        })
        return context


class AddToCartView(View, CartMixin):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(AddToCartView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        if request.is_ajax():
            data = {"status": -1}
            cart_type = request.POST.get('cart_type')
            prod_id = request.POST.get('prod_id')

            try:
                product = Product.objects.get(id=prod_id, active=True)
                addons = request.POST.getlist('addons[]')
                req_options = request.POST.getlist('req_options[]')
                cv_id = request.POST.get('cv_id')
                data['status'] = self.updateCart(product, addons, cv_id, cart_type, req_options)
            except Exception as e:
                data['error_message'] = str(e)
                logging.getLogger('error_log').error("%s " % str(e))

            if data['status'] == 1 and cart_type == "express":
                data['redirect_url'] = reverse('cart:payment-login')

            data['cart_count'] = str(self.get_cart_count())

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
                    if line_obj.parent_deleted:
                        parent = line_obj.parent
                        childs = cart_obj.lineitems.filter(parent=parent, parent_deleted=True)
                        if childs.count() > 1:
                            line_obj.delete()
                        else:
                            parent.delete()
                    else:
                        line_obj.delete()

                    data['status'] = 1
                else:
                    data['error_message'] = 'this cart item alredy removed.'

            except Exception as e:
                data['error_message'] = str(e)

            return HttpResponse(json.dumps(data), content_type="application/json")

        return HttpResponseForbidden()


class PaymentLoginView(TemplateView):
    template_name = "cart/payment-login.html"

    def get(self, request, *args, **kwargs):
        candidate_id = request.session.get('candidate_id')
        if candidate_id:
            return HttpResponseRedirect(reverse('cart:payment-shipping'))
        return super(self.__class__, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            login_resp = {}
            login_dict = {}
            remember_me = request.POST.get('remember_me')
            email = self.request.POST.get('email').strip()
            password = self.request.POST.get('password')

            valid_email = False
            try:
                validate_email(email)
                valid_email = True
            except Exception as e:
                valid_email = False

            if valid_email:
                login_dict.update({
                    "email": email,
                    "password": password,
                })

                user_exist = RegistrationLoginApi().check_email_exist(login_dict['email'])

                if user_exist['exists'] and password:
                    login_resp = RegistrationLoginApi().user_login(login_dict)

                    if login_resp['response'] == 'login_user':
                        resp_status = ShineCandidateDetail().get_status_detail(email=None, shine_id=login_resp['candidate_id'])
                        self.request.session.update(resp_status)
                        if remember_me:
                            self.request.session.set_expiry(365 * 24 * 60 * 60)  # 1 year
                        return HttpResponseRedirect(reverse('cart:payment-shipping'))

                    elif login_resp['response'] == 'error_pass':
                        context = self.get_context_data()
                        context.update({
                            "non_field_error": login_resp.get("non_field_errors")[0],
                            'email_exist': True,
                            "email": email})
                        return TemplateResponse(request, self.template_name, context)

                elif user_exist['exists']:
                    context = self.get_context_data()
                    context.update({
                        'email': email,
                        'email_exist': True})
                    return TemplateResponse(request, self.template_name, context)

                elif not user_exist['exists']:
                    cart_pk = self.request.session.get('cart_pk')
                    if cart_pk:
                        cart_obj = Cart.objects.get(pk=cart_pk)
                        cart_obj.email = email
                        cart_obj.save()
                        return HttpResponseRedirect(reverse('cart:payment-shipping'))
                    return HttpResponseRedirect(reverse('cart:cart-product-list'))
            else:
                email_error = "Please enter valid email address."
                context = self.get_context_data()
                context.update({
                    "email_exist": False,
                    "email_error": email_error})
                return TemplateResponse(request, self.template_name, context)

        except Exception as e:
            logging.getLogger('error_log').error("%s " % str(e))
            return HttpResponseRedirect(reverse('cart:cart-product-list'))

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        context.update({
            "email_exist": False,
        })
        return context


class PaymentShippingView(UpdateView, CartMixin):
    model = Cart
    template_name = "cart/payment-shipping.html"
    success_url = "/cart/payment-summary/"
    http_method_names = [u'get', u'post']
    form_class = ShippingDetailUpdateForm

    def redirect_if_necessary(self):
        if not self.request.session.get('cart_pk'):
            self.getCartObject()
        cart_pk = self.request.session.get('cart_pk')
        if not cart_pk:
            return HttpResponsePermanentRedirect(reverse('homepage'))
        try:
            cart_obj = Cart.objects.get(pk=cart_pk)
        except:
            return HttpResponsePermanentRedirect(reverse('homepage'))

        if cart_obj and not (cart_obj.email or self.request.session.get('candidate_id')):
            return HttpResponsePermanentRedirect(reverse('cart:payment-login'))
        return None
       
    def get_object(self):
        if not self.request.session.get('cart_pk'):
            self.getCartObject()
        cart_pk = self.request.session.get('cart_pk')

        if cart_pk:
            try:
                obj = Cart.objects.get(pk=cart_pk)
            except:
                raise Http404
            return obj
        raise Http404

    def get(self, request, *args, **kwargs):
        redirect = self.redirect_if_necessary()
        if redirect:
            return redirect
        self.object = self.get_object()
        return super(self.__class__, self).get(request, args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        form = context['form']
        {'last_name': 'kumar', 'address': None, 'mobile': None, 'email': None, 'pincode': None, 'country': '91', 'country_code': '91', 'first_name': None, 'state': None}

        if self.request.session.get('candidate_id'):
            if not form.initial.get('first_name'):
                form.initial.update({
                    'first_name': self.request.session.get('first_name')})

            if not form.initial.get('last_name'):
                form.initial.update({
                    'last_name': self.request.session.get('last_name')})

            if not form.instance.email:
                form.instance.email = self.request.session.get('email')
                form.instance.save()

            if not form.initial.get('mobile'):
                form.initial.update({
                    'mobile': self.request.session.get('mobile_no')})

        if not form.initial.get('country_code'):
            form.initial.update({
                'country_code': '91'})

        if not form.initial.get('country'):
            form.initial.update({
                'country': 'India'})
        
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()

        if form.is_valid():
            try:
                # form.data['email]' = form.initial.get('email')  # readonly
                obj = form.save(commit=False)
                obj.shipping_done = True
                valid_form = self.form_valid(form)
                return valid_form
            except Exception as e:
                non_field_error = 'Persional detail not updated. due to %s' % (str(e))
                form._errors[NON_FIELD_ERRORS] = form.error_class([non_field_error])
                return self.form_invalid(form)
        return self.form_invalid(form)


class PaymentSummaryView(TemplateView, CartMixin):
    template_name = "cart/payment-summary.html"

    def redirect_if_necessary(self):
        if not self.request.session.get('cart_pk'):
            self.getCartObject()
        cart_pk = self.request.session.get('cart_pk')
        if not cart_pk:
            return HttpResponsePermanentRedirect(reverse('homepage'))
        try:
            cart_obj = Cart.objects.get(pk=cart_pk)
            if not cart_obj.shipping_done:
                return HttpResponsePermanentRedirect(reverse('cart:payment-shipping'))
        except:
            return HttpResponsePermanentRedirect(reverse('homepage'))
            
        return None

    def get(self, request, *args, **kwargs):
        redirect = self.redirect_if_necessary()
        if redirect:
            return redirect
        return super(self.__class__, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)

        if self.request.session.get('cart_pk') and self.request.session.get('checkout_type') == 'express':
            context.update({
                "cart_items": self.get_cart_items(),
                "total_amount": self.getTotalAmount(),
            })
        else:
            self.getCartObject()
            context.update({
                "cart_items": self.get_cart_items(),
                "total_amount": self.getTotalAmount(),
            })
        cart_obj = None
        cart_pk = self.request.session.get('cart_pk')
        try:
            cart_obj = Cart.objects.get(pk=cart_pk)
        except Cart.DoesNotExist:
            pass
        context.update({'coupon': cart_obj.coupon})
        return context


