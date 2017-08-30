import datetime
import base64

from decimal import Decimal, ROUND_HALF_DOWN
from Crypto.Cipher import XOR

from django.conf import settings
from django.template import Context
from django.template.loader import get_template
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile
# from django.http import HttpResponse

from weasyprint import HTML


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

    def get_quantize(self, amount):
        return Decimal(amount).quantize(
            Decimal('.01'), rounding=ROUND_HALF_DOWN)

    def getTaxAmountByPart(self, tax_amount, tax_rate_per, cart_obj=None, order=None):
        data = {
            "sgst": round((tax_rate_per / 2), 0),
            "cgst": round((tax_rate_per / 2), 0),
            "igst": 0,
            "sgst_amount": Decimal(0.00),
            "cgst_amount": Decimal(0.00),
            "igst_amount": Decimal(0.00),
        }
        if order:
            # tax in percentage
            if order.country.lower() == 'india' and order.state.lower() == 'haryana':
                sgst = round((tax_rate_per / 2), 0)
                cgst = round((tax_rate_per / 2), 0)
                igst = 0

                sgst_amount = self.get_quantize(tax_amount / 2)
                cgst_amount = sgst_amount
                igst_amount = Decimal(0.00)

            elif order.country.lower() == 'india':
                sgst = round((tax_rate_per / 2), 0)
                cgst = round((tax_rate_per / 2), 0)
                igst = 0

                sgst_amount = self.get_quantize(tax_amount / 2)
                cgst_amount = sgst_amount
                igst_amount = Decimal(0.00)
            else:
                sgst = 0
                cgst = 0
                igst = 0

                sgst_amount = self.get_quantize(tax_amount / 2)
                cgst_amount = sgst_amount
                igst_amount = Decimal(0.00)
        elif cart_obj:
            # tax in percentage
            if cart_obj.country.lower() == 'india' and cart_obj.state.lower() == 'haryana':
                sgst = round((tax_rate_per / 2), 0)
                cgst = round((tax_rate_per / 2), 0)
                igst = 0

                sgst_amount = self.get_quantize(tax_amount / 2)
                cgst_amount = sgst_amount
                igst_amount = Decimal(0.00)

            elif cart_obj.country.lower() == 'india':
                sgst = round((tax_rate_per / 2), 0)
                cgst = round((tax_rate_per / 2), 0)
                igst = 0

                sgst_amount = self.get_quantize(tax_amount / 2)
                cgst_amount = sgst_amount
                igst_amount = Decimal(0.00)
            else:
                sgst = 0
                cgst = 0
                igst = 0

                sgst_amount = self.get_quantize(tax_amount / 2)
                cgst_amount = sgst_amount
                igst_amount = Decimal(0.00)
        data.update({
            "sgst": sgst,
            "cgst": cgst,
            "igst": igst,
            "sgst_amount": sgst_amount,
            "cgst_amount": cgst_amount,
            "igst_amount": igst_amount,
        })
        return data

    def get_invoice_data(self, order=None):
        invoice_data = {}
        if order:
            invoice_no = 'IN' + str(order.id)
            email = order.email
            mobile = order.mobile
            if order.payment_date:
                invoice_date = order.payment_date
            else:
                invoice_date = timezone.now()

            coupons_applied = order.couponorder_set.all()
            coupon_amount = Decimal(0)

            for coupon in coupons_applied:
                coupon_amount += coupon.value

            # loyalty point used
            redeemed_reward_point = Decimal(0)
            wal_txn = order.wallettxn.filter(txn_type=2).order_by('-created').select_related('wallet')
            if wal_txn.exists():
                wal_txn = wal_txn[0]
                redeemed_reward_point = wal_txn.point_value

            total_payable_amount = order.total_incl_tax

            total_amount_before_discount = order.total_excl_tax  # without discount
            total_amount_after_discount = total_amount_before_discount - coupon_amount
            total_amount_after_discount = total_amount_before_discount - redeemed_reward_point

            tax_amount = total_payable_amount - total_amount_after_discount

            tax_rate_per = (tax_amount * 100) / total_amount_after_discount
            tax_rate_per = self.get_quantize(tax_rate_per)

            # tax in percentage
            invoice_data.update(self.getTaxAmountByPart(
                tax_amount, tax_rate_per, cart_obj=None, order=order))

            order_items = []
            parent_ois = order.orderitems.filter(
                parent=None).select_related('product', 'partner')
            for p_oi in parent_ois:
                data = {}
                data['oi'] = p_oi
                data['addons'] = order.orderitems.filter(
                    parent=p_oi,
                    is_addon=True,
                    no_process=False).select_related('product', 'partner')
                data['variations'] = order.orderitems.filter(
                    parent=p_oi, no_process=False,
                    is_variation=True).select_related('product', 'partner')
                data['combos'] = order.orderitems.filter(
                    parent=p_oi, no_process=False,
                    is_combo=True).select_related('product', 'partner')
                order_items.append(data)

            invoice_data.update({
                "invoice_no": invoice_no,
                "email": email,
                "mobile": mobile,
                "invoice_date": invoice_date,
                "order_items": order_items,
                "total_amount_before_discount": total_amount_before_discount,
                "total_amount_after_discount": total_amount_after_discount,
                "total_payable_amount": total_payable_amount,
                "order": order,
                "coupon_amount": coupon_amount,
                "redeemed_reward_point": redeemed_reward_point,
                
            })

        return invoice_data

    def generate_pdf(self, context_dict={}, template_src=None):
        if template_src:
            html_template = get_template(template_src)
            context = Context(context_dict)

            rendered_html = html_template.render(context).encode(encoding='UTF-8')

            pdf_file = HTML(string=rendered_html).write_pdf()
            # stylesheets=[CSS(settings.STATICFILES_DIRS[0] +  '/shinelearn/css/invoice/invoice.css')]
            return pdf_file

            # http_response = HttpResponse(pdf_file, content_type='application/pdf')
            # http_response['Content-Disposition'] = 'filename="report.pdf"'
            # return http_response

    def save_order_invoice_pdf(self, order=None):
        if order:
            context_dict = self.get_invoice_data(order=order)
            pdf_file = self.generate_pdf(
                context_dict=context_dict,
                template_src='invoice/invoice-product.html')
            file_name = 'invoice-' + str(order.number) + '-'\
                + timezone.now().strftime('%d%m%Y') + '.pdf'
            order.invoice = SimpleUploadedFile(
                file_name, pdf_file,
                content_type='application/pdf')
            order.save()
            return order