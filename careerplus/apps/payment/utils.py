#python imports
import base64
from hashlib import sha256
import requests
import logging

#django imports
from django.conf import settings

#local imports

#inter app imports

#third party imports
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

    vendor = orderitem.product.vendor.name
    vendor = vendor.lower()
    api_url = settings.VENDOR_URLS[vendor]['get_autologin_url']
    headers = settings.VENDOR_HEADERS[vendor]

    data = {
        'module_id': orderitem.product.attr,
        'email': orderitem.order.email
    }
    resp = requests.post(api_url, data=data, headers=headers)
    if resp.status_code == 200:
        resp = resp.json()
        autologin_url = resp['data']['autoLoginUrl']
        logging.getLogger('info_log').error(
            "AutoLogin url for Order item %s successfully retrieved" % (str(orderitem))
        )
        orderitem.autologin_url = autologin_url
        orderitem.save()
        return True
    else:
        logging.getLogger('error_log').error(
            "Failed fetching autologin for Order item:- %s , Error:- %s" % (str(orderitem), str(resp.content))
        )
        return False
