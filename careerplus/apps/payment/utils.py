# python imports
import base64
from hashlib import sha256,sha512
import requests
import logging, json, copy,math
import hmac
import logging
from datetime import datetime



# django imports
from django.conf import settings
from django.core.cache import cache
# local imports

# inter app imports
from api.config import LOCATION_MAPPING, DEGREE_MAPPING
from core.api_mixin import ShineCandidateDetail

# third party imports
from Crypto.Cipher import AES

class EpayLaterEncryptDecryptUtil(object):

    def __init__(self, key, iv):
        self.bs = 16
        self.key = key
        self.iv = iv

    def checksum(self, raw):
        return sha256(raw).hexdigest().upper()

    def encrypt(self, raw):
        raw = self._pad(raw)
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        return base64.b64encode(cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        return self._unpad(cipher.decrypt(enc)).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s)
                                                      %self.bs).encode('utf-8')

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]


def update_auto_login_url_for_assesment(orderitem, data):
    from core.api_mixin import AmcatApiMixin
    autologin_url = AmcatApiMixin().get_auto_login_url(data)
    if autologin_url:
        orderitem.autologin_url = autologin_url
        orderitem.save()
        return True
    else:
        logging.getLogger('error_log').error(
            "Failed fetching autologin for Order item:- %s"
        )
        return False


def manually_generate_autologin_url(assesment_items=[]):
    for oi in assesment_items:
        candidate_id = oi.order.candidate_id
        status_response = ShineCandidateDetail().get_status_detail(
            email=None, shine_id=candidate_id
        )
        skill_id = oi.product.new_productskills.filter(primary=True).first()
        if skill_id:
            skill_id = skill_id.third_party_skill_id
        if not oi.autologin_url and skill_id:
            candidate_location = status_response.get('candidate_location', 'N.A')
            if candidate_location != 'N.A':
                candidate_location = LOCATION_MAPPING.get(candidate_location, 'N.A')
            candidate_degree = status_response.get('highest_education', 'N.A')
            if candidate_degree != 'N.A':
                candidate_degree = DEGREE_MAPPING.get(candidate_degree, 'N.A')
            candidate_mobile = "{}{}".format(
                status_response.get('country_code', '91'),
                oi.order.mobile
            )
            data = {
                "candidate_email": oi.order.email,
                "skill_id": str(skill_id),
                "candidate_phone": candidate_mobile,
                "candidate_name": oi.order.first_name if oi.order.first_name else "No Name",
                "candidate_city": candidate_location,
                "candidate_degree": candidate_degree,
                "shine_learning_order_id": str(oi.id)
            }
            update_auto_login_url_for_assesment(oi, data)


