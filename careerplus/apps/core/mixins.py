import datetime
import base64

from django.conf import settings
from django.template import Context
from django.template.loader import get_template
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile

from Crypto.Cipher import XOR
from weasyprint import HTML
from decimal import Decimal


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

    def get_invoice_data(self, order=None):
        invoice_data = {}
        if order:
            invoice_no = order.id
            email = order.email
            mobile = order.mobile
            invoice_date = timezone.now()

            tax_amount = Decimal(0)
            total_price = Decimal(0)
            order_items = []
            parent_ois = order.orderitems.filter(parent=None).select_related('product', 'partner')
            for p_oi in parent_ois:
                data = {}
                data['oi'] = p_oi
                data['addons'] = order.orderitems.filter(
                    parent=p_oi, is_combo=False,
                    is_variation=False,
                    no_process=False).select_related('product', 'partner')
                data['variations'] = order.orderitems.filter(
                    parent=p_oi, no_process=False,
                    is_variation=True).select_related('product', 'partner')
                data['combos'] = order.orderitems.filter(
                    parent=p_oi, no_process=False,
                    is_combo=True).select_related('product', 'partner')
                order_items.append(data)

            for data in order_items:
                parent_oi = data.get('oi')
                addons = data.get('addons')
                variations = data.get('variations')
                combos = data.get('combos')
                product_price = parent_oi.product.get_price()
                product_tax = product_price * Decimal(18 / 100)
                parent_oi.oi_price_incl_tax = product_price + product_tax
                parent_oi.save()
                if parent_oi.no_process == True and parent_oi.product.type_flow == 12:
                    tax_amount += product_tax
                    total_price += parent_oi.oi_price_incl_tax
                elif parent_oi.no_process == False:
                    tax_amount += product_tax
                    total_price += parent_oi.oi_price_incl_tax

                for oi in addons:
                    product_price = oi.product.get_price()
                    product_tax = product_price * Decimal(18 / 100)
                    oi.oi_price_incl_tax = product_price + product_tax
                    oi.save()
                    tax_amount += product_tax
                    total_price += oi.oi_price_incl_tax

                for oi in variations:
                    product_price = oi.product.get_price()
                    product_tax = product_price * Decimal(18 / 100)
                    oi.oi_price_incl_tax = product_price + product_tax
                    oi.save()
                    tax_amount += product_tax
                    total_price += oi.oi_price_incl_tax

                for oi in combos:
                    product_price = oi.product.get_price()
                    product_tax = product_price * Decimal(18 / 100)
                    oi.oi_price_incl_tax = product_price + product_tax
                    oi.save()
                    tax_amount += product_tax
                    total_price += oi.oi_price_incl_tax

            tax_amount = round(tax_amount, 2)
            tax_level1 = round(tax_amount / 2, 2)
            tax_level2 = round(tax_amount / 2, 2)
            total_price = round(total_price, 2)
            invoice_data.update({
                "invoice_no": invoice_no,
                "email": email,
                "mobile": mobile,
                "invoice_date": invoice_date,
                "order_items": order_items,
                "tax_amount": tax_amount,
                "tax_level1": tax_level1,
                "tax_level2": tax_level2,
                "total_price": total_price,
                "order": order,
            })

        return invoice_data

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
            context_dict = self.get_invoice_data(order=order)
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