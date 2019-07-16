import json
import logging
from decimal import Decimal
from django.utils import timezone
from django.views.generic import TemplateView, View, UpdateView
from django.forms.forms import NON_FIELD_ERRORS
from django.http import HttpResponseForbidden, HttpResponse, \
    HttpResponseRedirect, Http404
from django.urls import reverse
from django.core.validators import validate_email
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.template.response import TemplateResponse
from django.conf import settings
from users.forms import (
    PasswordResetRequestForm, )

from shine.core import ShineCandidateDetail
from shop.models import Product, ProductClass
from users.mixins import RegistrationLoginApi, UserMixin
from console.decorators import Decorate, stop_browser_cache
from wallet.models import Wallet
from geolocation.models import Country
from users.tasks import user_register
from search.helpers import get_recommendations
from cart.tasks import cart_drop_out_mail, create_lead_on_crm

from .models import Cart
from .mixins import CartMixin
from .forms import ShippingDetailUpdateForm


@Decorate(stop_browser_cache())
class CartView(TemplateView, CartMixin, UserMixin):
    template_name = "cart/cart.html"

    def get_recommended_products(self):
        rcourses = get_recommendations(self.request.session.get('func_area', None),
                                       self.request.session.get('skills', None))
        if rcourses:
            rcourses = rcourses[:6]
        return {'recommended_products': rcourses}

    def get(self, request, *args, **kwargs):

        return super(self.__class__, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        cart_obj = self.getCartObject()
        line_items_list = cart_obj.lineitems.filter(parent=None)
        type_flow = -1
        if len(line_items_list):
            line_item = line_items_list[0];
            type_flow = int(line_item.product.type_flow)
        #  resume builder flow handle
        if type_flow == 17:
            cart_dict = self.get_local_cart_items(cart_obj=cart_obj)
        else:
            cart_dict = self.get_solr_cart_items(cart_obj=cart_obj)
        cart_items = cart_dict.get('cart_items', [])
        total_amount = cart_dict.get('total_amount')
        context.update({
            "cart_items": cart_items,
            "total_amount": total_amount,
        })
        if not context['cart_items']:
            context.update(self.get_recommended_products())

        return context


class AddToCartView(View, CartMixin):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(AddToCartView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {"status": -1}
        cart_type = request.POST.get('cart_type')
        prod_id = request.POST.get('prod_id', '')
        cart_pk = request.session.get('cart_pk', '')
        is_resume_template = request.POST.get('add_resume', False)
        candidate_id = request.session.get('candidate_id', '')
        try:
            product = Product.objects.get(id=int(prod_id))  # not filter on active because product is coming from solr
            addons = request.POST.getlist('addons[]')
            req_options = request.POST.getlist('req_options[]')
            cv_id = request.POST.get('cv_id')
            data['status'] = self.updateCart(product, addons, cv_id, cart_type, req_options, is_resume_template)

            try:
                cart_obj = Cart.objects.get(pk=cart_pk)
            except Exception as e:
                logging.getLogger('error_log').error('unable to get cart object %s' % str(e))
                cart_obj = None
            logging.getLogger('info_log').info(
                "Cart Obj:{}, candidate_ID: {}, Owner ID:{}".format(cart_obj, candidate_id, cart_obj.owner_id))
            if cart_obj and (candidate_id == cart_obj.owner_id) and not request.ip_restricted:
                first_name = request.session.get('first_name', '')
                last_name = request.session.get('last_name', '')
                email = request.session.get('email', '')
                name = "{}{}".format(first_name, last_name)
                # cart_drop_out_mail.apply_async(
                #     (cart_pk, email),
                #     countdown=settings.CART_DROP_OUT_EMAIL)
                source_type = "cart_drop_out"

                create_lead_on_crm.apply_async(
                    (cart_obj.pk, source_type, name),
                    countdown=settings.CART_DROP_OUT_LEAD)
        except Exception as e:
            data['error_message'] = str(e)
            logging.getLogger('error_log').error("%s " % str(e))

        if data['status'] == 1 and cart_type == "express":
            data['redirect_url'] = reverse('cart:payment-login')

        data['cart_count'] = str(self.get_cart_count())
        data['cart_url'] = reverse('cart:payment-summary')

        return HttpResponse(json.dumps(data), content_type="application/json")


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
                    data['error_message'] = 'this cart item already removed.'

            except Exception as e:
                data['error_message'] = str(e)
                logging.getLogger('error_log').error("unable to remove item from cart%s " % str(e))

            return HttpResponse(json.dumps(data), content_type="application/json")

        return HttpResponseForbidden()


@Decorate(stop_browser_cache())
class PaymentLoginView(TemplateView, CartMixin):
    template_name = "cart/payment-login.html"

    def get(self, request, *args, **kwargs):
        candidate_id = request.session.get('candidate_id')
        cart_pk = request.session.get('cart_pk')
        try:
            self.cart_obj = Cart.objects.get(pk=cart_pk)
            self.cart_obj.shipping_done = True
            self.cart_obj.save()
        except Exception as e:
            logging.getLogger('error_log').error("unable to assign cart object to self %s " % str(e))
            return HttpResponseRedirect(reverse('homepage'))
        if candidate_id:
            return HttpResponseRedirect(reverse('payment:payment-option'))
        return super(self.__class__, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            login_resp = {}
            login_dict = {}
            remember_me = request.POST.get('remember_me')
            email = self.request.POST.get('email', '').strip()
            password = self.request.POST.get('password', '')
            login_with = self.request.POST.get('login_with', '')
            mobile_number = ''
            guest_name = ''

            valid_email = False
            try:
                validate_email(email)
                valid_email = True
            except Exception as e:
                logging.getLogger('error_log').error("email validation failed  %s " % str(e))
                valid_email = False

            if valid_email and login_with:
                cart_pk = self.request.session.get('cart_pk')
                mobile_number = self.request.POST.get('mobile', '')
                guest_name = self.request.POST.get('name', '')
                if guest_name:
                    first_name = guest_name.strip().split(' ')[0]
                    last_name = ' '.join((guest_name + ' ').split(' ')[1:]).strip()
                if cart_pk:
                    cart_obj = Cart.objects.get(pk=cart_pk)
                    cart_obj.email = email
                    cart_obj.owner_email = email
                    cart_obj.mobile = mobile_number
                    cart_obj.first_name = first_name
                    cart_obj.last_name = last_name
                    # registering user into shine (for getting candidate/owner id
                    data = {}
                    data.update({
                        "email": cart_obj.email,
                        "country_code": cart_obj.country_code,
                        "cell_phone": cart_obj.mobile,
                        "name": guest_name,
                    })
                    candidate_id, error = user_register(data=data)
                    # error handling
                    cart_obj.owner_id = candidate_id
                    resp_status = ShineCandidateDetail().get_status_detail(email=None,
                                                                           shine_id=candidate_id)
                    self.request.session.update(resp_status)
                    cart_obj.save()
                    return HttpResponseRedirect(reverse('payment:payment-option'))
                return HttpResponseRedirect(reverse('cart:cart-product-list'))

            if valid_email:
                login_dict.update({
                    "email": email,
                    "password": password,
                })
                user_exist = RegistrationLoginApi.check_email_exist(login_dict['email'])

                if user_exist.get('exists') and password:
                    login_resp = RegistrationLoginApi.user_login(login_dict)

                    if login_resp['response'] == 'login_user':
                        resp_status = ShineCandidateDetail().get_status_detail(email=None,
                                                                               shine_id=login_resp['candidate_id'])
                        self.request.session.update(resp_status)
                        cart_pk = self.request.session.get('cart_pk')
                        if cart_pk:
                            cart_obj = Cart.objects.get(pk=cart_pk)
                            cart_obj.email = email
                            cart_obj.owner_id = login_resp['candidate_id']
                            cart_obj.owner_email = email
                            cart_obj.first_name = self.request.session.get('first_name', '')
                            cart_obj.save()
                        if remember_me:
                            self.request.session.set_expiry(
                                settings.SESSION_COOKIE_AGE)  # 1 year
                        return HttpResponseRedirect(reverse('payment:payment-option'))

                    elif login_resp['response'] == 'error_pass':
                        context = self.get_context_data()
                        context.update({
                            "non_field_error": login_resp.get("non_field_errors")[0],
                            'email_exist': True,
                            "email": email})
                        return TemplateResponse(request, self.template_name, context)

                elif user_exist.get('exists'):
                    context = self.get_context_data()
                    context.update({"guest_login": "guest_login"})
                    cart_pk = self.request.session.get('cart_pk')
                    if cart_pk:
                        cart_obj = Cart.objects.get(pk=cart_pk)
                        cart_obj.email = email
                        cart_obj.save()
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
                        return HttpResponseRedirect(reverse('payment:payment-option'))
                    return HttpResponseRedirect(reverse('cart:cart-product-list'))
            else:
                email_error = "Please enter valid email address."
                context = self.get_context_data()
                context.update({
                    "email_exist": False,
                    "email_error": email_error})
                return TemplateResponse(request, self.template_name, context)

        except Exception as e:
            logging.getLogger('error_log').error("payment login execution failed  %s " % str(e))
            return HttpResponseRedirect(reverse('homepage'))

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        email = self.request.GET.get('email', '')
        context.update({
            "email_exist": False,
            'reset_form': PasswordResetRequestForm()
        })

        cart_pk = self.request.session.get('cart_pk')  # required for calling self.get_context_data()
        cart_obj = Cart.objects.get(pk=cart_pk)
        type_flow = -1

        line_item_list = cart_obj.lineitems.filter(parent=None)

        if len(line_item_list):
            line_item = line_item_list[0]
            type_flow = int(line_item.product.type_flow)
        # resume builder flow handle
        if type_flow == 17:
            cart_dict = self.get_local_cart_items(cart_obj=cart_obj)
        else:
            cart_dict = self.get_solr_cart_items(cart_obj=cart_obj)
        cart_items = cart_dict.get('cart_items', [])
        payment_dict = self.getPayableAmount(cart_obj, cart_dict.get('total_amount'))
        context.update(payment_dict)

        if cart_obj.email == email:
            context['email_exist'] = True
            context.update({'email': email, })
        return context


@Decorate(stop_browser_cache())
class PaymentShippingView(UpdateView, CartMixin):
    model = Cart
    template_name = "cart/payment-shipping.html"
    success_url = "/payment/payment-options/"
    http_method_names = [u'get', u'post']
    form_class = ShippingDetailUpdateForm

    def redirect_if_necessary(self):
        if not self.request.session.get('cart_pk'):
            self.getCartObject()
        cart_pk = self.request.session.get('cart_pk')
        if not cart_pk:
            return HttpResponseRedirect(reverse('homepage'))
        try:
            cart_obj = Cart.objects.get(pk=cart_pk)
        except Exception as e:
            logging.getLogger('error_log').error("unable to fetch cart object%s " % str(e))
            return HttpResponseRedirect(reverse('homepage'))

        if cart_obj and not (cart_obj.email or self.request.session.get('candidate_id')):
            return HttpResponseRedirect(reverse('cart:payment-login'))
        elif not cart_obj:
            return HttpResponseRedirect(reverse('homepage'))
        return None

    def get_form_kwargs(self, **kwargs):
        kwargs = super(PaymentShippingView, self).get_form_kwargs(**kwargs)
        kwargs['flavour'] = self.request.flavour
        return kwargs

    def get_object(self):
        if not self.request.session.get('cart_pk'):
            self.getCartObject()
        cart_pk = self.request.session.get('cart_pk')

        if cart_pk:
            try:
                obj = Cart.objects.get(pk=cart_pk)
            except Exception as e:
                logging.getLogger('error_log').error('unable to get cart object%s' % str(e))
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

            form.instance.email = self.request.session.get('email')
            form.instance.save()

            if not form.initial.get('mobile'):
                form.initial.update({
                    'mobile': self.request.session.get('mobile_no')})

        elif self.request.session.get('prefill_details'):
            prefill_details = self.request.session.get('prefill_details')
            social_login = self.request.session.get('key', '')
            if social_login == 'g_plus':
                name = prefill_details.get('name', '').split(" ")
                if len(name) > 1 and name[0] != "":
                    form.initial.update({'first_name': name[0], 'last_name': name[-1]})
                elif len(name) == 1:
                    form.initial.update({'first_name': name[0]})

            elif social_login == 'linkedin':
                name = prefill_details.get('name', '').split(" ")
                if len(name) > 1 and name[0] != "":
                    form.initial.update({'first_name': name[0], 'last_name': name[-1]})
                elif len(name) == 1:
                    form.initial.update({'first_name': name[0]})

            else:
                pass

        elif self.request.session.get('direct_linkedin'):
            form.initial.update({'first_name': self.request.session.get('first_name')})
            form.initial.update({'last_name': self.request.session.get('last_name')})

        if not form.initial.get('mobile'):
            form.initial.update({
                'mobile': self.request.session.get('lead_mobile')})

        if not form.initial.get('first_name'):
            form.initial.update({
                'first_name': self.request.session.get('lead_first_name')})
        if not form.initial.get('last_name'):
            form.initial.update({
                'last_name': self.request.session.get('lead_last_name')})

        if not form.initial.get('country_code'):
            form.initial.update({
                'country_code': '91'})

        if not form.initial.get('country'):
            try:
                initial_country = Country.objects.get(phone='91', active=True)
            except Exception as e:
                logging.getLogger('error_log').error('unable to get country object %s' % str(e))
                initial_country = None
            form.initial.update({
                'country': initial_country})

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()

        if form.is_valid():
            try:
                # form.data['email]' = form.initial.get('email')  # readonly
                obj = form.save(commit=False)
                obj.shipping_done = True
                if not request.session.get('candidate_id'):
                    obj.owner_id = ''
                    data = {}
                    data.update({
                        "email": obj.email,
                        "country_code": obj.country_code,
                        "cell_phone": obj.mobile,
                        "name": obj.first_name + ' ' + obj.last_name,
                    })

                    candidate_id, error = user_register(data=data)
                    obj.owner_id = candidate_id

                    if request.session.get('email'):
                        # for linkedin services
                        del request.session['email']

                elif request.session.get('candidate_id'):
                    obj.owner_id = request.session.get('candidate_id')

                if not obj.owner_id:
                    non_field_error = error
                    form._errors[NON_FIELD_ERRORS] = form.error_class([non_field_error])
                    return self.form_invalid(form)
                valid_form = self.form_valid(form)
                if obj.owner_id == request.session.get('candidate_id') and not request.ip_restricted:
                    first_name = request.session.get('first_name', '')
                    last_name = request.session.get('last_name', '')
                    name = "{}{}".format(first_name, last_name)
                    source_type = "shipping_drop_out"
                    create_lead_on_crm.apply_async(
                        (obj.pk, source_type, name),
                        countdown=settings.SHIPPING_DROP_OUT_LEAD)
                return valid_form
            except Exception as e:
                non_field_error = 'Personal detail not updated due to %s' % (str(e))
                form._errors[NON_FIELD_ERRORS] = form.error_class([non_field_error])
                logging.getLogger('error_log').error("%s " % str(e))
                return self.form_invalid(form)
        return self.form_invalid(form)


@Decorate(stop_browser_cache())
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
                # cart_dict = self.get_solr_cart_items(cart_obj=self.cart_obj)
                # if not self.cart_obj.shipping_done or not self.cart_obj.owner_id:
                #     return HttpResponseRedirect(reverse('cart:payment-shipping'))

                if not self.cart_obj.lineitems.all().exists():
                    return HttpResponseRedirect(reverse('homepage'))

            except Exception as e:
                logging.getLogger('error_log').error("%s " % str(e))
                return HttpResponseRedirect(reverse('homepage'))

        if not self.cart_obj:
            return HttpResponseRedirect(reverse('homepage'))

        return None

    def get(self, request, *args, **kwargs):
        redirect = self.redirect_if_necessary()
        if redirect:
            return redirect
        return super(self.__class__, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):

        context = super(self.__class__, self).get_context_data(**kwargs)
        cart_obj, wal_obj = self.cart_obj, None
        cart_coupon, cart_wallet = None, None
        wal_txn, wal_total, wal_point = None, None, None

        type_flow = -1

        line_item_list = cart_obj.lineitems.filter(parent=None)

        if len(line_item_list):
            line_item = line_item_list[0]
            type_flow = int(line_item.product.type_flow)
        # resume builder flow handle
        if type_flow == 17:
            cart_dict = self.get_local_cart_items(cart_obj=cart_obj)
        else:
            cart_dict = self.get_solr_cart_items(cart_obj=cart_obj)
        cart_items = cart_dict.get('cart_items', [])
        payment_dict = self.getPayableAmount(cart_obj, cart_dict.get('total_amount'))
        context.update(payment_dict)

        if cart_obj:
            wal_txn = cart_obj.wallettxn.filter(txn_type=2).order_by('-created').select_related('wallet')
            cart_coupon = cart_obj.coupon
            if cart_coupon:
                wal_obj = None
            elif wal_txn.exists():
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
                if cart_obj.owner_email:
                    wal_obj.owner_email = cart_obj.owner_email
                    wal_obj.save()
                wal_total = wal_obj.get_current_amount()
                if wal_total <= Decimal(0):
                    wal_obj = None

        context.update({
            'cart_coupon': cart_coupon, 'cart_wallet': cart_wallet, 'wallet': wal_obj,
            'cart': cart_obj, 'wallet_total': wal_total, 'wallet_point': wal_point,
            'candidate_in_session': self.request.session.get('candidate_id')})

        context.update({
            "cart_items": cart_items,
        })
        return context


class UpdateDeliveryType(View, CartMixin):
    def post(self, request, *args, **kwargs):
        cart_pk = request.session.get('cart_pk')
        data = {"total_cart_amount": -1, "delivery_charge": -1}
        if cart_pk:
            lineid = request.POST.get('lineid', None)
            delivery_type = request.POST.get('delivery_type', None)
            cart_obj = Cart.objects.get(pk=cart_pk)

            line_obj = cart_obj.lineitems.get(pk=lineid)
            delivery_servieces = line_obj.product.get_delivery_types()
            if delivery_servieces:
                delivery_obj = delivery_servieces.get(pk=delivery_type)
                line_obj.delivery_service = delivery_obj
                line_obj.save()
                type_flow = -1

                line_item_list = cart_obj.lineitems.filter(parent=None)

                if len(line_item_list):
                    line_item = line_item_list[0]
                    type_flow = int(line_item.product.type_flow)

                # resume builder flow handle
                if type_flow == 17:
                    cart_dict = self.get_local_cart_items(cart_obj=cart_obj)
                else:
                    cart_dict = self.get_solr_cart_items(cart_obj=cart_obj)
                total_cart_amount = cart_dict.get('total_amount')
                delivery_charge = delivery_obj.get_price()
                data.update({
                    "total_cart_amount": int(total_cart_amount),
                    "delivery_charge": int(delivery_charge),
                })

        return HttpResponse(json.dumps(data), content_type="application/json")
