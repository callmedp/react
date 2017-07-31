import datetime
import base64

from django.conf import settings
from django.template import Context
from django.template.loader import get_template
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile


from Crypto.Cipher import XOR
from weasyprint import HTML


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
        return email, type, (dt >= datetime.datetime.now())


class InvoiceGenerate(object):

    def get_invoice_data(self):
        pass

    def generate_pdf(self, context_dict={}, template_src=None):
        if template_src:
            html_template = get_template(template_src)
            context = Context(context_dict)

            rendered_html = html_template.render(context).encode(
                encoding="UTF-8")

            pdf_file = HTML(string=rendered_html).write_pdf()
            return pdf_file

        # http_response = HttpResponse(pdf_file, content_type='application/pdf')
        # http_response['Content-Disposition'] = 'filename="report.pdf"'
        # return http_response

    def save_order_invoice_pdf(self, order=None):
        if order:
            context_dict = {}
            pdf_file = self.generate_pdf(
                context_dict=context_dict,
                template_src='invoice/invoice.html')
            file_name = 'invoice-' + str(order.number) + '-'\
                + timezone.now().strftime('%d%m%Y') + '.pdf'
            order.invoice = SimpleUploadedFile(
                file_name, pdf_file,
                content_type='application/pdf')
            order.save()
            return order