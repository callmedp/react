import urllib
import hmac
import logging
import time
import codecs

from django.core.urlresolvers import reverse
from django.views.generic import TemplateView, View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.detail import SingleObjectMixin
from django.conf import settings
from django.http import HttpResponseRedirect

from hashlib import sha256
from xml.etree.ElementTree import XML

from cart.models import Cart
from order.models import Order
from order.mixins import OrderMixin

from .mixin import PaymentMixin
from .models import PaymentTxn


import platform
py_major, py_minor, py_patchlevel = platform.python_version_tuple()


TEST_MODE = True

if TEST_MODE:
    MERCHANT_NAME = 'mobikwik'
    MOBIKWIK_MERCHANT_ID = "MBK9002"
    MOBIKWIK_SECRET_KEY = "ju6tygh7u7tdg554k098ujd5468o"
    STATUS_URL = "https://test.mobikwik.com/mobikwik/checkstatus"
    FORM_URL = "https://test.mobikwik.com/mobikwik/wallet"
else:
    MERCHANT_NAME = 'shinecom'
    MOBIKWIK_MERCHANT_ID = "MBK8137"
    MOBIKWIK_SECRET_KEY = "sWH9xkTxHk4yFWxP2LyAna6QDz3A"
    STATUS_URL = "https://www.mobikwik.com/checkstatus"
    FORM_URL = "https://www.mobikwik.com/wallet"


def remote_call(url):
    data = ""
    try:
        reqt = urllib.request.Request(url)
        response = urllib.request.urlopen(reqt)
        data = str(response.read().strip().decode())
    except Exception as e:
        logging.getLogger('error_log').error(str(e))
        print (str(e))
        pass
    return data


def send_checksum_string(orderid):
    mer_id = MOBIKWIK_MERCHANT_ID
    checksum_string = "'%s''%s'" % (mer_id, orderid)
    return checksum_string


def make_checksum(checksum_string):
    if py_major == '3' and py_minor == '4':
        # python 3.4
        sec_key = MOBIKWIK_SECRET_KEY
        hmac_obj = hmac.new(sec_key.encode(), checksum_string.encode(), sha256)
        checksum = codecs.encode(hmac_obj.digest(), "hex").decode()
        return checksum
    else:
        # python 3.5
        sec_key = MOBIKWIK_SECRET_KEY
        hmac_obj = hmac.new(sec_key.encode(), checksum_string.encode(), sha256)
        checksum = hmac_obj.digest().hex()
        return checksum


def calculate_response_checksum(statuscode, orderid, amount, statusmessage):
    if py_major == '3' and py_minor == '4':
        # python 3.4
        sec_key = MOBIKWIK_SECRET_KEY
        mer_id = MOBIKWIK_MERCHANT_ID
        checksum_string = "'%s''%s''%s''%s''%s'" % (statuscode, orderid, amount, statusmessage, mer_id)
        hmac_obj = hmac.new(sec_key.encode(), checksum_string.encode(), sha256)
        checksum = codecs.encode(hmac_obj.digest(), "hex").decode()
        return checksum
    else:
        # python 3.5
        sec_key = MOBIKWIK_SECRET_KEY
        mer_id = MOBIKWIK_MERCHANT_ID
        checksum_string = "'%s''%s''%s''%s''%s'" % (statuscode, orderid, amount, statusmessage, mer_id)
        hmac_obj = hmac.new(sec_key.encode(), checksum_string.encode(), sha256)
        checksum = hmac_obj.digest().hex()
        return checksum


