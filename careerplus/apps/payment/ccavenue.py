# import md5
import codecs
import time
import logging

from django.conf import settings
from django.core.urlresolvers import reverse
from django.views.generic import View
from django.http import HttpResponseRedirect
from django.http import HttpResponse

from string import Template
from Crypto.Cipher import AES
from hashlib import md5

# from shinecp.cart.models import Order
from cart.models import Cart
from order.mixins import OrderMixin

from .mixin import PaymentMixin


class Ccavenue(View, PaymentMixin, OrderMixin):

    def get_constants(self):
        res_dict = {}
        res_dict['merchant_id'] = '392'
        res_dict['integration_type'] = 'iframe_normal'
        res_dict['language'] = 'EN'

        if settings.DEBUG:
            res_dict['accesscode'] = 'AVJH02BJ75AO65HJOA'
            res_dict['workingkey'] = '608D07A4DCF6EE54C142F158A107DB44'
            res_dict['url'] = 'https://secure.ccavenue.com/transaction/transaction.do?command=initiateTransaction'
        else:
            res_dict['accesscode'] = 'AVQE02BI61BL12EQLB'
            res_dict['workingkey'] = '2A4038880C818A5E64E59B6F33493D0F'
            res_dict['url'] = 'https://secure.ccavenue.com/transaction/transaction.do?command=initiateTransaction'

        return res_dict

    def default_params(self, request, cart_obj=None):
        res_dict = {}

        # current_order = order
        # currency_choice = current_order.get_currency(is_choice=1)

        # if currency_choice:
        #     res_dict['currency'] = currency_choice
        # elif request.session.get('currency'):
        #     res_dict['currency'] = request.session.get('currency')
        # else:
        #     res_dict['currency'] = 'INR'
        res_dict['currency'] = 'INR'
        return res_dict

    def pad(self, data):
        length = 16 - (len(data) % 16)
        data += chr(length) * length
        return data

    def encrypt(self, plainText, workingKey):
        iv = '\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f'
        plainText = self.pad(plainText)
        encDigest = md5()
        encDigest.update(workingKey.encode())
        enc_cipher = AES.new(encDigest.digest(), AES.MODE_CBC, iv)
        encryptedText = enc_cipher.encrypt(plainText).hex()
        return encryptedText

    def decrypt(self, cipherText, workingKey):
        iv = '\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f'
        decDigest = md5()
        decDigest.update(workingKey.encode())
        encryptedText = codecs.decode(cipherText, "hex")
        dec_cipher = AES.new(decDigest.digest(), AES.MODE_CBC, iv)
        decryptedText = dec_cipher.decrypt(encryptedText)
        return decryptedText.decode()

    def get_request_url(self, cart_obj, request, data={}):

        context_dict = {}
        context_dict.update(self.get_constants())
        context_dict.update(self.default_params(request, cart_obj))
        order_id = 'CP%d%s' % (cart_obj.pk, int(time.time()))
        # amount = round(order.amount_payable)
        amount = round(self.getTotalAmount())
        surl = "http://" + settings.SITE_DOMAIN + reverse("payment:ccavenue_response", args=("success",))
        curl = "http://" + settings.SITE_DOMAIN + reverse("payment:ccavenue_response", args=("cancel",))

        p_merchant_id = context_dict['merchant_id']
        p_currency = context_dict['currency']
        p_order_id = order_id
        p_amount = amount
        p_redirect_url = surl
        p_cancel_url = curl
        p_language = context_dict['language']
        p_merchant_param1 = str(cart_obj.pk)

        if data.get('p_payment_option') == 'ALL':
            p_payment_option = ''
        else:
            p_payment_option = data.get('p_payment_option')

        if data.get('p_card_type') == 'ALL':
            p_card_type = ''
        else:
            p_card_type = data.get('p_card_type')

        merchant_data = 'merchant_id=' + p_merchant_id + '&' + 'order_id=' + p_order_id + '&' + "currency=" + p_currency + '&' + 'amount=' + str(p_amount) + '&' + 'redirect_url=' + p_redirect_url + '&' + 'cancel_url=' + p_cancel_url + '&' + 'language=' + p_language + '&' + 'merchant_param1=' + p_merchant_param1 + '&' + 'payment_option=' + p_payment_option + '&' + 'card_type=' + p_card_type + '&'

        if cart_obj.mobile:
            p_billing_tel = cart_obj.mobile  #excluding country_code
            merchant_data += 'billing_tel=' + p_billing_tel + '&'
        elif self.request.session.get('mobile'):
            p_billing_tel = self.request.session.get('mobile')
            merchant_data += 'billing_tel=' + p_billing_tel + '&'

        if cart_obj.email:
            p_billing_email = cart_obj.email
        elif self.request.session.get('email'):
            p_billing_email = self.request.session.get('email')
        merchant_data += 'billing_email=' + p_billing_email + '&'

        encryption = self.encrypt(merchant_data, context_dict['workingkey'])
        return {'url': context_dict['url'], 'encReq': encryption, 'xscode': context_dict['accesscode']}

    def get(self, request, *args, **kwargs):
        # order creating after payemnt 
        data = {}
        cart_id = kwargs.get('order_id', None)
        paytype = kwargs.get('paytype', '')

        if cart_id and len(paytype) > 0:
            # order = Order.objects.get(id=order_id)
            cart_obj = Cart.objects.get(id=cart_id)
            self.fridge_cart(cart_obj)
            # order = self.createOrder(cart_obj)

            if paytype == "international":
                data = {'p_payment_option': 'OPTCRDC',
                        'p_card_type': 'CRDC'}
                # order.payment_mode = 7

            elif paytype == "netbanking":
                data = {'p_payment_option': 'OPTNBK', 'p_card_type': 'NBK'}
                # order.payment_mode = 10

            elif paytype == "emi":
                data = {'p_payment_option': 'OPTEMI', 'p_card_type': 'CRDC'}
                # order.payment_mode = 11

            elif paytype == "creditcard":
                data = {'p_payment_option': 'OPTCRDC', 'p_card_type': 'CRDC'}
                # order.payment_mode = 9

            elif paytype == "debit":
                data = {'p_payment_option': 'OPTDBCRD', 'p_card_type': 'DBCRD'}
                # order.payment_mode = 8

            elif paytype == "all":
                data = {'p_payment_option': 'ALL', 'p_card_type': 'ALL'}

            # order.save()

            context = self.get_request_url(cart_obj, request, data=data)

            html = '''\
                <html>
                <head>
                    <title>Sub-merchant checkout page</title>
                    <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>
                </head>
                <body>
                <form id="nonseamless" method="post" name="redirect" action="https://secure.ccavenue.com/transaction/transaction.do?command=initiateTransaction"/>
                        <input type="hidden" id="encRequest" name="encRequest" value=$encReq>
                        <input type="hidden" name="access_code" id="access_code" value=$xscode>
                        <script language='javascript'>document.redirect.submit();</script>
                </form>
                </body>
                </html>
                '''
            fin = Template(html).safe_substitute(context)
            return HttpResponse(fin)
        return HttpResponse({}, status=400)

    def post(self, request, *args, **kwargs):
        context_dict = {}
        decresp_dict = {}
        context_dict.update(self.get_constants())
        order_id = ''

        encresp = request.POST.get('encResp', None)
        stresp = kwargs.get('pgstatus', None)

        if stresp and encresp:
            decresp = self.decrypt(encresp, context_dict['workingkey'])

            for param_set in decresp.split('&'):
                params = param_set.split('=')
                param0 = '' if len(params) <= 0 else params[0]
                param1 = '' if len(params) <= 1 else params[1]
                if len(param0) <= 0:
                    continue
                decresp_dict[param0] = param1
            cart_id = decresp_dict.get('merchant_param1')
            txn_id = decresp_dict.get('order_id')
            order_status = decresp_dict.get('order_status')

            cart_obj = Cart.objects.get(pk=cart_id)

            if stresp.upper() == "SUCCESS":

                if order_status.upper() == "SUCCESS":
                    try:
                        order = self.createOrder(cart_obj)
                        return_url = self.process_payment_method(
                            order_type='CCAVENUE', request=request,
                            data={'order_id': order.pk, 'txn_id': txn_id})
                        return HttpResponseRedirect(return_url)
                    except Exception as e:
                        cart_obj = self.get_cart_last_status(cart_obj)
                        logging.getLogger('payment_log').error(str(e))
                        return HttpResponseRedirect(
                            reverse('payment:payment_oops') +
                            '?error=success&txn_id=' + txn_id)

                elif order_status.upper() == "FAILURE":
                    cart_obj = self.get_cart_last_status(cart_obj)
                    logging.getLogger('payment_log').error('Order_id - %s Order_status - %s' %(order_id, order_status))
                    return HttpResponseRedirect(reverse('payment:payment_oops') + '?error=failure&txn_id='+txn_id)

                elif order_status.upper() == "ABORTED":
                    cart_obj = self.get_cart_last_status(cart_obj)
                    logging.getLogger('payment_log').error('Order_id - %s Order_status - %s' %(order_id, order_status))
                    return HttpResponseRedirect(reverse('payment:payment_oops') + '?error=aborted&txn_id='+txn_id)

                elif order_status.upper() == "INVALID":
                    cart_obj = self.get_cart_last_status(cart_obj)
                    logging.getLogger('payment_log').error('Order_id - %s Order_status - %s' %(order_id, order_status))
                    return HttpResponseRedirect(reverse('payment:payment_oops') + '?error=invalid&txn_id='+txn_id)

            elif stresp.upper() == "CANCEL":
                cart_obj = self.get_cart_last_status(cart_obj)
                logging.getLogger('payment_log').error('Order_id - %s Order_status - %s' %(order_id, order_status))
                return HttpResponseRedirect(reverse('payment:payment_oops') + '?error=cancel&txn_id='+txn_id)

        # order_id = b64encode(str(order_id)) if order_id in (request.session.get('email_invoice_for') or []) else str(order_id)
        # payloads = '?tab=payment&error=payment_error&orderid='+order_id + '#internationalcard'
        # logging.getLogger('payment_log').error(str(request))
        cart_obj = self.get_cart_last_status(cart_obj)
        return HttpResponseRedirect(reverse('payment:payment_oops') + '?error=failure')
