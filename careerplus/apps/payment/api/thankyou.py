# python imports

import platform
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import requests
import logging
import json
import time
import codecs
from Crypto.Cipher import AES
from hashlib import md5
from datetime import datetime

# django imports
from django.http import HttpResponse, HttpResponseForbidden
from django.conf import settings

# local imports
from payment.utils import PayuPaymentUtil, ZestMoneyUtil, EpayLaterEncryptDecryptUtil
from cart.models import Cart
from payment.models import PaymentTxn
from order.mixins import OrderMixin
from cart.mixins import CartMixin
from payment.mixin import PaymentMixin
from geolocation.models import PAYMENT_CURRENCY_SYMBOL
from core.utils import get_client_ip, get_client_device_type

# inter app imports
from order.api.v1.serializers import (OrderItemAPISerializer,
                                      OrderSerializer, OrderSerializerForThankYouAPI)
from order.models import Order
from shop.api.core.serializers import(ProductSerializerForThankYouAPI,
                                      DeliveryServiceSerializerForThankYouAPI)

from payment.models import PaymentTxn


# third party imports


class ThankYouAPIView(APIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = None

    def get(self, request, *args, **kwargs):
        order_pk = request.GET.get('order_pk', None)
        if not order_pk:
            return Response({"error_message": "No order primary key provided"},
                            status=status.HTTP_400_BAD_REQUEST)
        order = Order.objects.filter(pk=order_pk).first()
        if not order:
            logging.getLogger('error_log').error(
                'unable to get order with given order id %s', order_pk)
            return Response({"error_message":
                             "No order found with given primary key."},
                            status=tatus.HTTP_400_BAD_REQUEST)

        order_items = []
        parent_ois = order.orderitems.filter(
            parent=None)

        for p_oi in parent_ois:
            data = {}
            data['oi'] = OrderItemAPISerializer(p_oi).data
            if data['oi'] and data['oi']['product']:
                data['oi']['product'] = ProductSerializerForThankYouAPI(
                    p_oi.product).data

            if data['oi'] and data['oi']['delivery_service']:
                data['oi']['delivery_service'] = \
                    DeliveryServiceSerializerForThankYouAPI(
                    p_oi.delivery_service).data

            data['addons'] = order.orderitems.filter(
                parent=p_oi,
                is_addon=True)

            adds = []

            for ind, addons_oi in enumerate(data['addons']):
                adds.append(OrderItemAPISerializer(addons_oi).data)
                if adds[ind] and adds[ind]['product']:
                    adds[ind]['product'] = ProductSerializerForThankYouAPI(
                        addons_oi.product).data
                if adds[ind] and adds[ind]['delivery_service']:
                    adds[ind]['delivery_service'] =\
                        DeliveryServiceSerializerForThankYouAPI(
                        addons_oi.delivery_service).data

            data['addons'] = adds

            data['variations'] = order.orderitems.filter(
                parent=p_oi,
                is_variation=True)

            vars = []

            for ind, var_oi in enumerate(data['variations']):
                vars.append(OrderItemAPISerializer(var_oi).data)
                if vars[ind] and vars[ind]['product']:
                    vars[ind]['product'] = ProductSerializerForThankYouAPI(
                        var_oi.product).data

                if vars[ind] and vars[ind]['delivery_service']:
                    vars[ind]['delivery_service'] =\
                        DeliveryServiceSerializerForThankYouAPI(
                        var_oi.delivery_service).data

            data['variations'] = vars

            order_items.append(data)

        pending_resume_items = True if order.orderitems.filter(
            order__status__in=[0, 1],
            no_process=False, oi_status=2).count()\
            else False

        assesment_items = True if order.orderitems.filter(
            order__status__in=[0],
            product__type_flow=16,
            product__sub_type_flow=1602
        ).count() else False

        booster_item_exist = True if order.orderitems.filter(  # for single booster element in order
            order__status__in=[0, 1],
            product__type_flow__in=[7, 15],
            no_process=False, oi_status=2).count()\
            else False

        last_payment_txn = order.ordertxns.filter().last()
        if last_payment_txn:
            last_payment_txn = last_payment_txn.txn
        else:
            last_payment_txn = None
        order = OrderSerializerForThankYouAPI(order).data
        order['last_payment_txn'] = last_payment_txn

        result = {
            "order": order,
            "order_items": order_items,
            "pending_resume_items": pending_resume_items,
            "assesment_items": assesment_items,
            "booster_item_exist": booster_item_exist,
            "error_message": ""
        }
        return Response(result, status=status.HTTP_200_OK)

    # def get_context_data(self, **kwargs):
    #     context = super(ThankYouView, self).get_context_data(**kwargs)
    #     order_pk = self.request.session.get('order_pk')
    #     if not order_pk:
    #         return
    #     order = Order.objects.filter(pk=order_pk).first()
    #     if not order:
    #         return
    #     order_items = []
    #     parent_ois = order.orderitems.filter(
    #         parent=None).select_related('product', 'partner')
    #     for p_oi in parent_ois:
    #         data = {}
    #         data['oi'] = p_oi
    #         data['addons'] = order.orderitems.filter(
    #             parent=p_oi,
    #             is_addon=True).select_related('product', 'partner')
    #         data['variations'] = order.orderitems.filter(
    #             parent=p_oi,
    #             is_variation=True).select_related('product', 'partner')
    #         order_items.append(data)
    #     context.update({
    #         'orderitems': order_items,
    #         'order': order})

    #     pending_resume_items = order.orderitems.filter(
    #         order__status__in=[0, 1],
    #         no_process=False, oi_status=2)

    #     assesment_items = order.orderitems.filter(
    #         order__status__in=[0],
    #         product__type_flow=16,
    #         product__sub_type_flow=1602
    #     )
    #     booster_item_exist = True if order.orderitems.filter(  # for single booster element in order
    #         order__status__in=[0, 1],
    #         product__type_flow__in=[7, 15],
    #         no_process=False, oi_status=2).count()\
    #         else False

    #     context.update({
    #         "pending_resume_items": pending_resume_items,
    #         "assesment_items": assesment_items,
    #         'booster_item_exist': booster_item_exist,
    #         'candidate_id': self.request and self.request.session.get('candidate_id', '')
    #     })

    #     if not self.request.session.get('resume_id', None):
    #         DashboardInfo().check_user_shine_resume(
    #             candidate_id=self.request.session.get('candidate_id'),
    #             request=self.request)
    #     return context

    # @csrf_exempt
    # def post(self, request, *args, **kwargs):
    #     action_type = request.POST.get('action_type', '').strip()
    #     order_pk = request.session.get('order_pk')
    #     resume_id = request.session.get('resume_id', None)
    #     candidate_id = request.session.get(
    #         'candidate_id', None) or request.session.get('guest_candidate_id', None)
    #     order = Order.objects.filter(pk=order_pk).first()
    #     if not order:
    #         return
    #     order_item_ids = list(
    #         order.orderitems.all().values_list('id', flat=True))
    #     file = request.FILES.get('resume_file', '')

    #     if action_type == 'upload_resume' and order_pk and file:
    #         data = {
    #             "list_ids": order_item_ids,
    #             "candidate_resume": file,
    #             'last_oi_status': 3,
    #         }
    #         DashboardInfo().upload_candidate_resume(candidate_id=candidate_id, data=data)

    #     elif action_type == "shine_reusme" and order_pk and candidate_id and resume_id:
    #         response = ShineCandidateDetail().get_shine_candidate_resume(
    #             candidate_id=candidate_id,
    #             resume_id=request.session.get('resume_id'))
    #         if not response:
    #             request.session.pop('resume_id')
    #             DashboardInfo().check_user_shine_resume(
    #                 candidate_id=candidate_id, request=request)
    #             response = ShineCandidateDetail().get_shine_candidate_resume(
    #                 candidate_id=candidate_id,
    #                 resume_id=request.session.get('resume_id'))
    #         if response.status_code == 200:
    #             file = ContentFile(response.content)
    #             data = {
    #                 "list_ids": order_item_ids,
    #                 "candidate_resume": file,
    #                 'last_oi_status': 13,
    #                 'is_shine': True,
    #                 'extension': request.session.get('resume_extn', '')
    #             }
    #             DashboardInfo().upload_candidate_resume(candidate_id=candidate_id, data=data)

    #     return HttpResponseRedirect(reverse('payment:thank-you'))
