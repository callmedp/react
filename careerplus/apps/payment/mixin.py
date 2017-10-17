import logging
from datetime import datetime

from django.core.urlresolvers import reverse

from users.tasks import user_register
from core.mixins import InvoiceGenerate
from order.mixins import OrderMixin
from order.tasks import (
    pending_item_email,
    process_mailer,
    payment_pending_mailer,
    payment_realisation_mailer,
)


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

        if order:
            request.session['order_pk'] = order.pk
            if not order.candidate_id:
                user_register.delay(data={}, order=order.pk)

            if order.status == 1:
                order = InvoiceGenerate().save_order_invoice_pdf(order=order)

            # add reward_point in wallet
            OrderMixin().addRewardPointInWallet(order=order)

            try:
                del request.session['cart_pk']
                del request.session['checkout_type']
                self.request.session.modified = True
            except Exception as e:
                logging.getLogger('error_log').error("%s " % str(e))
                pass

            # emails
            process_mailer.apply_async((order.pk,), countdown=900)
            # process_mailer(order=order)
            payment_pending_mailer.delay(order.pk)
            # payment_pending_mailer(order=order)
            pending_item_email.apply_async((order.pk,), countdown=900)
            # pending_item_email(order=order)
            # payment_realisation_mailer(order=order)
            payment_realisation_mailer.delay(order.pk)

            if return_parameter:
                return return_parameter
            else:
                return '/'

        raise Exception('Order Not Found for order type - %s' % payment_type)
