# python imports

import logging
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




