# python imports
import os,base64,datetime
import logging, gzip, shutil
from io import BytesIO
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
from resumebuilder.models import Candidate
from core.library.gcloud.custom_cloud_storage import (GCPInvoiceStorage, GCPPrivateMediaStorage)

# third party imports
import pdfkit
import zipfile
from PIL import Image
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

            elif cart_obj.country and cart_obj.country.phone == '91':
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


class ResumeGenerate(object):

    def generate_file(self, context_dict={}, template_src= None,file_type='pdf'):
        if not template_src:
            return None

        html_template = get_template(template_src)
        rendered_html = html_template.render(context_dict).encode(encoding='UTF-8')
        if file_type == 'pdf':
            options = {
                        'page-size': 'Letter',
                        'encoding': "UTF-8",
                        'no-outline': None,
                        'margin-top': '0.3in',
                        'margin-right': '0.2in',
                        'margin-bottom': '0.2in',
                        'margin-left': '0.2in',
                        'quiet': ''
                    }
            rendered_html = rendered_html.decode().replace("\n","")
            file = pdfkit.from_string(rendered_html,False,options=options)

        elif file_type == 'png':
            file = HTML(string=rendered_html).write_png()

        return file

    def store_file(self, file_dir, file_name, file_content):
        directory_path = "{}/{}".format(settings.RESUME_TEMPLATE_DIR, file_dir)
        if settings.IS_GCP:
            gcp_file = GCPPrivateMediaStorage().open("{}/{}".format(directory_path, file_name), 'wb')
            gcp_file.write(file_content)
            gcp_file.close()
            return

        directory_path = "{}/{}".format(settings.MEDIA_ROOT, directory_path)
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
        dest = open("{}/{}".format(directory_path, file_name), 'wb')
        dest.write(file_content)
        dest.close()

    def zip_all_resume_pdfs(self, order):
        content_type = "zip"
        candidate = Candidate.objects.get(candidate_id=order.candidate_id)
        file_dir = "{}/{}".format(candidate.id, content_type)
        file_name = "{}.{}".format("combo", content_type)

        zip_stream = BytesIO()
        zf = zipfile.ZipFile(zip_stream, "w")

        for i in range(1, 6):
            current_file = "{}_{}-{}.{}".format(order.first_name, order.last_name, i, "pdf")
            pdf_file_path = "{}/{}/pdf/{}.pdf".format(settings.RESUME_TEMPLATE_DIR, candidate.id, i)
            try:
                file_obj = GCPPrivateMediaStorage().open(pdf_file_path)
            except:
                logging.getLogger('error_log').error("Unable to open file - {}".format(pdf_file_path))

            if not settings.IS_GCP:
                pdf_file_path = "{}/{}".format(settings.MEDIA_ROOT, pdf_file_path)
                try:
                    file_obj = open(pdf_file_path, "rb")
                except:
                    logging.getLogger('error_log').error("Unable to open file - {}".format(pdf_file_path))
                    continue

            open(current_file, 'wb').write(file_obj.read())
            zf.write(current_file)
            os.unlink(current_file)

        self.store_file(file_dir, file_name, zip_stream.getvalue())

    def generate_pdf_for_template(self, order=None, index='1'):
        content_type = "pdf"
        candidate_id = order.candidate_id
        template_id = int(index)
        candidate = Candidate.objects.filter(candidate_id=candidate_id).first()
        if not candidate:
            return {}

        file_dir = "{}/{}".format(candidate.id, content_type)
        file_name = "{}.{}".format(index, content_type)
        entity_preference = eval(candidate.entity_preference_data)
        extracurricular = candidate.extracurricular_list
        education = candidate.candidateeducation_set.all().order_by('order')
        experience = candidate.candidateexperience_set.all().order_by('order')
        skills = candidate.skill_set.all().order_by('order')
        achievements = candidate.candidateachievement_set.all().order_by('order')
        references = candidate.candidatereference_set.all().order_by('order')
        projects = candidate.candidateproject_set.all().order_by('order')
        certifications = candidate.candidatecertification_set.all().order_by('order')
        languages = candidate.candidatelanguage_set.all().order_by('order')
        current_exp = experience.filter(is_working=True).order_by('-start_date').first()
        current_config = candidate.ordercustomisation_set.filter(template_no=template_id).first()
        entity_position = current_config.entity_position_eval

        latest_experience, latest_end_date = '', None
        for exp in experience:
            if exp.is_working:
                latest_end_date = date.today()
                latest_experience = exp.job_profile
                break
            elif latest_end_date is None:
                latest_end_date = exp.end_date
                latest_experience = exp.job_profile
            else:
                if latest_end_date < exp.end_date:
                    latest_end_date = exp.end_date
                    latest_experience = exp.job_profile

        # latest_experience = experience and experience[0].job_profile or 'FULL STACK DEVELOPER'

        template = get_template('resume{}_preview.html'.format(template_id))
        context_dict = {'candidate': candidate, 'education': education, 'experience': experience, 'skills': skills,
                        'achievements': achievements, 'references': references, 'projects': projects,
                        'certifications': certifications, 'extracurricular': extracurricular, 'languages': languages,
                        'current_exp': current_exp, 'latest_exp': latest_experience,
                        'preference_list': entity_preference, 'current_config': current_config,
                        'entity_position': entity_position, "width": 93.7
                        }

        pdf_file = self.generate_file(
            context_dict=context_dict,
            template_src='resume{}_preview.html'.format(index),
            file_type='pdf')

        self.store_file(file_dir, file_name, pdf_file)

    def save_order_resume_pdf(self, order=None, is_combo=False, index=None):
        if not order:
            return None, None

        if not is_combo:
            return self.generate_pdf_for_template(order, index=str(index))

        for i in range(1, 6):
            self.generate_pdf_for_template(order, index=str(i))

        return self.zip_all_resume_pdfs(order)
