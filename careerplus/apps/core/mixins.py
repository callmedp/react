import datetime
import base64

from django.conf import settings

from Crypto.Cipher import XOR
# from filebrowser.base import FileObject


# class ImageCompressedMixin(object):

#     def save_image(self, image, variant=None):
#         try:
#             image_orig = FileObject(image.path)
#             if image_orig.filetype == "Image":
#                 variant_list = [variant]
#                 if not variant:
#                     variant_list = ['large', 'medium']
#                 for variant in variant_list:
#                     image_orig.version_generate(variant)
#                 return True
#         except:
#             pass
#         return False


class TokenExpiry(object):

    def encode(self, email, oi_pk, days=None):
        """
          used for booster resume donload from link

        """
        key_expires = datetime.datetime.today() + datetime.timedelta(settings.EMAIL_SMS_TOKEN_EXPIRY if not days else days)

        inp_str = '{salt}|{email}|{oi_pk}|{dt}'.format(**{'salt': settings.ENCODE_SALT, 'email': email, 'oi_pk': oi_pk, 'dt': key_expires.strftime(settings.TOKEN_DT_FORMAT)})

        ciph = XOR.new(settings.ENCODE_SALT)
        token = base64.urlsafe_b64encode(ciph.encrypt(inp_str))
        return token.decode()

    def decode(self, token):
        token = base64.urlsafe_b64decode(str(token))
        ciph = XOR.new(settings.ENCODE_SALT)
        inp_str = ciph.decrypt(token).decode()
        inp_list = inp_str.split('|')
        email = inp_list[1]
        oi_pk = int(inp_list[2])
        dt = datetime.datetime.strptime(inp_list[3], settings.TOKEN_DT_FORMAT)
        return email, oi_pk, (dt >= datetime.datetime.now())


class TokenGeneration(object):
    # used auto login token for shine

    def encode(self, email, type, days=None):
        key_expires = datetime.datetime.today() + datetime.timedelta(
            settings.LOGIN_TOKEN_EXPIRY if not days else days)
        inp_str = '{salt}|{email}|{type}|{dt}'.format(**{'salt': settings.ENCODE_SALT, 'email': email, 'type': type, 'dt': key_expires.strftime(settings.TOKEN_DT_FORMAT)})
        ciph = XOR.new(settings.ENCODE_SALT)
        token = base64.urlsafe_b64encode(ciph.encrypt(inp_str))
        return token.decode()

    def decode(self, token):
        token = base64.urlsafe_b64decode(str(token))
        ciph = XOR.new(settings.ENCODE_SALT)
        inp_str = ciph.decrypt(token).decode()
        inp_list = inp_str.split('|')
        email = inp_list[1]
        type = int(inp_list[2])
        dt = datetime.datetime.strptime(inp_list[3], settings.TOKEN_DT_FORMAT)
        # try:
        #     orders = Order.objects.filter(email=email, status=1)
        #     if orders.exists():
                
        # except:
        #     return None, None, None
        return email, type, (dt >= datetime.datetime.now())
