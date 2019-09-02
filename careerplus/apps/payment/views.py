#python imports
import os
import ast
import json
import time
import logging
import mimetypes
from random import random
from datetime import datetime

#django imports
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect
from django.urls import reverse
from django.conf import settings
from django.shortcuts import render
from django.conf import settings
from cart.models import Cart
from order.mixins import OrderMixin
from order.models import Order
from console.decorators import Decorate, stop_browser_cache
from django.core.files.base import ContentFile
from django.utils import timezone
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect


#local imports
from core.api_mixin import ShineCandidateDetail
from .models import PaymentTxn
from .mixin import PaymentMixin
from .forms import StateForm, PayByCheckForm
from .utils import EpayLaterEncryptDecryptUtil
from .tasks import put_epay_for_successful_payment

#inter app imports
from cart.models import Cart
from order.models import Order
from cart.mixins import CartMixin
from order.mixins import OrderMixin
from cart.tasks import create_lead_on_crm
from core.api_mixin import ShineCandidateDetail
from dashboard.dashboard_mixin import DashboardInfo
from console.decorators import Decorate, stop_browser_cache
from core.utils import get_client_ip,get_client_device_type
from core.library.gcloud.custom_cloud_storage import GCPPrivateMediaStorage

# third party imports


@Decorate(stop_browser_cache())
class PaymentOptionView(TemplateView, OrderMixin, PaymentMixin):
    template_name = "payment/payment-option.html"

    def __init__(self):
        self.cart_obj = None

    def redirect_if_necessary(self):
        if not self.request.session.get('cart_pk'):
            self.cart_obj = self.getCartObject()
        else:
            cart_pk = self.request.session.get('cart_pk')
            if not cart_pk:
                return HttpResponsePermanentRedirect(reverse('homepage'))
            try:
                self.cart_obj = Cart.objects.get(pk=cart_pk)
                if not self.cart_obj.shipping_done or not self.cart_obj.owner_id:
                    return HttpResponsePermanentRedirect(reverse('cart:payment-shipping'))
            except Exception as e:
                logging.getLogger('error_log').error('unable to get cart object%s'%str(e))
                return HttpResponsePermanentRedirect(reverse('homepage'))
        if self.cart_obj and not (self.cart_obj.shipping_done):
            return HttpResponsePermanentRedirect(reverse('cart:payment-login'))

        elif not self.cart_obj:
            return HttpResponsePermanentRedirect(reverse('homepage'))
        elif self.cart_obj and not self.cart_obj.lineitems.filter(no_process=False).exists():
            return HttpResponsePermanentRedirect(reverse('homepage'))
        return None

    def get(self, request, *args, **kwargs):
        redirect = self.redirect_if_necessary()
        try:
            self.cart_obj.payment_page = True
            self.cart_obj.save()
        except Exception as e:
            logging.getLogger('error_log').error("unable to save cart object%s" % str(e))

        if redirect:
            return redirect

        payment_dict = self.getPayableAmount(cart_obj=self.cart_obj)
        source_type = "payment_drop_out"
        candidate_id = request.session.get('candidate_id')
        if self.cart_obj.owner_id == candidate_id and not request.ip_restricted:
            first_name = request.session.get('first_name', '')
            last_name = request.session.get('last_name', '')
            name = "{}{}".format(first_name, last_name)
            create_lead_on_crm.apply_async(
                (self.cart_obj.pk, source_type, name),
                countdown=settings.PAYMENT_DROP_LEAD)
        total_payable_amount = payment_dict.get('total_payable_amount')
        if total_payable_amount <= 0:
            order = self.createOrder(self.cart_obj)
            self.closeCartObject(self.cart_obj)
            if order:
                txn = 'CP%d%s' % (order.pk, int(time.time()))
                pay_txn = PaymentTxn.objects.create(
                    txn=txn,
                    order=order,
                    cart=self.cart_obj,
                    status=0,
                    payment_mode=11,
                    currency=order.currency,
                    txn_amount=order.total_incl_tax,
                )
                payment_type = "PAID FREE"
                return_parameter = self.process_payment_method(
                    payment_type, request, pay_txn)
                try:
                    del request.session['cart_pk']
                    del request.session['checkout_type']
                    request.session.modified = True
                except Exception as e:
                    logging.getLogger('error_log').error('unable to delete request session objects%s'%str(e))
                    pass
                return HttpResponseRedirect(return_parameter)

        return super(PaymentOptionView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        payment_type = request.POST.get('payment_type', '').strip()
        if payment_type == 'cash':
            form = StateForm(request.POST)
            if form.is_valid():
                cart_pk = request.session.get('cart_pk')
                if cart_pk:
                    cart_obj = Cart.objects.get(pk=cart_pk)
                    order = self.createOrder(cart_obj)
                    self.closeCartObject(cart_obj)
                    if order:
                        txn = 'CP%d%s' % (order.pk, int(time.time()))
                        pay_txn = PaymentTxn.objects.create(
                            txn=txn,
                            order=order,
                            cart=cart_obj,
                            status=0,
                            payment_mode=1,
                            currency=order.currency,
                            txn_amount=order.total_incl_tax,
                        )
                        payment_type = "CASH"
                        return_parameter = self.process_payment_method(
                            payment_type, request, pay_txn)
                        try:
                            del request.session['cart_pk']
                            del request.session['checkout_type']
                            request.session.modified = True
                        except Exception as e:

                            logging.getLogger('error_log').error('unable to delete session request object%s'%str(e))
                            pass
                        return HttpResponseRedirect(return_parameter)
                else:
                    return HttpResponseRedirect(reverse('homepage'))
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
                    order = self.createOrder(cart_obj)
                    self.closeCartObject(cart_obj)
                    if order:
                        txn = 'CP%d%s%s' % (
                            order.pk,
                            int(time.time()),
                            request.POST.get('cheque_no'))
                        pay_txn = PaymentTxn.objects.create(
                            txn=txn,
                            order=order,
                            cart=cart_obj,
                            status=0,
                            payment_mode=4,
                            currency=order.currency,
                            txn_amount=order.total_incl_tax,
                            instrument_number=request.POST.get('cheque_no'),
                            instrument_issuer=request.POST.get('drawn_bank'),
                            instrument_issue_date=request.POST.get('deposit_date')
                        )
                        payment_type = "CHEQUE"
                        return_parameter = self.process_payment_method(
                            payment_type, request, pay_txn)
                        try:
                            del request.session['cart_pk']
                            del request.session['checkout_type']
                            request.session.modified = True
                        except Exception as e:
                            logging.getLogger('error_log').error('unable to delete request session object%s'%str(e))
                            pass
                        return HttpResponseRedirect(return_parameter)
                else:
                    return HttpResponseRedirect(reverse('homepage'))
            else:
                context = self.get_context_data()
                context['check_form'] = form
                return render(request, self.template_name, context)

        return HttpResponseRedirect(reverse('cart:cart-product-list'))

    def get_context_data(self, **kwargs):
        context = super(PaymentOptionView, self).get_context_data(**kwargs)
        payment_dict = self.getPayableAmount(cart_obj=self.cart_obj)
        line_item = self.cart_obj.lineitems.filter(parent=None)[0]
        type_flow = int(line_item.product.type_flow)
        print(type_flow)
        context.update({
            "state_form": StateForm(),
            "check_form": PayByCheckForm(),
            "total_amount": payment_dict.get('total_payable_amount'),
            "cart_id": self.request.session.get('cart_pk'),
            "type_flow": type_flow

        })
        return context


@Decorate(stop_browser_cache())
class ThankYouView(TemplateView):
    template_name = "payment/thank-you.html"

    def get(self, request, *args, **kwargs):
        if self.request.session.get('order_pk'):
            return super(ThankYouView, self).get(request, *args, **kwargs)
        return HttpResponseRedirect(reverse('homepage'))

    def get_context_data(self, **kwargs):
        context = super(ThankYouView, self).get_context_data(**kwargs)
        order_pk = self.request.session.get('order_pk')
        if not order_pk:
            return
        order = Order.objects.filter(pk=order_pk).first()
        if not order:
            return
        order_items = []
        parent_ois = order.orderitems.filter(parent=None).select_related('product', 'partner')
        for p_oi in parent_ois:
            data = {}
            data['oi'] = p_oi
            data['addons'] = order.orderitems.filter(
                parent=p_oi,
                is_addon=True).select_related('product', 'partner')
            data['variations'] = order.orderitems.filter(
                parent=p_oi,
                is_variation=True).select_related('product', 'partner')
            order_items.append(data)
        context.update({
            'orderitems': order_items,
            'order': order})

        pending_resume_items = order.orderitems.filter(
            order__status__in=[0, 1],
            no_process=False, oi_status=2)

        assesment_items = order.orderitems.filter(
            order__status__in=[0],
            product__type_flow=16,
            product__sub_type_flow=1602
        )
        booster_item_exist = True if order.orderitems.filter(   #for single booster element in order
                                    order__status__in=[0, 1],
                                    product__type_flow__in=[7,15],
                                    no_process=False,oi_status=2).count()\
                            else False

        context.update({
            "pending_resume_items": pending_resume_items,
            "assesment_items": assesment_items,
            'booster_item_exist':booster_item_exist
        })

        if not self.request.session.get('resume_id', None):
            DashboardInfo().check_user_shine_resume(
                candidate_id=self.request.session.get('candidate_id'),
                request=self.request)
        return context

    def post(self, request, *args, **kwargs):
        action_type = request.POST.get('action_type', '').strip()
        order_pk = request.session.get('order_pk')
        resume_id = request.session.get('resume_id', None)
        candidate_id = request.session.get('candidate_id', None)
        order = Order.objects.filter(pk=order_pk).first()
        if not order:
            return
        order_item_ids =list(order.orderitems.all().values_list('id',flat=True))
        file = request.FILES.get('resume_file', '')

        if action_type == 'upload_resume' and order_pk and file:
            data = {
                        "list_ids": order_item_ids,
                        "candidate_resume": file,
                        'last_oi_status': 3,
                    }
            DashboardInfo().upload_candidate_resume(candidate_id=candidate_id, data=data)

        elif action_type == "shine_reusme" and order_pk and candidate_id and resume_id:
            response = ShineCandidateDetail().get_shine_candidate_resume(
                candidate_id=candidate_id,
                resume_id=request.session.get('resume_id'))
            if not response:
                request.session.pop('resume_id')
                DashboardInfo().check_user_shine_resume(candidate_id=candidate_id,request=request)
                response = ShineCandidateDetail().get_shine_candidate_resume(
                                                    candidate_id=candidate_id,
                                                    resume_id=request.session.get('resume_id'))
            if response.status_code == 200:
                file = ContentFile(response.content)
                data = {
                        "list_ids": order_item_ids,
                        "candidate_resume": file,
                        'last_oi_status': 13,
                        'is_shine':True,
                        'extension':request.session.get('resume_extn', '')
                    }
                DashboardInfo().upload_candidate_resume(candidate_id=candidate_id, data=data)

        return HttpResponseRedirect(reverse('payment:thank-you'))


@Decorate(stop_browser_cache())
class PaymentOopsView(TemplateView):
    template_name = 'payment/payment-oops.html'

    def get(self, request, *args, **kwargs):
        return super(PaymentOopsView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        error_type = self.request.GET.get('error', '')
        txn_id = self.request.GET.get('txn_id', '')
        context = super(PaymentOopsView, self).get_context_data(**kwargs)
        context.update({'error_type': error_type, 'txn_id': txn_id})
        context.update({'is_payment': True, })
        return context


class EPayLaterRequestView(OrderMixin,TemplateView):
    template_name = "payment/epaylater_submission_form.html"

    def _get_order_history_list(self,order):
        order_history = []

        for past_order in order.get_past_orders_for_email_and_mobile():
            past_txn = past_order.ordertxns.filter(status=1).first()
            if not past_txn:
                continue
            order_data = {"orderId":past_txn.txn,"amount":float(past_order.total_incl_tax),
                "currencyCode":past_order.get_currency_code(),
                "date":past_order.payment_date.isoformat().split("+")[0].split(".")[0]+"Z",
                "category": settings.EPAYLATER_INFO['category'],
                "returned": "false","paymentMethod":past_txn.get_payment_mode()}
            order_history.append(order_data)

        return order_history

    def get_context_data(self,**kwargs):
        cart_id = kwargs.get('cart_id',0)
        cart_obj = Cart.objects.filter(id=cart_id).first()
        if not cart_obj:
            return HttpResponseRedirect("/")

        site_domain = settings.SITE_DOMAIN
        if self.request.flavour == 'mobile':
            site_domain = settings.MOBILE_SITE_DOMAIN

        order = self.createOrder(cart_obj)
        txn_id = 'CP%d%s' % (order.pk, int(time.time()))
        pay_txn = PaymentTxn.objects.create(
            txn=txn_id,order=order,
            cart=cart_obj,status=0,
            payment_mode=11,currency=order.currency,
            txn_amount=order.total_incl_tax,
            )

        current_utc_string = datetime.utcnow().isoformat().split(".")[0] + "Z"
        initial_dict = {
            "redirectType": "WEBPAGE","marketplaceOrderId": txn_id,
            "mCode": settings.EPAYLATER_INFO.get('mCode'),
            "callbackUrl": "{}://{}/payment/epaylater/response/{}/".format(\
                settings.SITE_PROTOCOL,site_domain,cart_id),
            "customerEmailVerified": False,"customerTelephoneNumberVerified": False,
            "customerLoggedin": True,"amount": float(order.total_incl_tax*100),
            "currencyCode": order.get_currency_code(),
            "date": current_utc_string,"category": settings.EPAYLATER_INFO['category']}

        customer_data = {"firstName": order.first_name,"lastName": order.last_name,
            "emailAddress":order.email,"telephoneNumber":order.mobile}

        device_data = {"deviceType": get_client_device_type(self.request),
            "deviceClient": self.request.META.get('HTTP_USER_AGENT',''),
            "deviceNumber": get_client_ip(self.request)}

        market_data = {"marketplaceCustomerId":order.email,
            "memberSince":order.get_first_touch_for_email().\
                isoformat().split("+")[0].split(".")[0] + "Z"}

        initial_dict.update({"customer":customer_data,"device":device_data,
            "orderHistory":self._get_order_history_list(order),
            "marketplaceSpecificSection":market_data})

        # generate checksum and encdata for form submission
        epay_encdec_obj = EpayLaterEncryptDecryptUtil(settings.EPAYLATER_INFO['aeskey'],\
            settings.EPAYLATER_INFO['iv'])
        checksum = epay_encdec_obj.checksum(json.dumps(initial_dict).encode('utf-8'))
        encdata = epay_encdec_obj.encrypt(json.dumps(initial_dict).encode('utf-8'))

        template_context = {"action":settings.EPAYLATER_INFO['payment_url'],
                    "mcode":settings.EPAYLATER_INFO['mCode'],
                    "checksum":checksum,"encdata":encdata}
        return template_context


class EPayLaterResponseView(PaymentMixin,CartMixin,TemplateView):

    def get(self,request,*args,**kwargs):
        return HttpResponseNotAllowed()

    def _extract_json_from_string(self,dec_data):
        start_index = dec_data.find("{")
        end_index = dec_data.rfind("}")
        decrypted_text = dec_data[start_index:end_index+1]
        decrypted_text = decrypted_text.replace("null","\"\"")
        return ast.literal_eval(decrypted_text)

    def _handle_successful_transaction(self,txn_obj,txn_id,order):
        self.closeCartObject(txn_obj.cart)
        return_url = self.process_payment_method(
            payment_type='EPAYLATER', request=self.request,
            txn_obj=txn_obj,data={'order_id': order.pk, 'txn_id': txn_id})
        try:
            del self.request.session['cart_pk']
            del self.request.session['checkout_type']
            self.request.session.modified = True
        except Exception as e:
            logging.getLogger('error_log').error('unable to modify request session  %s'%str(e))
        return return_url

    def _handle_failed_transaction(self,txn_obj,failure_message):
        txn_obj.txn_status = 2
        txn_obj.txn_info = failure_message
        logging.getLogger('error_log').error('EPAYLATER failed for {}'.format(txn_obj.txn))
        txn_obj.save()

    def post(self,request,*args,**kwargs):
        paylater_data = request.POST.copy()
        checksum = paylater_data.get('checksum')
        encdata = paylater_data.get('encdata')
        epay_encdec_obj = EpayLaterEncryptDecryptUtil(settings.EPAYLATER_INFO['aeskey'],\
            settings.EPAYLATER_INFO['iv'])
        decrypted_data = epay_encdec_obj.decrypt(encdata)
        inferred_checksum = epay_encdec_obj.checksum(decrypted_data.encode('utf-8'))

        if checksum != inferred_checksum:
            logging.getLogger('error_log').error("PayLater Checksum failure - {}".format(decrypted_data))
            return HttpResponseRedirect(reverse('payment:payment_oops') + '?error=failure&txn_id='+txn_id)

        decrypted_data = self._extract_json_from_string(decrypted_data)
        transaction_status = decrypted_data.get('status','').upper()
        txn_id = decrypted_data.get('marketplaceOrderId')
        order_id = decrypted_data.get('eplOrderId')

        if not txn_id:
            logging.getLogger('error_log').error("PayLater No txn id - {}".format(decrypted_data))
            return HttpResponseRedirect(reverse('payment:payment_oops') + '?error=failure&txn_id='+txn_id)

        txn_obj = PaymentTxn.objects.filter(txn=txn_id).first()
        if not txn_obj:
            logging.getLogger('error_log').error("PayLater No txn obj - {}".format(decrypted_data))
            return HttpResponseRedirect(reverse('payment:payment_oops') + '?error=failure&txn_id='+txn_id)

        order = txn_obj.order

        if transaction_status == "SUCCESS":

            if txn_obj.status == 1:
                logging.getLogger('info_log').info('EPAY - Updating successful transaction {}'.format(txn_id))
                put_epay_for_successful_payment.delay(order_id,txn_id)
                return HttpResponseRedirect(reverse('payment:thank-you'))

            return_url = self._handle_successful_transaction(txn_obj,txn_id,order)
            put_epay_for_successful_payment.delay(order_id,txn_id)
            return HttpResponseRedirect(return_url)

        else:
            self._handle_failed_transaction(txn_obj,decrypted_data.get('statusDesc'))
            return HttpResponseRedirect(reverse('payment:payment_oops') + '?error=failure&txn_id='+txn_id)




