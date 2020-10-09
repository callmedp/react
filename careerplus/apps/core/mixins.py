# python imports
import os,base64,datetime
import logging, gzip, shutil
from pathlib import Path
from datetime import date

# django imports
from django.conf import settings
from decimal import Decimal, ROUND_HALF_DOWN
from django.conf import settings
from django.template import Context
from django.template.loader import get_template
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile

# local imports

# inter app imports
from core.library.gcloud.custom_cloud_storage import (GCPInvoiceStorage, GCPResumeBuilderStorage)

# third party imports
from Crypto.Cipher import XOR
from weasyprint import HTML, CSS


class TokenExpiry(object):

    def encode(self, email, oi_pk, days=None):
        """
          used for booster resume donload from link

        """
        key_expires = datetime.datetime.today() + datetime.timedelta(
            settings.EMAIL_SMS_TOKEN_EXPIRY if not days else days)

        inp_str = '{salt}|{email}|{oi_pk}|{dt}'.format(**{'salt': settings.ENCODE_SALT, 'email': email, 'oi_pk': oi_pk,
                                                          'dt': key_expires.strftime(settings.TOKEN_DT_FORMAT)})

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
        inp_str = '{salt}|{email}|{type}|{dt}'.format(**{'salt': settings.ENCODE_SALT, 'email': email, 'type': type,
                                                         'dt': key_expires.strftime(settings.TOKEN_DT_FORMAT)})
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


class EncodeDecodeUserData(object):

    def encode(self, email, name, contact):
        inp_str = '{salt}|{email}|{name}|{contact}|{dt}'.format( \
            **{'salt': settings.ENCODE_SALT, 'email': email, \
               'name': name, 'contact': contact, 'dt': timezone.now()})

        ciph = XOR.new(settings.ENCODE_SALT)
        token = base64.urlsafe_b64encode(ciph.encrypt(inp_str))
        return token.decode()

    def decode(self, token):
        try:
            token = base64.urlsafe_b64decode(str(token))
            ciph = XOR.new(settings.ENCODE_SALT)
            inp_str = ciph.decrypt(token).decode()

        except Exception as e:
            logging.getLogger('error_log').error("%(msg)s : %(err)s" % \
                                                 {'msg': 'Invalid Token for Decryption', 'err': e})
            return None

        inp_list = inp_str.split('|')
        if len(inp_list) < 3:
            return None
        email = inp_list[1]
        name = inp_list[2]
        contact = inp_list[3]
        return email, name, contact


class InvoiceGenerate(object):

    def get_quantize(self, amount):
        return Decimal(amount).quantize(
            Decimal('.01'), rounding=ROUND_HALF_DOWN)

    def get_order_item_list(self, order=None):
        order_items = []
        if order:
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
        return order_items

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
            if order.country and order.country.phone == '91' and order.state and order.state.lower() == 'haryana':
                sgst = round((tax_rate_per / 2), 0)
                cgst = round((tax_rate_per / 2), 0)
                igst = 0

                sgst_amount = self.get_quantize(tax_amount / 2)
                cgst_amount = sgst_amount
                igst_amount = Decimal(0.00)

            elif order.country and order.country.phone == '91':
                sgst = round((tax_rate_per / 2), 0)
                cgst = round((tax_rate_per / 2), 0)
                igst = 0

                sgst_amount = self.get_quantize(tax_amount / 2)
                cgst_amount = sgst_amount
                igst_amount = Decimal(0.00)

            elif order.country_code == '91':
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
            if cart_obj.country and cart_obj.country.phone == '91' and cart_obj.state and cart_obj.state.lower() == 'haryana':
                sgst = round((tax_rate_per / 2), 0)
                cgst = round((tax_rate_per / 2), 0)
                igst = 0

                sgst_amount = self.get_quantize(tax_amount / 2)
                cgst_amount = sgst_amount
                igst_amount = Decimal(0.00)

            # Removed country check from here.
            # elif cart_obj.country and cart_obj.country.phone == '91':

            elif cart_obj:
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
            total_amount_after_discount = total_amount_after_discount - redeemed_reward_point

            tax_amount = total_payable_amount - total_amount_after_discount

            tax_rate_per = settings.TAX_RATE_PERCENTAGE

            # tax in percentage
            invoice_data.update(self.getTaxAmountByPart(
                tax_amount, tax_rate_per, cart_obj=None, order=order))

            order_items = self.get_order_item_list(order=order)

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
                "tax_amount": tax_amount,
                "coupon_amount": coupon_amount,
                "redeemed_reward_point": redeemed_reward_point,
                "tax_rate_per": tax_rate_per,

            })

        return invoice_data

    def generate_pdf(self, context_dict: object = {}, template_src: object = None) -> object:
        if template_src:
            html_template = get_template(template_src)

            rendered_html = html_template.render(context_dict).encode(encoding='UTF-8')

            pdf_file = HTML(string=rendered_html).write_pdf()

            return pdf_file

    def save_order_invoice_pdf(self, order=None):
        try:
            if order:
                context_dict = self.get_invoice_data(order=order)
                pdf_file = self.generate_pdf(
                    context_dict=context_dict,
                    template_src='invoice/invoice-product.html')
                full_path = 'order/%s/' % str(order.pk)
                file_name = 'invoice-' + str(order.number) + '-' \
                            + timezone.now().strftime('%Y%m%d') + '.pdf'

                pdf_file = SimpleUploadedFile(
                    file_name, pdf_file,
                    content_type='application/pdf')

                if not settings.IS_GCP:
                    if not os.path.exists(settings.INVOICE_DIR + full_path):
                        os.makedirs(settings.INVOICE_DIR + full_path)
                    dest = open(
                        settings.INVOICE_DIR + full_path + file_name, 'wb')
                    for chunk in pdf_file.chunks():
                        dest.write(chunk)
                    dest.close()
                else:
                    GCPInvoiceStorage().save(settings.INVOICE_DIR + full_path + file_name, pdf_file)
                order.invoice = settings.INVOICE_DIR + full_path + file_name
                order.save()
                return order, order.invoice
        except Exception as e:
            logging.getLogger('error_log').error("%(msg)s : %(err)s" % {'msg': 'Contact Tech ERROR', 'err': e})
        return None, None

