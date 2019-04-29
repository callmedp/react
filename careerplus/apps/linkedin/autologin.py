import base64
import datetime

from Crypto.Cipher import XOR
from django.conf import settings


class AutoLogin(object):

    def encode(self, email, candidateid, days=None):
        import ipdb; ipdb.set_trace()
        key_expires = datetime.datetime.today() + datetime.timedelta(
            settings.LOGIN_TOKEN_EXPIRY if not days else days)
        inp_str = '{email}|{candidateid}|{dt}|{salt}'.format(
            **{'email': email, 'candidateid': candidateid, 'dt': key_expires.strftime(settings.TOKEN_DT_FORMAT), 'salt': settings.ENCODE_SALT})
        b = bytes(inp_str, 'utf-8')
        ciph = XOR.new(settings.ENCODE_SALT)
        token = base64.b64encode(ciph.encrypt(b))
        return token.decode()

    def decode(self, token):
        token = base64.b64decode(token)
        ciph = XOR.new(settings.ENCODE_SALT)
        inp_str = ciph.decrypt(token)
        str_inp = inp_str.decode("utf-8")
        inp_list = str_inp.split('|')
        email = inp_list[0]
        candidateid = inp_list[1]
        dt = datetime.datetime.strptime(
            inp_list[2], settings.TOKEN_DT_FORMAT)
        return email, candidateid, (dt >= datetime.datetime.now())

