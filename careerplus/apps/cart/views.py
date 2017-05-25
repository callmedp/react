import json
import logging

from django.shortcuts import render
from django.views.generic import TemplateView, View, UpdateView
from django.forms.forms import NON_FIELD_ERRORS
from django.http import HttpResponseForbidden, HttpResponse,\
    HttpResponseRedirect, Http404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from shine.core import ShineCandidateDetail
from shop.models import Product
from users.mixins import RegistrationLoginApi
from users.forms import ModalLoginApiForm

from .models import Cart, ShippingDetail
from .mixins import CartMixin
from .forms import ShippingDetailUpdateForm


class CartView(TemplateView, CartMixin):
    template_name = "cart/cart.html"

    def get(self, request, *args, **kwargs):
        return super(self.__class__, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        self.getCartObject()
        context.update({
            "cart_items": self.get_cart_items(),
            "total_amount": self.getTotalAmount(),
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
                cv_id = request.POST.get('cv_id')
                data['status'] = self.updateCart(product, addons, cv_id, cart_type)
            except Exception as e:
                data['error_message'] = str(e)
                logging.getLogger('error_log').error("%s " % str(e))

            if data['status'] == 1 and cart_type == "express":
                data['redirect_url'] = reverse('cart:payment-login')

            return HttpResponse(json.dumps(data), content_type="application/json")


            # if prod_id and cart_type == "cart":
            #     try:
            #         product = Product.objects.get(id=prod_id, active=True)
            #         addons = request.POST.getlist('addons[]')
            #         cv_id = request.POST.get('cv_id')
            #         data['status'] = self.updateCart(product, addons, cv_id, cart_type)
            #     except Exception as e:
            #         data['error_message'] = str(e)
            #         logging.getLogger('error_log').error("%s " % str(e))
            #     return HttpResponse(json.dumps(data), content_type="application/json")

            # elif prod_id and cart_type == "express":
            #     try:
            #         product = Product.objects.get(id=prod_id, active=True)
            #         addons = request.POST.getlist('addons[]')
            #         cv_id = request.POST.get('cv_id')
            #         data['status'] = self.updateCart(product, addons, cv_id, cart_type)
            #         if data['status'] == 1:
            #             data['redirect_url'] = reverse('cart:payment-login')

            #     except Exception as e:
            #         data['error_message'] = str(e)
            #         logging.getLogger('error_log').error("%s " % str(e))
            #     return HttpResponse(json.dumps(data), content_type="application/json")


            # data = {"status": -1}
            # cart_type = request.POST.get('cart_type')
            # if cart_type == 'enrol_cart':
            #     prod_id = request.POST.get('product_id', '')
            #     try:
            #         product = Product.objects.get(id=prod_id, active=True)
            #         data['status'] = self.createExpressCart(product)
            #     except Exception as e:
            #         data['error_message'] = str(e)

            #     if data['status'] == 1:
            #         data['redirect_url'] = reverse('cart:payment-login')

            #     return HttpResponse(json.dumps(data), content_type="application/json")

            # elif cart_type == 'add_cart':
            #     prod_id = request.POST.get('product_id', '')
            #     try:
            #         product = Product.objects.get(id=prod_id, active=True)
            #         data['status'] = self.updateCart(product)
            #     except Exception as e:
            #         data['error_message'] = str(e)

            #     return HttpResponse(json.dumps(data), content_type="application/json")

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


class PaymentLoginView(TemplateView):
    template_name = "cart/payment-login.html"

    def get(self, request, *args, **kwargs):
        candidate_id = request.session.get('candidate_id')
        if candidate_id:
            return HttpResponseRedirect(reverse('cart:payment-shipping'))
        return super(self.__class__, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        try:
            form = ModalLoginApiForm(request.POST)
            login_resp = {}
            if form.is_valid():
                login_dict = {}
                remember_me = request.POST.get('remember_me')
                login_dict = {}
                login_dict.update({
                    "email": self.request.POST.get('email'),
                    "password": self.request.POST.get('password')
                })

                user_exist = RegistrationLoginApi().check_email_exist(login_dict['email'])

                if user_exist['exists']:
                    login_resp = RegistrationLoginApi().user_login(login_dict)

                    if login_resp['response'] == 'login_user':
                        resp_status = ShineCandidateDetail().get_status_detail(email=None, shine_id=login_resp['candidate_id'])
                        self.request.session.update(resp_status)
                        if remember_me:
                            self.request.session.set_expiry(365 * 24 * 60 * 60)  # 1 year
                        return HttpResponseRedirect(reverse('cart:payment-shipping'))

                    elif login_resp['response'] == 'error_pass':
                        non_field_error = login_resp.get("non_field_errors")[0]
                        return render(request, self.template_name, {'non_field_error': non_field_error, 'form': form})

                elif not user_exist['exists']:
                    non_field_error = 'This email is not registered. Please register.'
                    return render(request, self.template_name, {'non_field_error': non_field_error, 'form': form})
            else:
                return render(request, self.template_name, {'form': form})

        except Exception as e:
            logging.getLogger('error_log').error("%s " % str(e))

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        context.update({
            "form": ModalLoginApiForm(),
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
                "total_amount": self.getTotalAmount(),
            })
        else:
            self.getCartObject()
            context.update({
                "cart_items": self.get_cart_items(),
                "total_amount": self.getTotalAmount(),
            })
        return context