class ZestMoneyUtil:
    """
    Refer - http://docs.zestmoney.in/docs/1-getting-started-with-zestmoney
    Password - 6de9cb13a0528

    OTP generation API -
    https://staging-instore.zestmoney.in/TestFolder/otp.php?contact=<contact_no>
    Has to be done explicitly on staging servers.
    """

    def __init__(self, **kwargs):
        self.zestmoney_dict = copy.deepcopy(settings.ZESTMONEY_INFO)

    def fetch_token_dict(self):
        cached_key = cache.get('zestmoney_token')
        if cached_key:
            return cached_key

        end_point = "{}/{}".format(
            self.zestmoney_dict.get('authentication_base_url'),
            "connect/token")

        data = {
            "client_id"    : self.zestmoney_dict.get('client_id'),
            "client_secret": self.zestmoney_dict.get('client_secret'),
            "grant_type"   : "client_credentials",
            "scope"        : "merchant_api_sensitive"
        }

        try:
            response = requests.post(end_point, data)
        except Exception as e:
            logging.getLogger('error_log').error(
                "Unable to extract authentication token, {}".format(e))
            return {}

        if response.status_code == 200:
            json_response = response.json()
            cache.set('zestmoney_token', json_response, 60 * 50)
            return json_response

        logging.getLogger('error_log').error(
            "Unable to extract authentication token, {}".format(response.text))
        return {}

    def get_authorization_header(self):
        token_dict = self.fetch_token_dict()
        headers = {"Authorization": "{} {}".format( \
            token_dict.get('token_type'), token_dict.get('access_token'))
        }

        return headers

    def get_customer_redirect_url(self, txn_obj):
        txn_order = txn_obj.order
        return_url = "{}/payment/zestmoney/response/?txnid={}".format(
            settings.SITE_DOMAIN, txn_obj.txn)
        end_point = "{}/{}".format(self.zestmoney_dict.get('api_base_url'),
                                    "preapprove/merchantCustomer/redirect")

        get_params_str = "mid={}&mcid={}&ru={}&em={}&mn={}".format( \
            self.zestmoney_dict['client_id'],
            txn_order.email.lower().strip(), \
            return_url, txn_order.email.lower().strip(),
            txn_order.mobile.strip())

        return '{}?{}'.format(end_point, get_params_str)

    def fetch_user_credit_limit(self, email, mobile_no):
        headers = self.get_authorization_header()
        headers.update(
            {"Accept": "application/json", "Content-Type": "application/json"})
        end_point = "{}/{}".format(self.zestmoney_dict.get('api_base_url'),
                                    "preapprove/user/details")

        data = {
            "emailAddress": email,
            "mobileNumber": mobile_no,
            "customerId"  : ""
        }

        try:
            response = requests.post(end_point, data=json.dumps(data),
                                      headers=headers)
        except Exception as e:
            logging.getLogger("info_log").info("requests ERROR :: \
                Unable to fetch user credit limit {}".format(e))
            return {}

        if response.status_code == 201:
            json_response = response.json()
            zest_payment_keys_mapping = {"approvedAmt" : "approved",
                                         "availableAmt": "available"
                                         }

            mapped_response_data = {
            zest_payment_keys_mapping[key]: json_response.get(key) \
            for key in json_response.keys() if
            zest_payment_keys_mapping.get(key)}

            return mapped_response_data

        logging.getLogger("info_log").info(
            "Unable to fetch user credit limit {}".format( \
                response.status_code, response.text))
        return {}

    def get_emi_plans(self, amount):
        try:
            amount = eval(amount)
        except Exception as e:
            logging.getLogger('error_log').error('Unable to evaluate amount {}'
                                                 .format(amount))
            amount = 0
        headers = self.get_authorization_header()
        end_point = "{}/{}?merchantId={}&basketAmount={}".format( \
            self.zestmoney_dict.get('api_base_url'),
            "Pricing/v2/quote/availableemiplans", \
            self.zestmoney_dict['client_id'], float(math.floor(amount)))

        # Map external response to standard underscored key convention.
        # Maintain code convention and API response integrity.
        zest_payment_keys_mapping = {"IsDefault"         : "is_default",
                                     "NumberOfMonths"    : "number_of_months",
                                     "TotalMonthlyAmount": "total_monthly_amount",
                                     "InterestAmount"    : "interest_amount",
                                     "InterestFreeMonths": "interest_free_months",
                                     "LoanAmount"        : "loan_amount",
                                     "DownpaymentAmount" : "down_payment_amount",
                                     "ProcessingFee"     : "processing_fee",
                                     "ProcessingFeeRate" : "processing_fee_rate",
                                     "DownpaymentRate"   : "down_payment_rate",
                                     "InterestRate"      : "interest_rate"
                                     }

        try:
            response = requests.get(end_point, headers=headers)
        except Exception as e:
            logging.getLogger("info_log").info("requests ERROR :: \
                Unable to fetch EMI Plans {}".format(e))
            return {}

        if not response.status_code == 200:
            logging.getLogger("info_log").info(
                "Unable to get EMI Plans {},{}".format( \
                    response.status_code, response.text))
            return {}

        json_response = response.json()
        mapped_response_data = {}
        mapped_response_data['recommended_options'] = [
            {zest_payment_keys_mapping[key]: x.get(key, "") \
             for key in x.keys() if zest_payment_keys_mapping.get(key)} \
            for x in json_response.get('RecommendedEmiOptions', [])]

        mapped_response_data['other_options'] = [
            {zest_payment_keys_mapping[key]: x.get(key, "") \
             for key in x.keys() if zest_payment_keys_mapping.get(key)} \
            for x in json_response.get('OtherEmiOptions', [])]

        return mapped_response_data

    def create_application_and_fetch_logon_url(self, txn_obj):

        order = txn_obj.order
        headers = self.get_authorization_header()
        headers.update({"Content-Type": "application/json"})
        end_point = "{}/{}".format( \
            self.zestmoney_dict.get('api_base_url'),
            "ApplicationFlow/LoanApplications")
        data = {}
        # data.update({"BasketAmount": float(math.ceil(order.total_incl_tax))})
        data.update({
            "OrderId"           : order.id,
            "DeliveryPostCode"  : '122011',
            "ReturnUrl"         : "{}/payment/zest-money/{}/callback/".format(settings.MAIN_DOMAIN_PREFIX, txn_obj.id),
            "ApprovedUrl"       : "{}/payment/zest-money/{}/callback/".format(settings.MAIN_DOMAIN_PREFIX, txn_obj.id),
            "MerchantCustomerId": order.email.lower().strip(),
            "EmailAddress"      : order.email.lower().strip(),
            "FullName"          : order.first_name + order.last_name if
            order.first_name and order.last_name else order.first_name
            ,"City"              : order.state,
            "AddressLine1"      : order.address,
            "MobileNumber"      : order.mobile,
        })

        oi_dict = order.get_oi_actual_price_mapping()
        if not oi_dict:
            return
        from order.models import OrderItem
        basketAmount = sum([float (math.floor (oi_dict.get (x.id, 0))) for x in
                        OrderItem.objects.filter(
                            id__in=oi_dict.keys ())])
        data.update({'BasketAmount' : float(math.floor(basketAmount))})

        basket_data = [{"Id"         : x.product.id,
                        "Description": x.product_name,
                        "Quantity"   : int(x.quantity),
                        "TotalPrice" : float(math.floor(oi_dict.get(x.id,0))),
                        "Category"   : "Services"
                        }for x in OrderItem.objects.filter(
                                        id__in=oi_dict.keys())]

        data['Basket'] = basket_data
        try:
            response = requests.post(end_point, data=json.dumps(data),
                                      headers=headers)
        except Exception as e:
            logging.getLogger("info_log").info("requests ERROR :: \
                Unable to create ZEST application {}".format(e))
            return ""

        if not response.status_code == 201:
            logging.getLogger("info_log").info(
                "Unable to create loan application {}".format(response.text))
            return ""

        json_response = response.json()
        logon_url = json_response.get('LogonUrl', '')
        # Cache url for 15 days and fetch when to be used.
        cache.set('zest_application_url_{}'.format(txn_obj.id), logon_url,
                   60 * 60 * 24 * 15)
        return logon_url

    def fetch_order_status(self, txn_obj):
        headers = self.get_authorization_header()
        headers.update({"Accept": "application/json"})

        end_point = "{}/{}".format( \
            self.zestmoney_dict.get('api_base_url'), \
            "ApplicationFlow/LoanApplications/orders/{}".format(
                txn_obj.order.id))

        try:
            response = requests.get(end_point, headers=headers)
        except Exception as e:
            logging.getLogger("info_log").info("requests ERROR :: \
                Unable to fetch Order Status {}".format(e))
            return ""

        if not response.status_code == 200:
            logging.getLogger("info_log").info(
                "Unable to fetch order status {}".format(response.text))
            return ""

        json_response = response.json()
        return json_response.get('OrderStatus', '')





