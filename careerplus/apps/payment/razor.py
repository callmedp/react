import hmac
import hashlib
import sys
import requests
import json
from django.conf import settings


class RazorPaymentUtil:
    BASE_URL = 'https://api.razorpay.com/v1'
    ORDER_URL = "/orders"
    INVOICE_URL = "/invoices"
    PAYMENTS_URL = "/payments"
    REFUNDS_URL = "/refunds"
    CARD_URL = "/cards"
    CUSTOMER_URL = "/customers"
    TRANSFER_URL = "/transfers"
    VIRTUAL_ACCOUNT_URL = "/virtual_accounts"
    SUBSCRIPTION_URL = "/subscriptions"
    ADDON_URL = "/addons"
    PLAN_URL = "/plans"
    FETCH_PAYMENT = "/orders/{}/payments"


    def create(self,order,pay_txn):

        response = None
        
        data ={ 'amount':int(order.total_incl_tax *100),
                'currency':'INR',
                'receipt': pay_txn.txn,
                'notes': {'product_name': order.get_product_name()}
               }

        #payment capture should always be 1
        data.update({'payment_capture':'1'})

        data = json.dumps(data)
        headers = {'Content-type': 'application/json'}
        auth=(settings.RAZOR_PAY_DICT.get('key_id'), settings.RAZOR_PAY_DICT.get('key_secret'))
        try:
            response = requests.post(self.BASE_URL+self.ORDER_URL, data=data,headers=headers,auth=auth)
        except:
            response = None
        if not response:
            return {}
        return response.json()



    def verify_payment(self,parameters):

        order_id = str(parameters['razorpay_order_id'])
        payment_id = str(parameters['razorpay_payment_id'])
        razorpay_signature = str(parameters['razorpay_signature'])
        msg = "{}|{}".format(order_id, payment_id)
        secret = settings.RAZOR_PAY_DICT.get('key_secret')
        return self.verify_signature(msg, razorpay_signature, secret)


    def verify_signature(self, body, signature, key):
        if sys.version_info[0] == 3:  # pragma: no cover
            key = bytes(key, 'utf-8')
            body = bytes(body, 'utf-8')

        dig = hmac.new(key=key,
                       msg=body,
                       digestmod=hashlib.sha256)

        generated_signature = dig.hexdigest()

        if sys.version_info[0:3] < (2, 7, 7):
            result = self.compare_string(generated_signature, signature)
        else:
            result = hmac.compare_digest(generated_signature, signature)
        return result


    def compare_string(self, expected_str, actual_str):
        """
        Returns True if the two strings are equal, False otherwise
        The time taken is independent of the number of characters that match
        For the sake of simplicity, this function executes in constant time only
        when the two strings have the same length. It short-circuits when they
        have different lengths
        """
        if len(expected_str) != len(actual_str):
            return False
        result = 0
        for x, y in zip(expected_str, actual_str):
            result |= ord(x) ^ ord(y)
        return result == 0


    def fetch_payment(self,order_id):
        if not order_id:
            return
        headers = {'Content-type': 'application/json'}
        auth=(settings.RAZOR_PAY_DICT.get('key_id'), settings.RAZOR_PAY_DICT.get('key_secret'))
        try:
            response = requests.get(self.BASE_URL+self.FETCH_PAYMENT.format(order_id) ,headers=headers,auth=auth)
        except:
            response = None

        return response







    # def all(self, data={}, **kwargs):
    #     """"
    #     Fetch all Order entities
    #     Returns:
    #         Dictionary of Order data
    #     """
    #     return super(Order, self).all(data, **kwargs)
    #
    # def fetch(self, order_id, data={}, **kwargs):
    #     """"
    #     Fetch Order for given Id
    #     Args:
    #         order_id : Id for which order object has to be retrieved
    #     Returns:
    #         Order dict for given order Id
    #     """
    #     return super(Order, self).fetch(order_id, data, **kwargs)
    #
    # def fetch_all_payments(self, order_id, data={}, **kwargs):  # pragma: no cover
    #     warnings.warn("Will be Deprecated in next release, use payments",
    #                   DeprecationWarning)
    #     return self.payments(order_id, data, **kwargs)
    #
    # def payments(self, order_id, data={}, **kwargs):
    #     """"
    #     Fetch Payment for Order Id
    #     Args:
    #         order_id : Id for which payment objects has to be retrieved
    #     Returns:
    #         Payment dict for given Order Id
    #     """
    #     url = "{}/{}/payments".format(self.base_url, order_id)
    #     return self.get_url(url, data, **kwargs)
    #
