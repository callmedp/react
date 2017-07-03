import logging
import base64

from Crypto.Cipher import XOR, AES
from django.conf import settings


class AutoLogin(object):

    def encode(self, email, candidateid):

        inp_str = '{email}|{candidateid}|{salt}'.format(
            **{'email': email, 'candidateid': candidateid, 'salt': settings.ENCODE_SALT})

        b = bytes(inp_str, 'utf-8')
        ciph = XOR.new(settings.ENCODE_SALT)

        return base64.b64encode(ciph.encrypt(b))

    def decode(self, token):
        token = base64.b64decode(token)
        ciph = XOR.new(settings.ENCODE_SALT)
        inp_str = ciph.decrypt(token)
        str_inp = inp_str.decode("utf-8")
        inp_list = str_inp.split('|')
        email = str_inp[0]
        candidateid = inp_list[1]
        return email, candidateid