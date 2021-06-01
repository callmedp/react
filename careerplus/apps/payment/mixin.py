import logging
from datetime import datetime
import json

from django.urls import reverse
from django.conf import settings
from django.core.cache import cache

from users.tasks import user_register
# from core.mixins import InvoiceGenerate
# from order.mixins import OrderMixin
from order.tasks import (
    pending_item_email,
    process_mailer,
    payment_pending_mailer,
    payment_realisation_mailer,
    invoice_generation_order,
)
from .tasks import (
    add_reward_point_in_wallet, make_logging_request, 
    make_logging_sk_request, make_logging_amount_request
    )
from ajax.functions import process_background_verification

class PaymentMixin(object):

    def payment_tracking(self, candidate_id, product_list, method, total_amount, total_amount_paid):
        cache_data = cache.get("tracking_payment_action",{})
        c_id_data = cache_data.get(str(candidate_id),{})
        if not c_id_data:
            logging.getLogger('info_log').info("candidate_id {} not being tracked".format(candidate_id))
            return False
        payment_ids = [str(x) for x in product_list]
        products_purchased_by_user = list(c_id_data.keys())
        tracked_purchased_products = list(set(payment_ids) & set(products_purchased_by_user))
        if not tracked_purchased_products:
            logging.getLogger('info_log').info("candidate_id {} not being tracked".format(candidate_id))
            return False
        for prod in tracked_purchased_products:
            prod_data = c_id_data.get(prod, {})
            t_id = prod_data.get('t_id', '')
            products = prod_data.get('products', '')
            domain = prod_data.get('domain', '')
            position = prod_data.get('position', '')
            trigger_point = prod_data.get('trigger_point', '')
            utm_campaign = prod_data.get('utm_campaign', '')
            referal_product = prod_data.get('referal_product', '')
            referal_subproduct = prod_data.get('referal_subproduct', '')
            popup_based_product = prod_data.get('popup_based_product', '')
            recommendation_by = prod_data.get('recommendation_by', '')
            cart_addition = prod_data.get('cart_addition', '')

            if t_id and prod and method:
                make_logging_amount_request.delay(
                    prod, products, t_id, method, position, trigger_point, str(candidate_id), utm_campaign, domain, referal_product, referal_subproduct, total_amount, total_amount_paid, popup_based_product, recommendation_by, cart_addition)
                logging.getLogger('info_log').info('purchase method data: tracking_product_id: {}, product_tracking_mapping_id : {}, tracking_id: {},'
                    'action: {}, position: {}, trigger_point: {}, u_id: {}, utm_campaign: {}, domain: {}, referal_product: {}, referal_subproduct: {},'
                    'total_amount: {}, total_amount_paid: {}, popup_based_product:{}, recommendation_by:{}, cart_addition:{}'.format(prod, products, t_id, method, position,\
                     trigger_point, str(candidate_id), utm_campaign, domain, referal_product, referal_subproduct, total_amount, total_amount_paid, popup_based_product, recommendation_by, cart_addition))
        return True

    def paid_amount_without_tax(self, order):
        original_amount = ''
        tax_config = order.tax_config if order.tax_config else ''
        if not tax_config:
            return ''
        try:
            tax_config = json.loads(tax_config)
        except Exception as e:
            logging.getLogger('error_log').error("invalid data in tax_config for order {}".format(order.id))
        if not isinstance(tax_config, dict):
            return '' 
        total_tax = 0
        for tax in tax_config:
            total_tax += tax_config[tax] 
        total_tax = 1 + total_tax/100

        try:
            original_amount = order.total_incl_tax if order.total_incl_tax else ''
            original_amount = float(original_amount)
        except Exception as e:
            logging.getLogger('error_log').error("invalid data in original_amount for order {}".format(order.id))
        if not original_amount:
            return ''
        original_amount = original_amount/total_tax

        return original_amount


    def process_payment_method(self, payment_type, request, txn_obj, data={}):
        """ This method should be called for adding info to the order.
            return_parameter -- you want to return order as return parameter.
        """

        # email_data = {}
        # sms_data = {}
        return_parameter = None
        payment_date = None
        method = None
        # is_tssc = False
        # mail_type = False
        # sms_type = False
        order = txn_obj.order

        if payment_type == "CASH":
            return_parameter = reverse('payment:thank-you')
            method = "purchase_done_cash"

        elif payment_type == "PAID FREE":
            payment_date = datetime.now()
            payment_mode = 11

            order.status = 1
            order.payment_date = payment_date
            order.save()

            txn_obj.status = 1
            txn_obj.payment_mode = payment_mode
            txn_obj.payment_date = payment_date
            txn_obj.save()

            return_parameter = reverse('payment:thank-you')

        elif payment_type == "REDEEMED":
            payment_date = datetime.now()
            payment_mode = 16

            order.status = 1
            order.payment_date = payment_date
            order.save()

            txn_obj.status = 1
            txn_obj.payment_mode = payment_mode
            txn_obj.payment_date = payment_date
            txn_obj.save()

            return_parameter = reverse('dashboard:dashboard')

            return return_parameter

        elif payment_type == "CCAVENUE":
            payment_date = datetime.now()
            payment_mode = 7

            order.status = 1
            order.payment_date = payment_date
            order.save()

            txn_obj.status = 1
            txn_obj.payment_mode = payment_mode
            txn_obj.payment_date = payment_date
            txn_obj.save()

            method = "purchase_done_card_and_netbanking"

            return_parameter = reverse('payment:thank-you')

        elif payment_type == "PAYU":
            payment_date = datetime.now()
            payment_mode = 13

            order.status = 1
            order.payment_date = payment_date
            order.save()

            txn_obj.status = 1
            txn_obj.payment_mode = payment_mode
            txn_obj.payment_date = payment_date
            txn_obj.save()

            method = "purchase_done_amazon_pay"

            return_parameter = reverse('payment:thank-you')

        elif payment_type == "EPAYLATER":
            payment_date = datetime.now()
            payment_mode = 12

            order.status = 1
            order.payment_date = payment_date
            order.save()

            txn_obj.status = 1
            txn_obj.payment_mode = payment_mode
            txn_obj.payment_date = payment_date
            txn_obj.save()

            return_parameter = reverse('payment:thank-you')
            method = "purchase_done_buy_now_pay_later"

        elif payment_type == "CHEQUE":
            return_parameter = reverse('payment:thank-you')
            method = "purchase_done_cheque"

        elif payment_type == "MOBIKWIK":
            payment_date = datetime.now()
            payment_mode = 6

            order.payment_date = payment_date
            order.status = 1
            order.save()

            txn_obj.status = 1
            txn_obj.payment_mode = payment_mode
            txn_obj.payment_date = payment_date
            txn_obj.save()

            return_parameter = reverse('payment:thank-you')

        elif payment_type == "ZESTMONEY":
            payment_date = datetime.now()
            txn_obj.status = 1
            txn_obj.payment_date = payment_date
            txn_obj.payment_mode = 14
            txn_obj.save()

            order.payment_date = payment_date
            order.status = 1
            order.save()
            method = "purchase_done_zest_money"

        elif payment_type == 'RAZORPAY':
            payment_date = datetime.now()
            txn_obj.status = 1
            txn_obj.payment_date = payment_date
            txn_obj.payment_mode = 15
            txn_obj.razor_payment_id = data.get('razorpay_payment_id')

            txn_obj.razorpay_signature = data.get('razorpay_signature')
            txn_obj.save()

            order.payment_date = payment_date
            order.status = 1
            order.save()
            return_parameter = reverse('payment:thank-you')
            method = "purchase_done_card_and_netbanking"

        if order:
            request.session['order_pk'] = order.pk
            if not order.candidate_id:
                user_register.delay(data={}, order=order.pk)
            tracking_product_id = request.session.get(
                'tracking_product_id', '')
            product_tracking_mapping_id = request.session.get(
                'product_tracking_mapping_id', '')
            tracking_id = request.session.get('tracking_id', '')
            product_availability = request.session.get(
                'product_availability', tracking_product_id)
            trigger_point = request.session.get(
                'trigger_point','')
            u_id = request.session.get(
                'u_id','')
            position = request.session.get(
                'position',1)
            utm_campaign = request.session.get(
                'utm_campaign','')
            referal_product = request.session.get(
            'referal_product','')
            referal_subproduct = request.session.get(
                'referal_subproduct','')
            popup_based_product = request.session.get(
                'popup_based_product','')
            recommendation_by = request.session.get(
                'recommendation_by','')
            cart_addition = request.session.get(
                'cart_addition','')
            
            action = 'purchase_done'
            total_amount = order.total_excl_tax if order.total_excl_tax else ""
            total_amount_paid = self.paid_amount_without_tax(order = order)
            if tracking_id and product_availability and payment_type != "PAID FREE":
                make_logging_amount_request.delay(
                    tracking_product_id, product_tracking_mapping_id, tracking_id, action, position, trigger_point, u_id, utm_campaign, 2, referal_product, referal_subproduct, total_amount, total_amount_paid, popup_based_product, recommendation_by, cart_addition)
                logging.getLogger('info_log').info('purchase done data: tracking_product_id: {}, product_tracking_mapping_id : {}, tracking_id: {},'
                    'action: {}, position: {}, trigger_point: {}, u_id: {}, utm_campaign: {}, domain: {}, referal_product: {}, referal_subproduct: {},'
                     'total_amount: {}, total_amount_paid: {}, popup_based_product:{}, recommendation_by:{}, cart_addition:{}'.format(tracking_product_id, product_tracking_mapping_id, tracking_id,\
                        action, position, trigger_point, u_id, utm_campaign, 2, referal_product, referal_subproduct, total_amount, total_amount_paid, popup_based_product, recommendation_by, cart_addition))
                # if method:
                #     make_logging_sk_request.delay(
                #         tracking_product_id, product_tracking_mapping_id, tracking_id, method, position, trigger_point, u_id, utm_campaign, 2, referal_product, referal_subproduct)
            candidate_id = order.candidate_id
            product_ids = list(order.orderitems.values_list('product__pk',flat=True))
            if candidate_id and product_ids and method:
                self.payment_tracking(candidate_id = candidate_id, product_list = product_ids, method = method, total_amount = total_amount, total_amount_paid = total_amount_paid)

            # order = InvoiceGenerate().save_order_invoice_pdf(order=order)
            invoice_generation_order.delay(order_pk=order.pk)

            if order.status == 1:
                # add reward_point in wallet
                add_reward_point_in_wallet.delay(order_pk=order.pk)
                # OrderMixin().addRewardPointInWallet(order=order)
                process_background_verification.delay(order_pk=order.pk)


            try:
                del request.session['cart_pk']
                del request.session['checkout_type']
                self.request.session.modified = True
                if tracking_id:
                    del request.session['tracking_id']
                if tracking_product_id:
                    del request.session['tracking_product_id']
                if product_tracking_mapping_id:
                    del request.session['product_tracking_mapping_id']
                if product_availability:
                    del request.session['product_availability']
            except Exception as e:
                logging.getLogger('error_log').error(
                    "unable to modify session request %s " % str(e))
                pass

            # emails
            process_mailer.apply_async(
                (order.pk,), countdown=settings.MAIL_COUNTDOWN)
            # process_mailer(order=order)
            payment_pending_mailer.delay(order.pk)
            # payment_pending_mailer(order=order)
            pending_item_email.apply_async(
                (order.pk,), countdown=settings.MAIL_COUNTDOWN)
            # pending_item_email(order=order)
            # payment_realisation_mailer(order=order)
            payment_realisation_mailer.delay(order.pk)

            if return_parameter:
                return return_parameter
            else:
                return '/'

        raise Exception('Order Not Found for order type - %s' % payment_type)
