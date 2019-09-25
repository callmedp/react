# python imports
import base64,math
from hashlib import sha512,sha256
import requests
import logging
from datetime import datetime



# django imports
from django.conf import settings

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
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) %self.bs).encode('utf-8')

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

            data = {
                "candidate_email": oi.order.email,
                "skill_id": str(skill_id),
                "candidate_phone": oi.order.mobile,
                "candidate_name": oi.order.first_name,
                "candidate_city": candidate_location,
                "candidate_degree": candidate_degree,
                "shine_learning_order_id": str(oi.id)
            }
            update_auto_login_url_for_assesment(oi, data)





class PayuPaymentUtil():
    KEYS = ('key', 'txnid', 'amount', 'productinfo', 'firstname', 'email',
            'udf1', 'udf2', 'udf3', 'udf4', 'udf5', 'udf6', 'udf7', 'udf8',
            'udf9', 'udf10')


    def generate_payu_hash(self,data):
        hash = sha512(b'')
        for key in self.KEYS:
            hash.update(str.encode("%s%s" % (str(data.get(key, '')), '|')))
        hash.update(str.encode(settings.PAYU_INFO.get('merchant_salt')))
        return hash.hexdigest().lower()

    def generate_payu_hash_data(self,data, KEYS):
        hash = sha512(b'')
        for key in KEYS:
            hash.update(str.encode("%s%s" % (str(data.get (key, '')), '|')))
        hash.update(str.encode(settings.PAYU_INFO.get('merchant_salt')))
        return hash.hexdigest().lower()

    def verify_payu_hash(self,data):
        keys_reversed = tuple (reversed (self.KEYS))
        hash = sha512 (settings.PAYU_INFO.get('merchant_salt'))
        hash.update("%s%s" % ('|', str(data.get('status', ''))))
        for key in keys_reversed:
            hash.update("%s%s" % ('|', str(data.get(key, ''))))
        return hash.hexdigest().lower() == data.get('hash')

    def orders_numbers_payparams(self,orders):
        if not orders:
            return None
        return "|".join(obj.txn_id for obj in orders)

    def create_payuparams(self,var, command):
        KEYS = ('key', 'command', 'var1')
        data = {}
        data.update({'var1'   : var,
                     'key'    : settings.PAYU_INFO.get('merchant_key'),
                     'command': command
                     })
        hash_value = self.generate_payu_hash_data(data, KEYS)
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


    def generate_payu_dict(self, txn):
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
            "pg": 'CC',
        }
        initial_dict.update \
            ({'txnid':txn.txn,
              'key':settings.PAYU_INFO['merchant_key'],
              'surl':"{}/payment/payu/response/success/".format(settings.SITE_DOMAIN),
              'furl':"{}/payment/payu/response/failure/".format(settings.SITE_DOMAIN),
              'curl':"{}/payment/payu/response/cancel/".format(settings.SITE_DOMAIN),
              })
        return initial_dict
