import time
from datetime import datetime

from django.core.urlresolvers import reverse

from order.models import Order


class PaymentMixin(object):

    def process_payment_method(self, order_type, request, data={}):
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
        order = None

        if order_type == "CASH":
            order = Order.objects.get(pk=request.session.get('order_pk'))
            txn = 'CP%d%s' % (order.pk, int(time.time()))
            # mail_type = mailers_config.MAIL_TYPE[6]
            order_status = 2
            payment_mode = 1
            # sms_type = mailers_config.SMS_TYPE[4]
            x_mailertag = "CASH_PAYMENT"
            return_parameter = reverse('payment:thank-you')

        elif order_type == "CCAVENUE":
            order = Order.objects.get(pk=data.get('order_id'))
            txn = data.get('txn_id')
            order_status = 1
            payment_mode = 7
            payment_date = datetime.now()
            x_mailertag = "CCAVENUE_PAYMENT"
            return_parameter = reverse('payment:thank-you')

        elif order_type == "CHEQUE":
            order = Order.objects.get(pk=request.session.get('order_pk'))
            order.instrument_number = request.POST.get('instrument_number')
            order.instrument_issuer = request.POST.get('instrument_issuer')
            order.instrument_issue_date = request.POST.get(
                'instrument_issue_date')
            txn = 'CP%d%s%s' % (order.pk, int(time.time()), request.POST.get(
                'instrument_number'))
            order_status = 2
            payment_mode = 4
            x_mailertag = "CHEQUE_PAYMENT"
            return_parameter = reverse('payment:thank-you')

        elif order_type == "MOBIKWIK":

            order = Order.objects.get(pk=data.get('order_id'))
            txn = data.get('txn_id')
            order_status = 1
            payment_mode = 6
            payment_date = datetime.now()
            x_mailertag = "MOBIKWIK_PAYMENT"
            return_parameter = reverse('payment:thank-you')

        if order:
            order.txn = txn
            order.status = order_status
            order.payment_mode = payment_mode
            order.payment_date = payment_date if payment_date else None
            order.save()
            request.session['order_pk'] = order.pk

            if return_parameter:
                return return_parameter
            else:
                return order

        raise Exception('Order Not Found for order type - %s' % order_type)
