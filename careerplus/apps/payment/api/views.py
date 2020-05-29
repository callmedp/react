# python imports

import logging,json
import time

# django imports
from django.http import HttpResponse, HttpResponseForbidden
from django.conf import settings


# local imports
from payment.utils import ZestMoneyUtil
from payment.utils import PayuPaymentUtil
from cart.models import Cart
from payment.models import PaymentTxn
from order.mixins import OrderMixin
from cart.mixins import CartMixin
from payment.mixin import PaymentMixin

# inter app imports


# third party imports

import requests
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


class ZestMoneyFetchEMIPlansApi(APIView):
	authentication_classes = ()
	permission_classes = ()
	serializer_class = None

	def get(self, request, *args, **kwargs):
		amount = self.request.GET.get('amount',0)
		if not amount:
			return HttpResponseForbidden()
		zest_util_obj = ZestMoneyUtil()
		response_data = zest_util_obj.get_emi_plans(amount)
		return Response(response_data.get('recommended_options',[]),
						status=status.HTTP_200_OK)


class ResumeShinePayuRequestAPIView(OrderMixin,APIView):
    authentication_classes = ()
    permission_classes = ()
    serizlizer_classes =None

    def get(self,request,*args,**kwargs):
        return_dict = {}
        cart_id = self.request.GET.get('cart_pk')
        if not cart_id:
            return_dict.update({'error': 'Cart id not found'})
            return Response(return_dict,status=status.HTTP_400_BAD_REQUEST)
        cart_obj = Cart.objects.filter(id=cart_id).first()
        if not cart_obj:
            return_dict.update({'error': 'Cart id not found'})
            return Response(return_dict, status=status.HTTP_400_BAD_REQUEST)

        order = self.createOrder(cart_obj)
        if not order:
            logging.getLogger('error_log').error('order is not created for '
                                                 'cart id- {}'.format(cart_id))
            return Response(return_dict, status=status.HTTP_400_BAD_REQUEST)

        txn = 'CP%d%s' % (order.pk, int(time.time()))
        # creating txn object
        pay_txn = PaymentTxn.objects.create(
            txn=txn,
            order=order,
            cart=cart_obj,
            status=0,
            payment_mode=13,
            currency=order.currency,
            txn_amount=order.total_incl_tax,
        )

        payu_object = PayuPaymentUtil()
        payu_dict = payu_object.generate_payu_dict(pay_txn,'resume_shine')
        hash_val = payu_object.generate_payu_hash(payu_dict)
        payu_dict.update({'hash': hash_val, "action": settings.PAYU_INFO[
            'payment_url']})
        return Response(payu_dict,status=status.HTTP_200_OK)

#
# class ResumeShinePayuRequestAPIView(OrderMixin,APIView):
#     authentication_classes = ()
#     permission_classes = ()
#     serizlizer_classes = None
#
#
# def get(self,request,*args,**kwargs):
#         return_dict = {}
#         cart_id = self.request.GET.get('cart_id')
#         if not cart_id:
#             return_dict.update({'error': 'Cart id not found'})
#             return Response(return_dict,status=status.HTTP_400_BAD_REQUEST)
#         cart_obj = Cart.objects.filter(id=cart_id).first()
#         if not cart_obj:
#             return_dict.update({'error': 'Cart id not found'})
#             return Response(return_dict, status=status.HTTP_400_BAD_REQUEST)
#
#         order = self.createOrder(cart_obj)
#         if not order:
#             logging.getLogger('error_log').error('order is not created for '
#                                                  'cart id- {}'.format(cart_id))
#             return Response(return_dict, status=status.HTTP_400_BAD_REQUEST)
#
#         txn = 'CP%d%s' % (order.pk, int(time.time()))
#         # creating txn object
#         pay_txn = PaymentTxn.objects.create(
#             txn=txn,
#             order=order,
#             cart=cart_obj,
#             status=0,
#             payment_mode=13,
#             currency=order.currency,
#             txn_amount=order.total_incl_tax,
#         )
#
#         payu_object = PayuPaymentUtil()
#         payu_dict = payu_object.generate_payu_dict(pay_txn,'resume_shine')
#         hash_val = payu_object.generate_payu_hash(payu_dict)
#         payu_dict.update({'hash': hash_val, "action": settings.PAYU_INFO[
#             'payment_url']})
#         return Response(payu_dict,status=status.HTTP_200_OK)


class ResumeShinePayUResponseView(CartMixin,PaymentMixin,APIView):
    authentication_classes = ()
    permission_classes = ()
    serizlizer_classes = None

    def post(self, request, *args, **kwargs):
        payu_data = request.POST.copy()
        transaction_status = payu_data.get('status', '').upper()
        txn_id = payu_data.get('txnid')
        if not txn_id:
            logging.getLogger('error_log').error(
                "PayU No txn id - {}".format(payu_data))
            return Response({'error':'bad request'},status=status.HTTP_400_BAD_REQUEST)

        txn_obj = PaymentTxn.objects.filter(txn=txn_id,status=0).first()
        if not txn_obj:
            logging.getLogger('error_log').error(
                "PayU No txn obj for txnid - {}".format(txn_id))
            return Response({'error':'bad request'},status=status.HTTP_400_BAD_REQUEST)
        extra_info_dict ={
                    'bank_ref_no': payu_data.get('bank_ref_num', ''),
                    'bank_gateway_txn_id': payu_data.get('mihpayid', ''),
                    'bank_code': payu_data.get('bankcode', ''),
                    'txn_mode': payu_data.get('mode', ''),
                    'error': payu_data.get('error_Message',''),
        }
        extra_info_json = json.dumps(extra_info_dict)
        txn_obj.txn_info = extra_info_json
        txn_obj.save()

        if transaction_status == "SUCCESS":
            payment_type = "PAYU"
            return_parameter = self.process_payment_method(
                payment_type, request, txn_obj)
            self.closeCartObject(txn_obj.cart)
            return Response({'redirect' : return_parameter}, status=status.HTTP_200_OK)

        elif transaction_status == "FAILURE" or transaction_status == "PENDING":
            txn_obj.status = 0
            txn_obj.save()
        return Response({'redirect' : '/payment/oops?error=failure&txn_id=' + txn_id}, status=status.HTTP_200_OK)





