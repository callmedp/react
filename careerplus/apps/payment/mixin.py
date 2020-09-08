import logging
from datetime import datetime

from django.urls import reverse
from django.conf import settings

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
from .tasks import add_reward_point_in_wallet, make_logging_request


class PaymentMixin(object):

    def process_payment_method(self, payment_type, request, txn_obj, data={}):
        """ This method should be called for adding info to the order.
            return_parameter -- you want to return order as return parameter.
        """

        # email_data = {}
        # sms_data = {}
        return_parameter = None
        payment_date = None
        # is_tssc = False
        # mail_type = False
        # sms_type = False
        order = txn_obj.order

        if payment_type == "CASH":
            return_parameter = reverse('payment:thank-you')

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

        elif payment_type == "CHEQUE":
            return_parameter = reverse('payment:thank-you')

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
                'product_availability', '')
            trigger_point = self.request.session.get(
                'trigger_point','')
            u_id = self.request.session.get(
                'u_id','')
            position = self.request.session.get(
                'position',1)
            utm_campaign = self.request.session.get(
                'utm_campaign','')
            
            action = 'purchase_done'
            if tracking_id and product_availability:
                make_logging_request.delay(
                    tracking_product_id, product_tracking_mapping_id, tracking_id, action,position, trigger_point, u_id, utm_campaign, 2)

            # order = InvoiceGenerate().save_order_invoice_pdf(order=order)
            invoice_generation_order.delay(order_pk=order.pk)

            if order.status == 1:
                # add reward_point in wallet
                add_reward_point_in_wallet.delay(order_pk=order.pk)
                # OrderMixin().addRewardPointInWallet(order=order)

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
