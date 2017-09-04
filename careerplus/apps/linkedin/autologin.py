import logging
import base64

from Crypto.Cipher import XOR, AES
from django.conf import settings
from shine.core import ShineCandidateDetail


class AutoLogin(object):

    def encode(self, email, candidateid, orderid):
        inp_str = ''
        if not email and not candidateid:
            pass
        if email and candidateid:
            inp_str = '{email}|{candidateid}|{orderid}|{salt}'.format(
                **{'email': email, 'candidateid': candidateid, 'orderid': orderid, 'salt': settings.ENCODE_SALT})
        if email and not candidateid:
            resp_status = ShineCandidateDetail().get_status_detail(email=email, shine_id=None)
            inp_str = '{email}|{candidateid}|{orderid}|{salt}'.format(
                **{'email': email, 'candidateid': resp_status['candidate_id'], 'orderid': orderid, 'salt': settings.ENCODE_SALT})
        if not email and candidateid:
            resp_status = ShineCandidateDetail().get_status_detail(email=None, shine_id=candidateid)
            inp_str = '{email}|{candidateid}|{orderid}|{salt}'.format(
                **{'email': resp_status['email'], 'candidateid': candidateid, 'orderid': orderid, 'salt': settings.ENCODE_SALT})

        b = bytes(inp_str, 'utf-8')
        ciph = XOR.new(settings.ENCODE_SALT)

        return base64.b64encode(ciph.encrypt(b))

    def decode(self, token):
        token = base64.b64decode(token)
        ciph = XOR.new(settings.ENCODE_SALT)
        inp_str = ciph.decrypt(token)
        str_inp = inp_str.decode("utf-8")
        inp_list = str_inp.split('|')
        email = inp_list[0]
        candidateid = inp_list[1]
        orderid = inp_list[2]
        return email, candidateid, orderid
