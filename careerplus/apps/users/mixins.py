import requests
import json
import logging
import os
import datetime

from django.contrib.gis.geoip import GeoIP
from django.conf import settings
from django.utils import timezone
from shine.core import ShineCandidateDetail
from django.core.files.uploadedfile import SimpleUploadedFile

from geolocation.models import Country
from order.models import OrderItem

from .choices import (
    WRITING_STARTER_VALUE, RESUME_WRITING_MATRIX_DICT,
    LINKEDIN_STARTER_VALUE, LINKEDIN_WRITING_MATRIX_DICT,
    EXPRESS, SUPER_EXPRESS, VISUAL_RESUME_PRODUCT_LIST,
    VISUAL_RESUME, COVER_LETTER_PRODUCT_LIST, COVER_LETTER,
    COUNTRY_SPCIFIC_VARIATION, SECOND_REGULAR_RESUME_PRODUCT_LIST,
    SECOND_REGULAR_RESUME, DISCOUNT_ALLOCATION_DAYS,
    COMBO_DISCOUNT, REGULAR_SLA, EXPRESS_SLA, SUPER_EXPRESS_SLA,
    PASS_PERCENTAGE, INCENTIVE_PASS_PERCENTAGE,
    PENALTY_PERCENTAGE, INCENTIVE_PERCENTAGE
)


