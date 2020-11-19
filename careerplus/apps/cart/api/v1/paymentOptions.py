# third party imports
import logging
import json
import time
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from cart.tasks import create_lead_on_crm
from cart.models import Cart
from payment.models import PaymentTxn
from order.mixins import OrderMixin
from payment.mixin import PaymentMixin
from geolocation.models import Country
from payment.forms import PayByCheckForm
from payment.utils import PayuPaymentUtil


class PaymentOptionsApiView(APIView, OrderMixin, PaymentMixin):
    permission_classes = ()
    authentication_classes = ()
    serializer_classes = None

    def get_state_list(self):
        india_obj = Country.objects.filter(phone='91')
        state_choices = []
        if india_obj:
            india_obj = india_obj[0]
            states = india_obj.state_set.all().order_by('name')
            for st in states:
                state_choices.append([st.id, st.name])

        return state_choices

    def get(self, request, *args, **kwargs):
        cart_pk = self.request.GET.get('cart_pk')
        cart_obj = self.getCartObject()
        if not cart_pk:
            return Response({'redirect': '/'}, status=status.HTTP_200_OK)
        try:
            cart_obj = Cart.objects.get(pk=cart_pk)
            if not cart_obj.owner_id:
                return Response({'redirect': 'cart/payment-summary'}, status=status.HTTP_200_OK)
        except Exception as e:
            logging.getLogger('error_log').error(
                'unable to get cart object%s' % str(e))
            return Response({'redirect': '/'}, status=status.HTTP_200_OK)

        if not cart_obj.lineitems.filter(no_process=False).exists():
            return Response({'redirect': '/'}, status=status.HTTP_200_OK)

        cart_obj.payment_page = True
        # handling the resume.shine
        if not cart_obj.site:
            cart_obj.site = 1

        cart_obj.save()

        payment_dict = self.getPayableAmount(cart_obj)
        source_type = "payment_drop_out"
        candidate_id = self.request.GET.get('candidate_id')
        if cart_obj.owner_id == candidate_id and not request.ip_restricted:
            first_name = cart_obj.first_name if cart_obj.first_name else ''
            last_name = cart_obj.last_name if cart_obj.last_name else ''
            name = "{}{}".format(first_name, last_name)
            create_lead_on_crm.apply_async(
                (cart_obj.pk, source_type, name),
                countdown=settings.PAYMENT_DROP_LEAD)
        total_payable_amount = payment_dict.get('total_payable_amount')
        if total_payable_amount <= 0:
            order = self.createOrder(cart_obj)
            self.closeCartObject(cart_obj)
            if order:
                txn = 'CP%d%s' % (order.pk, int(time.time()))
                pay_txn = PaymentTxn.objects.create(
                    txn=txn,
                    order=order,
                    cart=cart_obj,
                    status=0,
                    payment_mode=11,
                    currency=order.currency,
                    txn_amount=order.total_incl_tax,
                )
                payment_type = "PAID FREE"
                return_parameter = self.process_payment_method(
                    payment_type, request, pay_txn)

                return Response({'redirect': return_parameter}, status=status.HTTP_200_OK)

        allstates = self.get_state_list()
        return Response({'states': allstates, "total_amount": payment_dict.get('total_payable_amount'),
                         'cart_id': cart_obj.id,
                         }, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        payment_type = request.data.get('payment_type', '').strip()
        if payment_type == 'cash':
            cart_pk = request.data.get('cart_pk')
            if cart_pk:
                cart_obj = Cart.objects.get(pk=cart_pk)
                order = self.createOrder(cart_obj)
                self.closeCartObject(cart_obj)
                if order:
                    txn = 'CP%d%s' % (order.pk, int(time.time()))
                    pay_txn = PaymentTxn.objects.create(
                        txn=txn,
                        order=order,
                        cart=cart_obj,
                        status=0,
                        payment_mode=1,
                        currency=order.currency,
                        txn_amount=order.total_incl_tax,
                    )
                    payment_type = "CASH"
                    return_parameter = self.process_payment_method(
                        payment_type, request, pay_txn)

                    return Response({'redirect': return_parameter, 'order_txn': txn, 'order_pk': order.pk},
                                    status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Cart NOT FOUND'}, status=status.HTTP_400_BAD_REQUEST)

        elif payment_type == 'cheque':
            form = PayByCheckForm(request.data)
            if not form.is_valid():
                return Response({'invalid Data'}, status=status.HTTP_400_BAD_REQUEST)
            cart_pk = request.data.get('cart_pk')
            if cart_pk:
                cart_obj = Cart.objects.get(pk=cart_pk)
                order = self.createOrder(cart_obj)
                self.closeCartObject(cart_obj)
                if order:
                    txn = 'CP%d%s%s' % (
                        order.pk,
                        int(time.time()),
                        request.data.get('cheque_no'))
                    pay_txn = PaymentTxn.objects.create(
                        txn=txn,
                        order=order,
                        cart=cart_obj,
                        status=0,
                        payment_mode=4,
                        currency=order.currency,
                        txn_amount=order.total_incl_tax,
                        instrument_number=request.data.get('cheque_no'),
                        instrument_issuer=request.data.get('drawn_bank'),
                        instrument_issue_date=request.data.get('deposit_date')
                    )
                    payment_type = "CHEQUE"
                    return_parameter = self.process_payment_method(
                        payment_type, request, pay_txn)

                    return Response({'redirect': return_parameter, 'order_txn': txn, 'order_pk': order.pk},
                                    status=status.HTTP_200_OK)
            else:
                return Response({'redirect': '/'})

        return Response({'redirect': '/'})





