# python imports
import base64
from hashlib import sha256
import requests
import logging
import hmac

# django imports
from django.conf import settings

# local imports

# inter app imports

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


def update_auto_login_url_for_assesment(orderitem):
    from core.api_mixins import AmcatApiMixin
    data = {
        "candidate_email": orderitem.order.email,
        "skill_name": "",
        "candidate_phone": orderitem.order.mobile,
        "candidate_name": orderitem.order.first_name,
        "candidate_city": "",
        "candidate_degree": "",
        "shine_learning_order_id": orderitem.order.number
    }
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