class MobikwikRequestView(SingleObjectMixin, TemplateView, OrderMixin):
    template_name = 'payment/mobikwik_wallet.html'

    def get(self, request, *args, **kwargs):
        if not request.session.get('cart_pk'):
            return HttpResponseRedirect(reverse('homepage'))
        return super(self.__class__, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        cart_pk = self.request.session.get('cart_pk')
        cart_obj = Cart.objects.get(pk=cart_pk)
        # self.fridge_cart(cart_obj)
        order_obj = self.createOrder(cart_obj)
        self.object = order_obj
        txn = 'MK%d_%d' % (order_obj.pk, int(time.time()))
        pay_txn = PaymentTxn.objects.create(
            txn=txn,
            order=order_obj,
            cart=cart_obj,
            status=0,
            payment_mode=6,
            currency=order_obj.currency,
            txn_amount=order_obj.total_incl_tax,
        )
        user_email = order_obj.email

        if order_obj.mobile:
            user_mobile = order_obj.mobile  #excluding country code
        elif self.request.session.get('mobile_no'):
            user_mobile = self.request.session.get('mobile_no')
        else:
            user_mobile = ""

        order_amount = "%.2f" % order_obj.total_incl_tax
        txn_id = pay_txn.txn
        context = super(self.__class__, self).get_context_data(**kwargs)

        return_url = "http://" + settings.SITE_DOMAIN + reverse("payment:mobikwik_response")

        ch_string = "'%s''%s''%s''%s''%s''%s'" % (user_mobile, user_email, order_amount, txn_id, return_url, MOBIKWIK_MERCHANT_ID)
        checksum = make_checksum(ch_string)

        context['params'] = {
            'email': user_email,
            'redirecturl': return_url,
            'mid': MOBIKWIK_MERCHANT_ID,
            'amount': order_amount,
            'cell': user_mobile,
            'orderid': txn_id,
            'form_url': FORM_URL,
            "checksum": checksum,
        }

        return context


class MobikwikResponseView(View, PaymentMixin, OrderMixin):

    def post(self, request, *args, **kwargs):
        err_mesg = None
        orderid = request.POST.get('orderid', '')
        checksum = request.POST.get('checksum', '')
        mid = request.POST.get('mid', '')
        amount = request.POST.get('amount', '')
        statusmessage = request.POST.get('statusmessage', '')
        statuscode = request.POST.get('statuscode', '')

        # cart_pk = request.session.get('cart_pk')
        txn = orderid
        order_pk = orderid.split('_')[0]
        order_pk = order_pk.replace('MK', '')
        order_obj = Order.objects.get(pk=order_pk)
        txn_obj = PaymentTxn.objects.get(txn=txn)
        response_checksum = calculate_response_checksum(statuscode, orderid, amount, statusmessage)

        if response_checksum == checksum and order_obj:
            if str(statuscode) == "0":
                order_id = order_pk
                actual_amount = "%.2f" % order_obj.total_incl_tax

                if str(order_id) != str(order_obj.pk):
                    err_mesg = "Original orderid # %s and actual orderid # %s do not match" % (str(order_obj.pk), order_id)

                elif float(actual_amount) == float(amount):
                    csumstring = send_checksum_string(orderid)
                    sndchecksum = make_checksum(csumstring)
                    status_url = STATUS_URL + "?mid=%s&checksum=%s&orderid=%s" % (mid, sndchecksum, orderid)
                    data = remote_call(status_url)
                    try:
                        tree = XML(data)
                        try:
                            amount2 = tree.find('.//amount').text
                        except Exception as e:
                            err_mesg = "amount not found"
                            logging.getLogger('error_log').error(str(e))
                        try:
                            statuscode2 = tree.find('.//statuscode').text
                        except Exception as e:
                            logging.getLogger('error_log').error(str(e))
                            err_mesg = "statuscode not found"
                        try:
                            orderid2 = tree.find('.//orderid').text
                        except Exception as e:
                            logging.getLogger('error_log').error(str(e))
                            err_mesg = "orderid not found"
                        try:
                            refid2 = tree.find('.//refid').text
                        except Exception as e:
                            logging.getLogger('error_log').error(str(e))

                            err_mesg = "refid not found"
                        try:
                            statusmessage2 = tree.find('.//statusmessage').text
                        except Exception as e:
                            err_mesg = "statusmessage not found"
                        try:
                            ordertype2 = tree.find('.//ordertype').text
                        except Exception as e:
                            logging.getLogger('error_log').error(str(e))
                            err_mesg = "ordertype not found"
                        try:
                            checksum2 = tree.find('.//checksum').text
                        except Exception as e:
                            logging.getLogger('error_log').error(str(e))
                            err_mesg = "checksum not found"

                        if not err_mesg and str(statuscode2) == "0":
                            ckstring2 = "'%s''%s''%s''%s''%s''%s'" % (statuscode2, orderid2, refid2, amount2, statusmessage2, ordertype2)
                            cksum2 = make_checksum(ckstring2)

                            if cksum2 == checksum2 and float(amount2) == float(actual_amount) and orderid2 == orderid:
                                try:
                                    self.closeCartObject(txn_obj.cart)
                                    return_url = self.process_payment_method(payment_type='MOBIKWIK', request=request, txn_obj=txn_obj, data={'order_id': order_obj.pk, 'txn_id': refid2})
                                    try:
                                        del request.session['cart_pk']
                                        del request.session['checkout_type']
                                        request.session.modified = True
                                    except Exception as e:
                                        logging.getLogger('error_log').error(str(e))
                                        pass
                                    return HttpResponseRedirect(return_url)
                                except Exception as e:
                                    logging.getLogger('error_log').error(str(e))
                                    return HttpResponseRedirect(reverse('payment:payment_oops')+'?error=success&txn_id='+txn)
                            else:
                                err_mesg = "Fraud Detected for order id - %s" % orderid
                        else:
                            if not err_mesg:
                                err_mesg = "Transaction failed because of reason = " + statusmessage2
                    except Exception as e:
                        logging.getLogger('error_log').error(str(e))
                        err_mesg = "Error Occur = %s" % e
                else:
                    err_mesg = "Txn Failed for order id - %s" % orderid
            else:
                err_mesg = "Txn Failed Because of reason : " + statusmessage
        else:
            err_mesg = str(request.POST)

        logging.getLogger('error_log').error(err_mesg)
        return HttpResponseRedirect(reverse('payment:payment_oops') + '?error=failure')

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        cart_pk = self.request.session.get('cart_pk')
        if not cart_pk:
            return HttpResponseRedirect(reverse('cart:payment-summary'))
        return super(self.__class__, self).dispatch(*args, **kwargs)
