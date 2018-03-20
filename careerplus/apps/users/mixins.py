import requests
import json
import logging
import os
import datetime
import calendar

from django.contrib.gis.geoip import GeoIP
from django.conf import settings
from django.utils import timezone
from shine.core import ShineCandidateDetail
from django.core.files.uploadedfile import SimpleUploadedFile

from geolocation.models import Country
from order.models import OrderItem
from core.mixins import InvoiceGenerate
from core.library.gcloud.custom_cloud_storage import GCPInvoiceStorage

from .choices import (
    WRITING_STARTER_VALUE, RESUME_WRITING_MATRIX_DICT,
    LINKEDIN_STARTER_VALUE, LINKEDIN_WRITING_MATRIX_DICT,
    EXPRESS, SUPER_EXPRESS, VISUAL_RESUME, COVER_LETTER,
    COUNTRY_SPCIFIC_VARIATION,
    SECOND_REGULAR_RESUME, DISCOUNT_ALLOCATION_DAYS,
    COMBO_DISCOUNT, REGULAR_SLA, EXPRESS_SLA, SUPER_EXPRESS_SLA,
    PASS_PERCENTAGE, INCENTIVE_PASS_PERCENTAGE,
    PENALTY_PERCENTAGE, INCENTIVE_PERCENTAGE
)

VISUAL_RESUME_PRODUCT_LIST = settings.VISUAL_RESUME_PRODUCT_LIST
SECOND_REGULAR_RESUME_PRODUCT_LIST = settings.SECOND_REGULAR_RESUME_PRODUCT_LIST
COVER_LETTER_PRODUCT_LIST = settings.COVER_LETTER_PRODUCT_LIST