class PayuPaymentUtil():
    KEYS = ('key', 'txnid', 'amount', 'productinfo', 'firstname', 'email',
            'udf1', 'udf2', 'udf3', 'udf4', 'udf5', 'udf6', 'udf7', 'udf8',
            'udf9', 'udf10')


    def generate_payu_hash(self,data,site=None):
        hash = sha512(b'')
        for key in self.KEYS:
            hash.update(str.encode("%s%s" % (str(data.get(key, '')), '|')))
        if site:
            hash.update(str.encode(settings.PAYU_INFO1.get('merchant_salt')))
        else:
            hash.update(str.encode(settings.PAYU_INFO.get('merchant_salt')))
        return hash.hexdigest().lower()

    def generate_payu_hash_data(self,data, KEYS,site=None):
        hash = sha512(b'')
        for key in KEYS:
            hash.update(str.encode("%s%s" % (str(data.get (key, '')), '|')))
        if site:
            hash.update(str.encode(settings.PAYU_INFO1.get('merchant_salt')))
        else:
            hash.update(str.encode(settings.PAYU_INFO.get('merchant_salt')))

        return hash.hexdigest().lower()

    def verify_payu_hash(self,data,site=None):
        keys_reversed = tuple (reversed (self.KEYS))
        if site:
            hash = sha512 (settings.PAYU_INFO1.get('merchant_salt'))
        else:
            hash.update(str.encode(settings.PAYU_INFO.get('merchant_salt')))
        hash.update("%s%s" % ('|', str(data.get('status', ''))))
        for key in keys_reversed:
            hash.update("%s%s" % ('|', str(data.get(key, ''))))
        return hash.hexdigest().lower() == data.get('hash')

    def orders_numbers_payparams(self,orders):
        if not orders:
            return None
        return "|".join(obj.txn_id for obj in orders)

    def create_payuparams(self,var, command,site=None):
        KEYS = ('key', 'command', 'var1')
        data = {}
        data.update({'var1'   : var,
                     'key'    : settings.PAYU_INFO1.get('merchant_key') if site else settings.PAYU_INFO.get(
                         'merchant_key'),
                     'command': command
                     })
        hash_value = self.generate_payu_hash_data(data, KEYS,site)
        data.update({'hash': hash_value})
        return data

    def update_payu_transaction_object(self,order_status, txn_obj, order_desc):
        if order_status == 'success':
            txn_obj.invoicesent.status = 2
            txn_obj.invoicesent.txn_id = txn_obj.id
            txn_obj.invoicesent.paid_on = datetime.now()
            txn_obj.invoicesent.save()
            txn_obj.txn_status = 1
            txn_obj.save()
            return True

        elif order_status == 'failure':
            txn_obj.txn_status = 2
            txn_obj.failure_desc = order_desc
            txn_obj.save()
            return False


    def generate_payu_dict(self, txn,site=None):
        order = txn.order
        if not order:
            logging.getLogger('error_log').error('No order found for txn {}'.format(txn))
            return {}
        oi_dict = order.get_oi_actual_price_mapping()
        from order.models import OrderItem
        initial_dict = {
            'firstname'  : order.first_name,
            'lastname'   : order.last_name if order.last_name else "",
            'email'      : order.email,
            'phone'      : order.mobile,
            'productinfo': ''.join(str([{"Description": x.product_name,
                              "Quantity"   : int(x.quantity),
                              }for x in OrderItem.objects.filter(
                                id__in=oi_dict.keys())]))[:100]
            ,'udf1'       : "Orderid - {}".format(order.id),
            'amount'     : float(order.total_incl_tax),
            "pg": 'CASH',
        }
        initial_dict.update \
            ({'txnid':txn.txn,
              'key':settings.PAYU_INFO['merchant_key'],
              'surl':"{}://{}/payment/payu/response/success/".format(settings.SITE_PROTOCOL,
                                                                   settings.SITE_DOMAIN),
              'furl':"{}://{}/payment/payu/response/failure/".format(settings.SITE_PROTOCOL,
                                                                   settings.SITE_DOMAIN),
              'curl':"{}://{}/payment/payu/response/cancel/".format(settings.SITE_PROTOCOL,
                                                               settings.SITE_DOMAIN),
              'msurl':"{}://{}/payment/payu/response/success/".format(settings.SITE_PROTOCOL,
                                                                   settings.SITE_DOMAIN),
              'mfurl':"{}://{}/payment/payu/response/failure/".format(settings.SITE_PROTOCOL,
                                                                   settings.SITE_DOMAIN),
              'mcurl':"{}://{}/payment/payu/response/cancel/".format(settings.SITE_PROTOCOL,
                                                               settings.SITE_DOMAIN),

              })

        if site:
            initial_dict.update({
                'txnid' : txn.txn,
                'key' : settings.PAYU_INFO1['merchant_key'],
                'surl' : "{}://{}/payment/payu/response/success/".format(settings.RESUME_SHINE_SITE_PROTOCOL,
                                                                         settings.RESUME_SHINE_SITE_DOMAIN),
                'furl' : "{}://{}/payment/payu/response/failure/".format(settings.RESUME_SHINE_SITE_PROTOCOL,
                                                                         settings.RESUME_SHINE_SITE_DOMAIN),
                'curl' : "{}://{}/payment/payu/response/cancel/".format(settings.RESUME_SHINE_SITE_PROTOCOL,
                                                                        settings.RESUME_SHINE_SITE_DOMAIN),
                'msurl' : "{}://{}/payment/payu/response/success/".format(settings.RESUME_SHINE_SITE_PROTOCOL,
                                                                          settings.RESUME_SHINE_SITE_DOMAIN),
                'mfurl' : "{}://{}/payment/payu/response/failure/".format(settings.RESUME_SHINE_SITE_PROTOCOL,
                                                                          settings.RESUME_SHINE_SITE_DOMAIN),
                'mcurl' : "{}://{}/payment/payu/response/cancel/".format(settings.RESUME_SHINE_SITE_PROTOCOL,
                                                                         settings.RESUME_SHINE_SITE_DOMAIN),

            })
        print(initial_dict)
        return initial_dict
