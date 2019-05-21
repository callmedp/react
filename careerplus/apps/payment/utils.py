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