class WriterInvoiceMixin(object):
    def get_context_writer_invoice(self, user=None, invoice_date=None):
        item_list = []
        error = ''
        data = {'item_list': item_list, "error": error}
        msg = 'Few writer mandatory fields are not available\
            for invoice generation please contact support'

        if not user:
            error = "Provide proper writer"

        if not invoice_date:
            error = 'Provide invoice date'

        if user and user.userprofile and not error:
            if user.name and not error:
                writer_name = user.name
            else:
                error = msg

            if user.userprofile.pan_no and not error:
                writer_pan = user.userprofile.pan_no
            else:
                error = msg

            if user.userprofile.gstin and not error:
                writer_gstin = user.userprofile.gstin
            else:
                writer_gstin = ''  # optional

            if user.userprofile.address and not error:
                writer_address = user.userprofile.address
            else:
                error = msg

            if user.userprofile.writer_type and not error:
                writer_group = user.userprofile.writer_type
            else:
                msg = error

            if user.userprofile.po_number and not error:
                writer_po_number = user.userprofile.po_number
            else:
                error = msg

            valid_from = user.userprofile.valid_from
            valid_to = user.userprofile.valid_to
            if valid_from and valid_to and valid_from < valid_to \
                and invoice_date and invoice_date < valid_to:
                pass
            else:
                error = 'Update writer Po Number validity'

            data.update({
                "writer_name": writer_name,
                "writer_pan": writer_pan,
                "writer_gstin": writer_gstin,
                "writer_address": writer_address,
                "writer_group": writer_group,
                "writer_po_number": writer_po_number,
                "error": error
            })

        elif not error:
            error = msg

        if user and invoice_date and not error:
            orderitems = OrderItem.objetcs.filter(
                order__status__in=[1, 3],
                product__type_flow__in=[1, 8, 12, 13],
                oi_status=4, assigned_to=user,
                closed_on__month=invoice_date.month,
                closed_on__year=invoice_date.year, no_process=False).select_related('product').order_by('id')

            writing_dict = RESUME_WRITING_MATRIX_DICT
            linkedin_dict = LINKEDIN_WRITING_MATRIX_DICT
            express_slug_list = settings.EXPRESS_DELIVERY_SLUG
            super_express_slug_list = settings.SUPER_EXPRESS_DELIVERY_SLUG
            delivery_slug_list = express_slug_list + super_express_slug_list

            last_invoice_date = invoice_date.replace(day=1)
            last_invoice_date = last_invoice_date - datetime.timedelta(days=1)
            added_base_object = []  # for country specific resume
            added_delivery_object = []  # for delivery price only for parent item 
            combo_discount_object = []  # for discount combo, eithr resume or linkedin
            user_type = user.userprofile.writer_type if user.userprofile else 0

            total_combo_discount = 0
            total_sum = 0
            success_closure = 0

            for oi in orderitems:
                oi_dict = {}
                # sla incentive or penalty calculation
                if oi.assigned_date and oi.closed_on and oi.assigned_date < oi.closed_on:
                    finish_days = (oi.closed_on - oi.assigned_date).days
                    if oi.delivery_service and oi.delivery_service.slug in express_slug_list:
                        if finish_days <= EXPRESS_SLA:
                            success_closure += 1
                    elif oi.delivery_service and oi.delivery_service.slug in super_express_slug_list:
                        if finish_days <= SUPER_EXPRESS_SLA:
                            success_closure += 1
                    else:
                        if finish_days <= REGULAR_SLA:
                            success_closure += 1

                if oi.is_variation:
                    p_oi = oi.parent
                    variations = p_oi.orderitem_set.filter(
                        variation=True, no_process=False)
                    closed_variations = p_oi.orderitem_set.filter(
                        variation=True, no_process=False, oi_status=4).order_by('-closed_on')

                    if variations.count() == closed_variations.count() and p_oi.pk not in added_base_object:
                        p_oi_dict = {}
                        pk = p_oi.pk
                        product_name = p_oi.product.get_name
                        closed_on = closed_variations[0].closed_on.date()
                        combo_discount = 0
                        exp_code = p_oi.get_exp()
                        if not exp_code:
                            exp_code = 'FR'
                        starter_value = WRITING_STARTER_VALUE
                        amount = starter_value
                        value_dict = writing_dict.get(exp_code, {})
                        if value_dict and value_dict.get(user_type):
                            amount = (starter_value * value_dict.get(user_type)) / 100
                            amount = int(amount)

                        # combo discount calculation
                        if p_oi.product and p_oi.product.type_flow in [1, 12, 13] and p_oi.pk not in combo_discount_object:
                            order = p_oi.order
                            linkedin_ois = order.orderitems.filter(
                                product__type_flow=8, oi_status=4).order_by('-id')
                            if linkedin_ois.exsists():
                                linkedin_obj = linkedin_ois[0]
                                exp_code = linkedin_obj.get_exp()
                                if not exp_code:
                                    exp_code = 'FR'
                                starter_value = LINKEDIN_STARTER_VALUE
                                linkedin_amount = starter_value
                                value_dict = linkedin_dict.get(exp_code, {})
                                if value_dict and value_dict.get(user_type):
                                    linkedin_amount = (starter_value * value_dict.get(user_type)) / 100
                                    linkedin_amount = int(linkedin_amount)

                                combo_discount = max(amount, linkedin_amount) * (COMBO_DISCOUNT / 100)
                                combo_discount_object.append(linkedin_obj.pk)
                                combo_discount_object.append(p_oi.pk)
                            else:
                                pass
                        added_base_object.append(pk)

                        p_oi_dict.update({
                            "item_id": pk,
                            "product_name": product_name,
                            "closed_on": closed_on,
                            "combo_discount": combo_discount,
                            "amount": amount,
                            "item_type": "variation_parent",
                        })
                        total_sum += amount

                        item_list.append(p_oi_dict)

                        if p_oi.delivery_service and p_oi.delivery_service.slug in delivery_slug_list and p_oi.pk not in added_delivery_object:
                            amount = 0
                            if p_oi.delivery_service.slug in express_slug_list:
                                amount = EXPRESS
                            elif p_oi.delivery_service.slug in super_express_slug_list:
                                amount = SUPER_EXPRESS
                            d_dict = {
                                "item_id": p_oi.pk,
                                "product_name": p_oi.delivery_service.name,
                                "closed_on": closed_on,
                                "combo_discount": 0,
                                "amount": amount,
                                "item_type": "delivery_service",
                            }
                            item_list.append(d_dict)
                            added_delivery_object.append(p_oi.pk)
                            total_sum += amount

                    pk = oi.pk
                    product_name = oi.product.get_name
                    closed_on = oi.closed_on.date()
                    combo_discount = 0
                    amount = COUNTRY_SPCIFIC_VARIATION

                    oi_dict.update({
                        "item_id": pk,
                        "product_name": product_name,
                        "closed_on": closed_on,
                        "combo_discount": combo_discount,
                        "amount": amount,
                        "item_type": "variation",
                    })
                    item_list.append(oi_dict)
                    total_sum += amount

                elif oi.is_addon:
                    pk = oi.pk
                    product_name = oi.product.get_name
                    closed_on = oi.closed_on.date()
                    combo_discount = 0
                    product_pk = oi.product.pk
                    amount = 0
                    if product_pk in VISUAL_RESUME_PRODUCT_LIST:
                        amount = VISUAL_RESUME
                    elif product_pk in COVER_LETTER_PRODUCT_LIST:
                        amount = COVER_LETTER
                    elif product_pk in SECOND_REGULAR_RESUME_PRODUCT_LIST:
                        amount = SECOND_REGULAR_RESUME
                    else:
                        error = 'Addon Product id - %s is missing in product_list (backend).' % (product_pk)
                        break

                    oi_dict.update({
                        "item_id": pk,
                        "product_name": product_name,
                        "closed_on": closed_on,
                        "combo_discount": combo_discount,
                        "amount": amount,
                        "item_type": "addon",
                    })
                    item_list.append(oi_dict)
                    total_sum += amount
                elif oi.is_combo:
                    pk = oi.pk
                    product_name = oi.product.get_name
                    closed_on = oi.closed_on.date()
                    combo_discount = 0
                    product_pk = oi.product.pk
                    resuem_writing_ois = oi.order.orderitems.filter(
                        product__type_flow__in=[1, 12])
                    amount = 0
                    if product_pk in VISUAL_RESUME_PRODUCT_LIST and resuem_writing_ois.exists():
                        amount = VISUAL_RESUME
                    elif product_pk in COVER_LETTER_PRODUCT_LIST and resuem_writing_ois.exists():
                        amount = COVER_LETTER
                    elif product_pk in SECOND_REGULAR_RESUME_PRODUCT_LIST and resuem_writing_ois.exists():
                        amount = SECOND_REGULAR_RESUME
                    else:
                        exp_code = oi.get_exp()
                        if not exp_code:
                            exp_code = 'FR'
                        if oi.product.type_flow == 8:
                            starter_value = LINKEDIN_STARTER_VALUE
                            value_dict = linkedin_dict.get(exp_code, {})
                        else:
                            starter_value = WRITING_STARTER_VALUE
                            value_dict = writing_dict.get(exp_code, {})

                        amount = starter_value
                        if value_dict and value_dict.get(user_type):
                            amount = (starter_value * value_dict.get(user_type)) / 100

                        if product_pk in VISUAL_RESUME_PRODUCT_LIST:
                            amount += VISUAL_RESUME
                        elif product_pk in COVER_LETTER_PRODUCT_LIST:
                            amount += COVER_LETTER
                        elif product_pk in SECOND_REGULAR_RESUME_PRODUCT_LIST:
                            amount += SECOND_REGULAR_RESUME

                        amount = int(amount)

                    oi_dict.update({
                        "item_id": pk,
                        "product_name": product_name,
                        "closed_on": closed_on,
                        "combo_discount": combo_discount,
                        "amount": amount,
                        "item_type": "combo",
                    })
                    total_sum += amount

                    item_list.append(oi_dict)
                    p_oi = oi.parent
                    child_items = p_oi.orderitem_set.filter(
                        no_process=False)
                    closed_child_items = p_oi.orderitem_set.filter(
                        no_process=False, oi_status=4).order_by('-closed_on')

                    if child_items.count() == closed_child_items.count() and p_oi.pk not in added_delivery_object:
                        if p_oi.delivery_service and p_oi.delivery_service.slug in delivery_slug_list:
                            amount = 0
                            if p_oi.delivery_service.slug in express_slug_list:
                                amount = EXPRESS
                            elif p_oi.delivery_service.slug in super_express_slug_list:
                                amount = SUPER_EXPRESS
                            d_dict = {
                                "item_id": p_oi.pk,
                                "product_name": p_oi.delivery_service.name,
                                "closed_on": closed_child_items[0].closed_on.date(),
                                "combo_discount": 0,
                                "amount": amount,
                                "item_type": "delivery_service",
                            }
                            item_list.append(d_dict)
                            added_delivery_object.append(p_oi.pk)
                            total_sum += amount
                else:
                    pk = oi.pk
                    product_name = oi.product.get_name
                    closed_on = oi.closed_on.date()
                    combo_discount = 0
                    product_pk = oi.product.pk
                    resuem_writing_ois = oi.order.orderitems.filter(
                        product__type_flow__in=[1, 12])
                    if product_pk in VISUAL_RESUME_PRODUCT_LIST and resuem_writing_ois.exists():
                        amount = VISUAL_RESUME
                    elif product_pk in COVER_LETTER_PRODUCT_LIST and resuem_writing_ois.exists():
                        amount = COVER_LETTER
                    elif product_pk in SECOND_REGULAR_RESUME_PRODUCT_LIST and resuem_writing_ois.exists():
                        amount = SECOND_REGULAR_RESUME
                    else:
                        exp_code = oi.get_exp()
                        if not exp_code:
                            exp_code = 'FR'
                        if oi.product.type_flow == 8:
                            starter_value = LINKEDIN_STARTER_VALUE
                            value_dict = linkedin_dict.get(exp_code, {})
                        else:
                            starter_value = WRITING_STARTER_VALUE
                            value_dict = writing_dict.get(exp_code, {})

                        amount = starter_value
                        if value_dict and value_dict.get(user_type):
                            amount = (starter_value * value_dict.get(user_type)) / 100

                        if product_pk in VISUAL_RESUME_PRODUCT_LIST:
                            amount += VISUAL_RESUME
                        elif product_pk in COVER_LETTER_PRODUCT_LIST:
                            amount += COVER_LETTER
                        elif product_pk in SECOND_REGULAR_RESUME_PRODUCT_LIST:
                            amount += SECOND_REGULAR_RESUME

                        amount = int(amount)

                    oi_dict.update({
                        "item_id": pk,
                        "product_name": product_name,
                        "closed_on": closed_on,
                        "combo_discount": combo_discount,
                        "amount": amount,
                        "item_type": "standalone",
                    })
                    item_list.append(oi_dict)
                    total_sum += amount

                    if oi.delivery_service and oi.delivery_service.slug in delivery_slug_list:
                        amount = 0
                        if oi.delivery_service.slug in express_slug_list:
                            amount = EXPRESS
                        elif oi.delivery_service.slug in super_express_slug_list:
                            amount = SUPER_EXPRESS
                        d_dict = {
                            "item_id": oi.pk,
                            "product_name": oi.delivery_service.name,
                            "closed_on": closed_on,
                            "combo_discount": 0,
                            "amount": amount,
                            "item_type": "delivery_service",
                        }
                        item_list.append(d_dict)
                        total_sum += amount
        
        data.update({
            "error": error,
        })
        return data

    def calculate_writer_invoice(self, user=None, invoice_date=None):
        if not user:
            user = self.request.user
        if not invoice_date:
            today_date = datetime.datetime.now().date()
            today_date = today_date.replace(day=1)
            prev_month = today_date - datetime.timedelta(days=1)
            invoice_date = prev_month

        if user:
            data = self.get_context_writer_invoice(
                user=user, invoice_date=invoice_date)

    def save_writer_invoice_pdf(self, user=None, invoice_date=None):
        data = {}
        import ipdb; ipdb.set_trace()
        try:
            if not user:
                try:
                    user = self.request.user
                except:
                   pass

            if not invoice_date:
                today_date = datetime.datetime.now().date()
                today_date = today_date.replace(day=1)
                prev_month = today_date - datetime.timedelta(days=1)
                invoice_date = prev_month

            data = self.get_context_writer_invoice(
                user=user, invoice_date=invoice_date)
            error = data.get("error", "")

            if not error:
                pdf_file = self.generate_pdf(
                    context_dict=data,
                    template_src='invoice/writer_invoice.html')
                full_path = "user/{user_pk}/{month}_{year}/".format(
                    user_pk=user.pk, month=invoice_date.month,
                    year=invoice_date.year)
                file_name = 'invoice-' + str(user.name) + '-'\
                    + timezone.now().strftime('%d%m%Y') + '.pdf'
                if not os.path.exists(settings.INVOICE_DIR + full_path):
                    os.makedirs(settings.INVOICE_DIR + full_path)
                dest = open(
                    settings.INVOICE_DIR + full_path + file_name, 'wb')
                pdf_file = SimpleUploadedFile(
                    file_name, pdf_file,
                    content_type='application/pdf')
                for chunk in pdf_file.chunks():
                    dest.write(chunk)
                dest.close()
                user.userprofile.invoice = full_path + file_name
                user.save()
                return data
        except Exception as e:
            logging.getLogger('error_log').error("%(msg)s : %(err)s" % {'msg': 'Contact Tech ERROR', 'err': e})
        return data


