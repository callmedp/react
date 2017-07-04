import json
import logging
from decimal import Decimal
from django.utils import timezone
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
from wallet.models import Wallet

class CartView(TemplateView, CartMixin, UserMixin):
    template_name = "cart/cart.html"

    def get_recommended_products(self):
        recommended_products = []
        # recommended_products = Product.objects.filter(
        #     type_service=3, type_product__in=[0, 1, 3], active=True)
        return {'recommended_products': list(recommended_products)}

    def get(self, request, *args, **kwargs):
        return super(self.__class__, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        cart_obj = self.getCartObject()
        context.update({
            "cart_items": self.get_cart_items(cart_obj=cart_obj),
            "total_amount": self.getTotalAmount(cart_obj=cart_obj),
            "country_obj": self.get_client_country(self.request),
        })
        if not context['cart_items']:
            context.update(self.get_recommended_products())
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

                user_exist = RegistrationLoginApi.check_email_exist(login_dict['email'])

                if user_exist.get('exists') and password:
<<<<<<< HEAD
                    login_resp = RegistrationLoginApi.user_login(login_dict)
=======
                    login_resp = RegistrationLoginApi().user_login(login_dict)
>>>>>>> flow1

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

                elif user_exist.get('exists'):
                    context = self.get_context_data()
                    context.update({
                        'email': email,
                        'email_exist': True})
                    return TemplateResponse(request, self.template_name, context)

                elif not user_exist.get('exists'):
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
            return HttpResponseRedirect(reverse('homepage'))

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

    def __init__(self):
        self.cart_obj = None

    def redirect_if_necessary(self):
        if not self.request.session.get('cart_pk'):
            self.cart_obj = self.getCartObject()
        else:
            cart_pk = self.request.session.get('cart_pk')
            try:
                self.cart_obj = Cart.objects.get(pk=cart_pk)
                if not self.cart_obj.shipping_done:
                    return HttpResponsePermanentRedirect(reverse('cart:payment-shipping'))
            except:
                return HttpResponsePermanentRedirect(reverse('homepage'))

        if not self.cart_obj:
            return HttpResponsePermanentRedirect(reverse('homepage'))

        return None

    def get(self, request, *args, **kwargs):
        redirect = self.redirect_if_necessary()
        if redirect:
            return redirect
        return super(self.__class__, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
<<<<<<< HEAD
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
        cart_obj, wal_obj = None, None
        cart_coupon, cart_wallet  = None, None
        wal_txn, wal_total, wal_point = None, None, None
        
        cart_pk = self.request.session.get('cart_pk')
        try:
            cart_obj = Cart.objects.get(pk=cart_pk)
        except Cart.DoesNotExist:
            cart_obj = None
        if cart_obj:
            wal_txn = cart_obj.wallettxn.filter(txn_type=2).order_by('-created').select_related('wallet')
            cart_coupon = cart_obj.coupon
            if cart_coupon:
                wal_obj = None
            elif wal_txn:
                wal_obj = None
                wal_txn = wal_txn[0]
                points = wal_txn.point_txn.all()
                points_active = points.filter(expiry__gte=timezone.now())
                points_used = wal_txn.usedpoint.all()
                
                if len(points_active) == len(points):
                    cart_wallet = wal_txn
                    wal_point = wal_txn.point_value
                else:
                    points_used = wal_txn.usedpoint.all().order_by('point__pk')
                    for pts in points_used:
                        point = pts.point
                        point.current += pts.point_value
                        point.last_used = timezone.now()
                        pts.txn_type = 5
                        if point.expiry <= timezone.now():
                            point.status = 3
                        else:
                            if point.current > Decimal(0):
                                point.status = 1
                            else:
                                point.status = 2
                        point.save()
                        pts.save()
                    wal_txn.txn_type = 5
                    wal_txn.notes = 'Auto Reverted From Cart'
                    wal_txn.status = 1
                    wal_txn.save()
                    wal_obj = wal_txn.wallet
                    wal_total = wal_obj.get_current_amount()
                    if wal_total <= Decimal(0):
                        wal_obj = None
            elif cart_obj.owner_id:
                wal_obj, created = Wallet.objects.get_or_create(owner=cart_obj.owner_id)
                wal_total = wal_obj.get_current_amount()
                if wal_total <= Decimal(0):
                    wal_obj = None

        context.update({
            'cart_coupon': cart_coupon, 'cart_wallet': cart_wallet, 'wallet': wal_obj,
            'cart': cart_obj, 'wallet_total': wal_total, 'wallet_point': wal_point})
=======
>>>>>>> flow1
        context.update({
            "cart_items": self.get_cart_items(cart_obj=self.cart_obj),
            "total_amount": self.getTotalAmount(cart_obj=self.cart_obj),
        })
        return context
