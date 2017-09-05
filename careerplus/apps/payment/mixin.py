from datetime import datetime

from django.core.urlresolvers import reverse

from order.functions import (
    payment_pending_mailer,
    pending_item_email,
    payment_realisation_mailer,
    process_mailer,)


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
            x_mailertag = "CASH_PAYMENT"
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

            x_mailertag = "CCAVENUE_PAYMENT"
            return_parameter = reverse('payment:thank-you')

        elif payment_type == "CHEQUE":
            x_mailertag = "CHEQUE_PAYMENT"
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

            x_mailertag = "MOBIKWIK_PAYMENT"
            return_parameter = reverse('payment:thank-you')

        if order:
            request.session['order_pk'] = order.pk
            process_mailer(order=order)
            payment_pending_mailer(order=order)
            pending_item_email(order=order)
            payment_realisation_mailer(order=order)

            if return_parameter:
                return return_parameter
            else:
                return '/'

        raise Exception('Order Not Found for order type - %s' % payment_type)