class RegistrationLoginApi(object):

    @staticmethod
    def user_registration(post_data):
        response_json = {"response": "exist_user"}
        post_url = "{}/api/v2/web/candidate-profiles/?format=json".format(settings.SHINE_SITE)
        try:
            country_obj = Country.objects.get(phone=post_data['country_code'])
        except Country.DoesNotExist:
            country_obj = Country.objects.get(phone='91')

        headers = {'Content-Type': 'application/json'}
        post_data.update({"country_code": country_obj.phone})
        try:
            response = requests.post(
                post_url, data=json.dumps(post_data), headers=headers)

            if response.status_code == 201:
                response_json = response.json()
                response_json.update({'response': "new_user"})

            elif "non_field_errors" in response.json():
                response_json = response.json()
                response_json.update({'response': "exist_user"})

            elif response.status_code == 400:
                response_json = response.json()
                response_json.update({'response': "form_error"})

        except Exception as e:
            logging.getLogger('error_log').error("Error getting response from shine for"
                                                 " registration. %s " % str(e))

        return response_json

    @staticmethod
    def user_login(login_dict):
        response_json = {"response": False}
        post_url = "{}/api/v2/user/access/?format=json".format(settings.SHINE_SITE)

        headers = {'Content-Type': 'application/json'}
        try:
            response = requests.post(
                post_url, data=json.dumps(login_dict), headers=headers)

            if response.status_code == 201:
                response_json = response.json()
                response_json.update({'response': "login_user"})

            elif "non_field_errors" in response.json():
                response_json = response.json()
                response_json.update({'response': "error_pass"})

            elif response.status_code == 400:
                response_json = response.json()
                response_json.update({'response': "form_error"})

        except Exception as e:
            logging.getLogger('error_log').error("Error in getting response from shine for login. %s " % str(e))

        return response_json

    @staticmethod
    def check_email_exist(email):
        response_json = {"exists": False}
        email_url = "{}/api/v3/email-exists/?email={}&format=json".format(settings.SHINE_SITE, email)
        headers = {'Content-Type': 'application/json'}
        try:
            response = requests.get(email_url, headers=headers)
            if response.status_code == 200:
                response_json = response.json()

            elif response.status_code:
                logging.getLogger('error_log').error(
                    "Error in getting response from shine for existing email check. ""%s " % str(response.status_code))
        except Exception as e:
            logging.getLogger('error_log').error("Error in getting response from shine for existing email check. "
                                                 "%s " % str(e))
        return response_json

    @staticmethod
    def reset_update(data_dict):
        
        response_json = {"response": False}
        post_data = {}

        post_url = "{}/api/v2/career-plus/login/change-password/?format=json".format(settings.SHINE_SITE)

        post_data.update({
            'email': data_dict.get('email'),
            'password':data_dict.get('new_password1'),
            'confirm_password':data_dict.get('new_password2')
        })
        request_header = ShineCandidateDetail().get_api_headers(token=None)
        request_header.update({'Content-Type':'application/json'})
        try:
            response = requests.post(post_url, data=json.dumps(post_data), headers=request_header)
            if response.status_code == 201:
                response_json = response.json()
                response_json.update({'response':True})

            if response.status_code == 400:
                response_json = response.json()
                response_json.update({'status_code':response.status_code})
                logging.getLogger('error_log').error(
                    "Error in getting response from shine for existing email check. ""%s " % str(response.status_code))
        except Exception as e:
            logging.getLogger('error_log').error("Error in getting response from shine for existing email check. "
                                                 "%s " % str(e))
        return response_json

    @staticmethod
    def social_login(data_dict):
        response_json = {"response": False}
        post_url = None
        post_data = {}
        if data_dict.get('key') == 'fb':
            post_data = {
                'access_token': data_dict.get('accessToken', ''),
                'expires_on': data_dict.get('expiresIn', '')
            }
            post_url = "{}/api/v2/facebook/login/?format=json".format(settings.SHINE_SITE)

        elif data_dict.get('key') == 'gplus':
            post_data = {
                'access_token': data_dict.get('accessToken', ''),
                'expires_on': data_dict.get('expiresIn', '')
            }
            post_url = "{}/api/v2/google-plus/login/?format=json".format(settings.SHINE_SITE)

        elif data_dict.get('key') == 'linkedin':
            post_data = {
                'token': data_dict.get('access_token', ''),
                'expires_in': data_dict.get('expires_in', '')
            }
            post_url = "{}/api/v2/linkedin/login/?format=json".format(settings.SHINE_SITE)

        try:
            request_header = ShineCandidateDetail().get_api_headers(token=None)
            request_header.update({'Content-Type':'application/json'})
            response = requests.post(post_url, data=json.dumps(post_data), headers=request_header)
            if response.status_code == 201:
                response_json = response.json()
                response_json.update({'response':True})

            if response.status_code == 400:
                response_json = response.json()
                response_json.update({'status_code':response.status_code})
                logging.getLogger('error_log').error(
                    "Error in getting response from shine for existing email check. ""%s " % str(response.status_code))
        except Exception as e:
            logging.getLogger('error_log').error("Error in getting response from shine for existing email check. "
                                                 "%s " % str(e))
        return response_json


class UserMixin(object):
    def get_client_ip(self, request):
        try:
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')
            return ip
        except:
            pass
        return None

    def get_client_country(self, request):
        g = GeoIP()
        ip = self.get_client_ip(request)
        try:
            if ip:
                code2 = g.country(ip)['country_code']
            else:
                code2 = 'IN'
        except:
            code2 = 'IN'

        if not code2:
            code2 = 'IN'

        code2 = code2.upper()

        try:
            country_objs = Country.objects.filter(code2=code2)
            country_obj = country_objs[0]
        except:
            country_obj = Country.objects.get(phone='91')

        return country_obj



