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
from order.models import Order
from geolocation.models import PAYMENT_CURRENCY_SYMBOL

from .mixin import PaymentMixin
from .models import PaymentTxn

import platform
py_major, py_minor, py_patchlevel = platform.python_version_tuple()


class Ccavenue(View, PaymentMixin, OrderMixin):

    def get_constants(self):
        res_dict = {}
        res_dict['merchant_id'] = '392'
        res_dict['integration_type'] = 'iframe_normal'
        res_dict['language'] = 'EN'
        if self.request.flavour == 'mobile':
            res_dict['accesscode'] = settings.CCAVENUE_MOBILE_ACCESS_CODE
            res_dict['workingkey'] = settings.CCAVENUE_MOBILE_WORKING_KEY
        else:
            res_dict['accesscode'] = settings.CCAVENUE_ACCESS_CODE
            res_dict['workingkey'] = settings.CCAVENUE_WORKING_KEY
        res_dict['url'] = settings.CCAVENUE_URL

        # if settings.DEBUG:
        #     res_dict['accesscode'] = 'AVJH02BJ75AO65HJOA'
        #     res_dict['workingkey'] = '608D07A4DCF6EE54C142F158A107DB44'
        #     res_dict['url'] = 'https://secure.ccavenue.com/transaction/transaction.do?command=initiateTransaction'
        # else:
        #     res_dict['accesscode'] = 'AVQE02BI61BL12EQLB'
        #     res_dict['workingkey'] = '2A4038880C818A5E64E59B6F33493D0F'
        #     res_dict['url'] = 'https://secure.ccavenue.com/transaction/transaction.do?command=initiateTransaction'

        return res_dict

    def default_params(self, request, order_obj=None):
        res_dict = {}

        # current_order = order
        # currency_choice = current_order.get_currency(is_choice=1)

        # if currency_choice:
        #     res_dict['currency'] = currency_choice
        # elif request.session.get('currency'):
        #     res_dict['currency'] = request.session.get('currency')
        # else:
        #     res_dict['currency'] = 'INR'
        currency_dict = dict(PAYMENT_CURRENCY_SYMBOL)
        if currency_dict.get(order_obj.currency):
            res_dict['currency'] = currency_dict.get(order_obj.currency)
        else:
            res_dict['currency'] = 'INR'
        return res_dict

    def pad(self, data):
        length = 16 - (len(data) % 16)
        data += chr(length) * length
        return data

    def encrypt(self, plainText, workingKey):
        if py_major == '3' and py_minor == '4':
            # python 3.4
            iv = '\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f'
            plainText = self.pad(plainText)
            encDigest = md5()
            encDigest.update(workingKey.encode())
            enc_cipher = AES.new(encDigest.digest(), AES.MODE_CBC, iv)
            encryptedText = codecs.encode(enc_cipher.encrypt(plainText), "hex").decode()
            return encryptedText
        else:
            # python 3.5
            iv = '\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f'
            plainText = self.pad(plainText)
            encDigest = md5()
            encDigest.update(workingKey.encode())
            enc_cipher = AES.new(encDigest.digest(), AES.MODE_CBC, iv)
            encryptedText = enc_cipher.encrypt(plainText).hex()
            return encryptedText

    def decrypt(self, cipherText, workingKey):

        if py_major == '3' and py_minor == '4':
            # python 3.4
            iv = '\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f'
            decDigest = md5()
            decDigest.update(workingKey.encode())
            encryptedText = codecs.decode(cipherText, "hex")
            dec_cipher = AES.new(decDigest.digest(), AES.MODE_CBC, iv)
            decryptedText = dec_cipher.decrypt(encryptedText)
            return decryptedText.decode()

        else:
            # python 3.5
            iv = '\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f'
            decDigest = md5()
            decDigest.update(workingKey.encode())
            encryptedText = codecs.decode(cipherText, "hex")
            dec_cipher = AES.new(decDigest.digest(), AES.MODE_CBC, iv)
            decryptedText = dec_cipher.decrypt(encryptedText)
            return decryptedText.decode()

    def get_request_url(self, order_obj, request, data={}, pay_txn=None):
        context_dict = {}
        context_dict.update(self.get_constants())
        context_dict.update(self.default_params(request, order_obj))
        order_id = pay_txn.txn

        amount = amount = order_obj.total_incl_tax
        domain = settings.MOBILE_PROTOCOL_DOMAIN if request.is_mobile else settings.MAIN_DOMAIN_PREFIX
        surl = domain + reverse("payment:ccavenue_response", args=("success",))
        curl = domain + reverse("payment:ccavenue_response", args=("cancel",))

        p_merchant_id = context_dict['merchant_id']
        p_currency = context_dict['currency']
        p_order_id = order_id
        p_amount = amount
        p_redirect_url = surl
        p_cancel_url = curl
        p_language = context_dict['language']
        p_merchant_param1 = str(order_obj.pk)

        if data.get('p_payment_option') == 'ALL':
            p_payment_option = ''
        else:
            p_payment_option = data.get('p_payment_option')

        if data.get('p_card_type') == 'ALL':
            p_card_type = ''
        else:
            p_card_type = data.get('p_card_type')

        merchant_data = 'merchant_id=' + p_merchant_id + '&' + 'order_id=' + p_order_id + '&' + "currency=" + p_currency + '&' + 'amount=' + str(p_amount) + '&' + 'redirect_url=' + p_redirect_url + '&' + 'cancel_url=' + p_cancel_url + '&' + 'language=' + p_language + '&' + 'merchant_param1=' + p_merchant_param1 + '&' + 'payment_option=' + p_payment_option + '&' + 'card_type=' + p_card_type + '&'

        if order_obj.mobile:
            p_billing_tel = order_obj.mobile  # excluding country_code
            merchant_data += 'billing_tel=' + p_billing_tel + '&'
        elif self.request.session.get('mobile'):
            p_billing_tel = self.request.session.get('mobile_no')
            merchant_data += 'billing_tel=' + p_billing_tel + '&'

        if order_obj.email:
            p_billing_email = order_obj.email
        elif self.request.session.get('email'):
            p_billing_email = self.request.session.get('email')
        merchant_data += 'billing_email=' + p_billing_email + '&'

        encryption = self.encrypt(merchant_data, context_dict['workingkey'])
        return {'url': context_dict['url'], 'encReq': encryption, 'xscode': context_dict['accesscode']}

    def get(self, request, *args, **kwargs):
        if not request.session.get('cart_pk'):
            return HttpResponseRedirect(reverse('homepage'))
        data = {}
        cart_id = kwargs.get('cart_id', None)
        paytype = kwargs.get('paytype', '')

        if cart_id and len(paytype) > 0:
            cart_obj = Cart.objects.get(id=cart_id)
            # self.fridge_cart(cart_obj)
            order = self.createOrder(cart_obj)
            txn = 'CP%d%s' % (order.pk, int(time.time()))
            pay_txn = PaymentTxn.objects.create(
                txn=txn,
                order=order,
                cart=cart_obj,
                status=0,
                payment_mode=7,
                currency=order.currency,
                txn_amount=order.total_incl_tax,
            )

            if paytype == "international":
                data = {'p_payment_option': 'OPTCRDC',
                        'p_card_type': 'CRDC'}

            elif paytype == "netbanking":
                data = {'p_payment_option': 'OPTNBK', 'p_card_type': 'NBK'}

            elif paytype == "emi":
                data = {'p_payment_option': 'OPTEMI', 'p_card_type': 'CRDC'}

            elif paytype == "creditcard":
                data = {'p_payment_option': 'OPTCRDC', 'p_card_type': 'CRDC'}

            elif paytype == "debit":
                data = {'p_payment_option': 'OPTDBCRD', 'p_card_type': 'DBCRD'}

            elif paytype == 'upi':
                data = {'p_payment_option': 'OPTUPI', 'p_card_type': 'UPI'}

            elif paytype == "all":
                data = {'p_payment_option': 'ALL', 'p_card_type': 'ALL'}

            context = self.get_request_url(order, request, data=data, pay_txn=pay_txn)

            html = '''\
                <html>
                <head>
                    <title>Sub-merchant checkout page</title>
                    <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>
                </head>
                <body>
                <form id="nonseamless" method="post" name="redirect" action="{}"/>
                        <input type="hidden" id="encRequest" name="encRequest" value=$encReq>
                        <input type="hidden" name="access_code" id="access_code" value=$xscode>
                        <script language='javascript'>document.redirect.submit();</script>
                </form>
                </body>
                </html>
                '''.format(settings.CCAVENUE_URL)
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
            order_id = decresp_dict.get('merchant_param1')
            txn_id = decresp_dict.get('order_id')
            order_status = decresp_dict.get('order_status')
            order = Order.objects.get(pk=order_id)
            txn_obj = PaymentTxn.objects.get(txn=txn_id)
            txn_info = str(decresp_dict)
            txn_obj.txn_info = txn_info
            txn_obj.save()

            if stresp.upper() == "SUCCESS":

                if order_status.upper() == "SUCCESS":
                    try:
                        self.closeCartObject(txn_obj.cart)
                        return_url = self.process_payment_method(
                            payment_type='CCAVENUE', request=request,
                            txn_obj=txn_obj,
                            data={'order_id': order.pk, 'txn_id': txn_id})
                        try:
                            del request.session['cart_pk']
                            del request.session['checkout_type']
                            request.session.modified = True
                        except Exception as e:
                            logging.getLogger('error_log').error('unable to modify request session  %s'%str(e))
                            pass
                        return HttpResponseRedirect(return_url)
                    except Exception as e:
                        logging.getLogger('error_log').error('Response redirection for order success failed %s'%str(e))
                        return HttpResponseRedirect(
                            reverse('payment:payment_oops') +
                            '?error=success&txn_id=' + txn_id)

                elif order_status.upper() == "FAILURE":
                    txn_obj.status = 2
                    txn_obj.save()
                    logging.getLogger('error_log').error('Order_id - %s Order_status - %s' %(order_id, order_status))
                    return HttpResponseRedirect(reverse('payment:payment_oops') + '?error=failure&txn_id='+txn_id)

                elif order_status.upper() == "ABORTED":
                    txn_obj.status = 3
                    txn_obj.save()
                    logging.getLogger('error_log').error('Order_id - %s Order_status - %s' %(order_id, order_status))
                    return HttpResponseRedirect(
                        reverse('payment:payment_oops') + '?error=aborted&txn_id='+txn_id)

                elif order_status.upper() == "INVALID":
                    txn_obj.status = 4
                    txn_obj.save()
                    logging.getLogger('error_log').error('Order_id - %s Order_status - %s' %(order_id, order_status))
                    return HttpResponseRedirect(reverse('payment:payment_oops') + '?error=invalid&txn_id='+txn_id)

            elif stresp.upper() == "CANCEL":
                txn_obj.status = 5
                txn_obj.save()
                logging.getLogger('error_log').error('Order_id - %s Order_status - %s' %(order_id, order_status))
                return HttpResponseRedirect(reverse('payment:payment_oops') + '?error=cancel&txn_id='+txn_id)

        # order_id = b64encode(str(order_id)) if order_id in (request.session.get('email_invoice_for') or []) else str(order_id)
        # payloads = '?tab=payment&error=payment_error&orderid='+order_id + '#internationalcard'
        # logging.getLogger('error_log').error(str(request))
        return HttpResponseRedirect(reverse('payment:payment_oops') + '?error=failure')