class WriterInvoiceMixin(object):
    def __init__(self):
        self.combo_discount_object = set()  # for discount combo, eithr resume or linkedin

    def get_combo_discount(self, oi=None, invoice_date=None, user_type=None):
        # linked + resume bought by same user assigned to same writer
        combo_discount = 0
        linkedin_dict = LINKEDIN_WRITING_MATRIX_DICT
        if oi.assigned_to:
            assigned_to = oi.assigned_to
            assigned_date = oi.assigned_date
            if not assigned_date:
                ops = oi.orderitemoperation_set.filter(oi_status=1).order_by('id')
                if ops.exists():
                    assigned_date = ops[0].created
                else:
                    assigned_date = datetime.datetime.today()
        else:
            oi_assigned = oi.orderitem_set.all().exclude(
                assigned_to=None)
            assigned_to = oi_assigned[0].assigned_to
            assigned_date = oi_assigned[0].assigned_date
            if not assigned_date:
                ops = oi_assigned[0].orderitemoperation_set.filter(oi_status=1).order_by('id')
                if ops.exists():
                    assigned_date = ops[0].created
                else:
                    assigned_date = datetime.datetime.today()

        start_date = assigned_date - datetime.timedelta(days=DISCOUNT_ALLOCATION_DAYS)
        end_date = assigned_date + datetime.timedelta(days=DISCOUNT_ALLOCATION_DAYS)
        if oi and invoice_date and assigned_date and user_type:
            if oi.product and oi.product.type_flow in [1, 12, 13]:
                prev_month = invoice_date.replace(day=1)
                prev_month = prev_month - datetime.timedelta(days=1)
                _, last_day = calendar.monthrange(
                    prev_month.year, prev_month.month)
                prev_month = datetime.date(prev_month.year, prev_month.month, last_day)

                linkedin_ois = OrderItem.objects.filter(
                    order__candidate_id=oi.order.candidate_id,
                    product__type_flow=8,
                    oi_status=4,
                    assigned_to=assigned_to,
                    assigned_date__range=[start_date, end_date],
                    closed_on__lte=prev_month).order_by('-id')
                if linkedin_ois.exists():
                    linkedin_obj = linkedin_ois[0]
                    writing_ois = linkedin_obj.order.orderitems.filter(
                        assigned_to=assigned_to,
                        product__type_flow__in=[1, 12, 13]).exclude(
                        product__id__in=COVER_LETTER_PRODUCT_LIST)
                    if writing_ois.exists():
                        linkedin_obj = None
                    else:
                        assigned_to = linkedin_obj.assigned_to
                        assigned_date = linkedin_obj.assigned_date
                        start_date = assigned_date - datetime.timedelta(days=DISCOUNT_ALLOCATION_DAYS)
                        end_date = assigned_date + datetime.timedelta(days=DISCOUNT_ALLOCATION_DAYS)
                        closed_on = linkedin_obj.closed_on
                        _, last_day = calendar.monthrange(
                            closed_on.year, closed_on.month)
                        closed_on_last = datetime.date(
                            closed_on.year, closed_on.month, last_day)
                        writing_ois = OrderItem.objects.filter(
                            order__candidate_id=oi.order.candidate_id,
                            product__type_flow__in=[1, 12, 13],
                            oi_status=4,
                            assigned_to=assigned_to,
                            assigned_date__range=[start_date, end_date],
                            closed_on__lte=closed_on_last).exclude(
                            product__id__in=COVER_LETTER_PRODUCT_LIST)

                        if writing_ois.exists():
                            linkedin_obj = None

                    if linkedin_obj:
                        if linkedin_obj.pk not in self.combo_discount_object:
                            exp_code = linkedin_obj.product.get_exp()
                            if not exp_code:
                                exp_code = 'FR'
                            value_dict = linkedin_dict.get(exp_code, {})
                            starter_value = LINKEDIN_STARTER_VALUE
                            linkedin_amount = starter_value
                            if value_dict and value_dict.get(user_type):
                                linkedin_amount = (starter_value * value_dict.get(user_type)) / 100
                                linkedin_amount = int(linkedin_amount)

                            combo_discount = linkedin_amount * (COMBO_DISCOUNT / 100)
                            self.combo_discount_object.add(linkedin_obj.pk)
            elif oi.product.type_flow == 8:
                writing_ois = oi.order.orderitems.filter(
                    assigned_to=assigned_to,
                    product__type_flow__in=[1, 12, 13]).exclude(
                    product__id__in=COVER_LETTER_PRODUCT_LIST)
                exp_code = oi.product.get_exp()
                if not exp_code:
                    exp_code = 'FR'
                value_dict = linkedin_dict.get(exp_code, {})
                starter_value = LINKEDIN_STARTER_VALUE
                linkedin_amount = starter_value
                if value_dict and value_dict.get(user_type):
                    linkedin_amount = (starter_value * value_dict.get(user_type)) / 100
                    linkedin_amount = int(linkedin_amount)
                if writing_ois.exists() and oi.pk not in self.combo_discount_object:
                    combo_discount = (linkedin_amount * COMBO_DISCOUNT) / 100
                    self.combo_discount_object.add(oi.pk)
                else:
                    _, last_day = calendar.monthrange(
                        invoice_date.year, invoice_date.month) 
                    last_invoice_date = datetime.date(
                        invoice_date.year, invoice_date.month, last_day)
                    writing_ois = OrderItem.objects.filter(
                        order__candidate_id=oi.order.candidate_id,
                        product__type_flow__in=[1, 12, 13],
                        oi_status=4,
                        assigned_to=assigned_to,
                        assigned_date__range=[start_date, end_date],
                        closed_on__lte=last_invoice_date).exclude(
                        product__id__in=COVER_LETTER_PRODUCT_LIST)
                    if writing_ois.exists() and oi.pk not in self.combo_discount_object:
                        combo_discount = (linkedin_amount * COMBO_DISCOUNT) / 100
                        self.combo_discount_object.add(oi.pk)

        combo_discount = int(combo_discount)

        return combo_discount

    def get_context_writer_invoice(self, user=None, invoice_date=None):
        item_list = []
        error = ''
        data = {'item_list': item_list, "error": error}
        msg = 'Few writer mandatory fields are not available for invoice generation please contact support'

        if not user:
            error = "Provide valid writer details"

        if not invoice_date:
            error = 'Provide valid invoice date'

        writer_name, writer_pan = '', ''
        writer_gstin, writer_address = '', ''
        writer_group, writer_po_number = 0, ''

        if user and user.userprofile and not error:
            if user.name and not error:
                writer_name = user.name
            elif not error:
                error = msg

            if user.userprofile.pan_no and not error:
                writer_pan = user.userprofile.pan_no
            elif not error:
                error = msg

            if user.userprofile.gstin and not error:
                writer_gstin = user.userprofile.gstin
            else:
                writer_gstin = ''  # optional

            if user.userprofile.address and not error:
                writer_address = user.userprofile.address
            elif not error:
                error = msg

            if user.userprofile.writer_type and not error:
                writer_group = user.userprofile.writer_type
            elif not error:
                error = msg

            if user.userprofile.po_number and not error:
                writer_po_number = user.userprofile.po_number
            elif not error:
                error = msg

            valid_from = user.userprofile.valid_from
            valid_to = user.userprofile.valid_to
            if valid_from and valid_to and valid_from < valid_to \
                and invoice_date and invoice_date >= valid_from and invoice_date <= valid_to:
                pass
            elif not error:
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
            _, last_day = calendar.monthrange(
                invoice_date.year, invoice_date.month)  #  _  return weekday of first day of the month
            last_invoice_date = datetime.date(
                invoice_date.year, invoice_date.month, last_day)
            first_invoice_date = datetime.date(
                invoice_date.year, invoice_date.month, 1)
            last_invoice_date = last_invoice_date + datetime.timedelta(
                days=1)

            orderitems = OrderItem.objects.filter(
                order__status__in=[1, 3],
                product__type_flow__in=[1, 8, 12, 13],
                oi_status=4, assigned_to=user,
                closed_on__range=[first_invoice_date, last_invoice_date],
                no_process=False).select_related('product').order_by('id')

            writing_dict = RESUME_WRITING_MATRIX_DICT
            linkedin_dict = LINKEDIN_WRITING_MATRIX_DICT
            express_slug_list = settings.EXPRESS_DELIVERY_SLUG
            super_express_slug_list = settings.SUPER_EXPRESS_DELIVERY_SLUG
            delivery_slug_list = express_slug_list + super_express_slug_list

            added_base_object = []  # for country specific resume
            added_delivery_object = []  # for delivery price only for parent item 

            user_type = 1
            if user.userprofile.wt_changed_date:
                changed_date = user.userprofile.wt_changed_date
                changed_date = changed_date.replace(day=1)
                changed_date = changed_date + datetime.timedelta(days=31)
                changed_date = changed_date.replace(day=1)
                if invoice_date >= changed_date:
                    user_type = user.userprofile.writer_type
                else:
                    user_type = user.userprofile.last_writer_type
            else:
                user_type = user.userprofile.writer_type if user.userprofile else 1

            total_combo_discount = 0
            total_sum = 0
            success_closure = 0

            order_before = datetime.date(2017, 11, 3)

            for oi in orderitems:
                process = False
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

                if oi.created.date() < order_before:
                    oi_dict = {}
                    oi_dict.update({
                        "item_id": oi.pk,
                        "product_name": oi.product.get_name,
                        "closed_on": oi.closed_on.date(),
                        "combo_discount": 0,
                        "amount": 0,
                        "item_type": "older",
                    })
                    item_list.append(oi_dict)
                    continue

                if oi.is_variation:
                    p_oi = oi.parent
                    variations = p_oi.orderitem_set.filter(
                        is_variation=True, no_process=False)
                    closed_variations = p_oi.orderitem_set.filter(
                        is_variation=True, no_process=False, oi_status=4).order_by('-closed_on')

                    if variations.count() == closed_variations.count() and p_oi.pk not in added_base_object:
                        p_oi_dict = {}
                        pk = p_oi.pk
                        product_name = p_oi.product.get_name
                        closed_on = closed_variations[0].closed_on.date()
                        combo_discount = 0
                        exp_code = p_oi.product.get_exp()
                        if not exp_code:
                            exp_code = 'FR'
                        value_dict = writing_dict.get(exp_code, {})
                        starter_value = WRITING_STARTER_VALUE
                        amount = starter_value
                        if value_dict and value_dict.get(user_type):
                            amount = (starter_value * value_dict.get(user_type)) / 100
                            amount = int(amount)

                        # combo discount calculation
                        combo_discount = self.get_combo_discount(
                            oi=p_oi, invoice_date=invoice_date,
                            user_type=user_type)
                        total_combo_discount += combo_discount

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
                            product_name = p_oi.product.get_name + ' - ' + p_oi.delivery_service.name
                            d_dict = {
                                "item_id": p_oi.pk,
                                "product_name": product_name,
                                "closed_on": closed_on,
                                "combo_discount": 0,
                                "amount": amount,
                                "item_type": "delivery_service",
                            }
                            item_list.append(d_dict)
                            added_delivery_object.append(p_oi.pk)
                            total_sum += amount

                    pk = oi.pk
                    product_name = oi.parent.product.get_name + " - " + oi.product.get_name
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

                    process = True

                elif oi.is_addon:
                    pk = oi.pk
                    product_name = oi.product.get_name
                    closed_on = oi.closed_on.date()
                    combo_discount = 0
                    product_pk = oi.product.pk
                    amount = 0
                    if product_pk in VISUAL_RESUME_PRODUCT_LIST:
                        amount = VISUAL_RESUME
                        # combo discount calculation
                        combo_discount = self.get_combo_discount(
                            oi=oi, invoice_date=invoice_date,
                            user_type=user_type)
                        total_combo_discount += combo_discount
                        process = True
                    elif product_pk in COVER_LETTER_PRODUCT_LIST:
                        amount = COVER_LETTER
                        process = True
                    elif product_pk in SECOND_REGULAR_RESUME_PRODUCT_LIST:
                        amount = SECOND_REGULAR_RESUME
                        # combo discount calculation
                        combo_discount = self.get_combo_discount(
                            oi=oi, invoice_date=invoice_date,
                            user_type=user_type)
                        total_combo_discount += combo_discount
                        process = True
                    
                    if process:
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
                        # combo discount calculation
                        combo_discount = self.get_combo_discount(
                            oi=oi, invoice_date=invoice_date,
                            user_type=user_type)
                        total_combo_discount += combo_discount
                    elif product_pk in COVER_LETTER_PRODUCT_LIST and resuem_writing_ois.exists():
                        amount = COVER_LETTER
                    elif product_pk in SECOND_REGULAR_RESUME_PRODUCT_LIST and resuem_writing_ois.exists():
                        amount = SECOND_REGULAR_RESUME
                        # combo discount calculation
                        combo_discount = self.get_combo_discount(
                            oi=oi, invoice_date=invoice_date,
                            user_type=user_type)
                        total_combo_discount += combo_discount
                    else:
                        exp_code = oi.product.get_exp()
                        if not exp_code:
                            exp_code = 'FR'
                        if oi.product.type_flow == 8:
                            value_dict = linkedin_dict.get(exp_code, {})
                            starter_value = LINKEDIN_STARTER_VALUE
                        else:
                            value_dict = writing_dict.get(exp_code, {})
                            starter_value = WRITING_STARTER_VALUE

                        amount = starter_value
                        if value_dict and value_dict.get(user_type):
                            amount = (starter_value * value_dict.get(user_type)) / 100

                        if product_pk in VISUAL_RESUME_PRODUCT_LIST:
                            amount += VISUAL_RESUME
                        elif product_pk in COVER_LETTER_PRODUCT_LIST:
                            amount = COVER_LETTER
                        elif product_pk in SECOND_REGULAR_RESUME_PRODUCT_LIST:
                            amount += SECOND_REGULAR_RESUME

                        amount = int(amount)

                        # combo discount calculation
                        combo_discount = self.get_combo_discount(
                            oi=oi, invoice_date=invoice_date,
                            user_type=user_type)
                        total_combo_discount += combo_discount

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
                            product_name = p_oi.product.get_name + ' - ' + p_oi.delivery_service.name
                            d_dict = {
                                "item_id": p_oi.pk,
                                "product_name": product_name,
                                "closed_on": closed_child_items[0].closed_on.date(),
                                "combo_discount": 0,
                                "amount": amount,
                                "item_type": "delivery_service",
                            }
                            item_list.append(d_dict)
                            added_delivery_object.append(p_oi.pk)
                            total_sum += amount
                    process = True
                elif not process:
                    pk = oi.pk
                    product_name = oi.product.get_name
                    closed_on = oi.closed_on.date()
                    combo_discount = 0
                    product_pk = oi.product.pk
                    resuem_writing_ois = oi.order.orderitems.filter(
                        product__type_flow__in=[1, 12])
                    if product_pk in VISUAL_RESUME_PRODUCT_LIST and resuem_writing_ois.exists():
                        amount = VISUAL_RESUME
                        # combo discount calculation
                        combo_discount = self.get_combo_discount(
                            oi=oi, invoice_date=invoice_date,
                            user_type=user_type)
                        total_combo_discount += combo_discount
                    elif product_pk in COVER_LETTER_PRODUCT_LIST:
                        amount = COVER_LETTER
                    elif product_pk in SECOND_REGULAR_RESUME_PRODUCT_LIST and resuem_writing_ois.exists():
                        amount = SECOND_REGULAR_RESUME
                        # combo discount calculation
                        combo_discount = self.get_combo_discount(
                            oi=oi, invoice_date=invoice_date,
                            user_type=user_type)
                        total_combo_discount += combo_discount
                    else:
                        exp_code = oi.product.get_exp()
                        if not exp_code:
                            exp_code = 'FR'
                        if oi.product.type_flow == 8:
                            value_dict = linkedin_dict.get(exp_code, {})
                            starter_value = LINKEDIN_STARTER_VALUE
                        else:
                            value_dict = writing_dict.get(exp_code, {})
                            starter_value = WRITING_STARTER_VALUE

                        amount = starter_value
                        if value_dict and value_dict.get(user_type):
                            amount = (starter_value * value_dict.get(user_type)) / 100

                        if product_pk in VISUAL_RESUME_PRODUCT_LIST:
                            amount += VISUAL_RESUME
                        elif product_pk in COVER_LETTER_PRODUCT_LIST:
                            amount = COVER_LETTER
                        elif product_pk in SECOND_REGULAR_RESUME_PRODUCT_LIST:
                            amount += SECOND_REGULAR_RESUME

                        amount = int(amount)
                        # combo discount calculation
                        combo_discount = self.get_combo_discount(
                            oi=oi, invoice_date=invoice_date,
                            user_type=user_type)
                        total_combo_discount += combo_discount

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
                        product_name = oi.product.get_name + ' - ' + oi.delivery_service.name
                        d_dict = {
                            "item_id": oi.pk,
                            "product_name": product_name,
                            "closed_on": closed_on,
                            "combo_discount": 0,
                            "amount": amount,
                            "item_type": "delivery_service",
                        }
                        item_list.append(d_dict)
                        total_sum += amount

                    process = True

            # penalty and incentive calc
            penalty = 0
            incentive = 0
            total_item = orderitems.count()
            total = total_sum - total_combo_discount
            total_payable = total
            if total_item:
                success_per = (success_closure / total_item) * 100
                success_per = int(success_per)

                if success_per >= INCENTIVE_PASS_PERCENTAGE:
                    incentive = (total * INCENTIVE_PERCENTAGE) / 100
                    incentive = int(incentive)
                    total_payable += incentive
                elif success_per < PASS_PERCENTAGE:
                    penalty = (total * PENALTY_PERCENTAGE) / 100
                    penalty = int(penalty)
                    total_payable -= penalty

            invoice_no = 'INV' + str(user.pk) + '-' + invoice_date.strftime('%d%m%Y')
            data.update({
                "item_list": item_list,
                "sub_total": total_sum,
                "total_combo_discount": total_combo_discount,
                "total": total,
                "total_payable": total_payable,
                "penalty": penalty,
                "incentive": incentive,
                "penalty_per": PENALTY_PERCENTAGE,
                "incentive_per": INCENTIVE_PERCENTAGE,
                "invoice_date": invoice_date,
                "invoice_no": invoice_no,
            })

        data.update({
            "error": error,
        })
        return data

    def calculate_writer_invoice(self, user=None, invoice_date=None):
        if not user:
            try:
                user = self.request.user
            except user.DoesNotExist:
                logging.getLogger('error_log').error('User  not found ')
                pass
        if not invoice_date:
            today_date = datetime.datetime.now().date()
            today_date = today_date.replace(day=1)
            prev_month = today_date - datetime.timedelta(days=1)
            invoice_date = prev_month

        data = {}
        if user:
            data = self.get_context_writer_invoice(
                user=user, invoice_date=invoice_date)
        return data

    def save_writer_invoice_pdf(self, user=None, invoice_date=None):
        error = ""
        data = {"error": error}
        try:
            if not user:
                try:
                    user = self.request.user
                except user.DoesNotExist:
                    logging.getLogger('error_log').error('User  not found ')
                    pass

            if not invoice_date:
                today_date = datetime.datetime.now().date()
                today_date = today_date.replace(day=1)
                prev_month = today_date - datetime.timedelta(days=1)
                invoice_date = prev_month
            data = self.get_context_writer_invoice(
                user=user, invoice_date=invoice_date)
            error = data.get("error", "")

            item_list = data.get('item_list', [])
            # item_list = [5] * 60
            # data.update({'item_list': item_list})

            if not error and item_list:
                pdf_file = InvoiceGenerate().generate_pdf(
                    context_dict=data,
                    template_src='invoice/writer_invoice.html')
                path = "invoice/user/{user_pk}/{month}_{year}/".format(
                    user_pk=user.pk, month=invoice_date.month,
                    year=invoice_date.year)
                file_name = 'invoice-' + str(user.name) + '-'\
                    + timezone.now().strftime('%d%m%Y') + '.pdf'
                pdf_file = SimpleUploadedFile(
                    file_name, pdf_file,
                    content_type='application/pdf')
                GCPInvoiceStorage().save(path + file_name, pdf_file)
                user.userprofile.user_invoice = path + file_name
                user.userprofile.invoice_date = invoice_date
                user.userprofile.save()
                user.save()
                return data
            elif not error and not item_list:
                error = 'No invoice for last month(no item is closed)'

        except Exception as e:
            error = 'something went wrong, try again later.'
            logging.getLogger('error_log').error("%(msg)s : %(err)s" % {'msg': 'Contact Tech ERROR', 'err': e})
        if error:
            data.update({"error": error, })
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
