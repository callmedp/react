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
from django.core.files.base import ContentFile


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
from dashboard.dashboard_mixin import DashboardInfo
from core.api_mixin import ShineCandidateDetail


from payment.models import PaymentTxn


# third party imports


class ThankYouAPIView(APIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = None

    def get(self, request, *args, **kwargs):
        order_pk = request.GET.get('order_pk', None)
        pay_txn = request.GET.get('pay_txn',None)
        if not order_pk and not pay_txn:
            return Response({"error_message": "No order primary key provided"},
                            status=status.HTTP_400_BAD_REQUEST)
        order = None
        if pay_txn:
            pay_obj = PaymentTxn.objects.filter(txn=pay_txn).first()
            if pay_obj:
                order = pay_obj.order
        else:
            order = Order.objects.filter(pk=order_pk).first()
        if not order:
            logging.getLogger('error_log').error(
                'unable to get order with given order id %s', order_pk)
            return Response({"error_message":
                             "No order found with given primary key."},
                            status=status.HTTP_400_BAD_REQUEST)

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

        candidate_id = order['candidate_id']
        resume_info = DashboardInfo().fetch_user_shine_resume(
            candidate_id=candidate_id, request=request)
        resume_id = None
        if resume_info:
            resume_id = resume_info['id']

        result = {
            "order": order,
            "order_items": order_items,
            "pending_resume_items": pending_resume_items,
            "assesment_items": assesment_items,
            "booster_item_exist": booster_item_exist,
            "resume_id": resume_id,
            "candidate_id": candidate_id,
            "error_message": ""
        }
        return Response(result, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):

        response = None
        resume_info = None
        result = {"error_message": "", "success": False}
        action_type = request.data.get('action_type', 'shine_reusme').strip()
        order_pk = request.data.get('order_pk')
        resume_id = request.data.get('resume_id', None)
        candidate_id = request.data.get(
            'candidate_id', None)
        if not candidate_id:
            result["error_message"] = "No candidate id is provided"
            return Response(result, status=status.HTTP_400_BAD_REQUEST)

        if not order_pk:
            result["error_message"] = "No order primary key is provided"
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
        order = Order.objects.filter(pk=order_pk).first()
        if not order:
            result["error_message"]: "No order avaialable with given primary key"
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
        order_item_ids = list(
            order.orderitems.all().values_list('id', flat=True))
        file = request.data.get('resume_file', '')

        if action_type == 'upload_resume' and order_pk and file:
            data = {
                "list_ids": order_item_ids,
                "candidate_resume": file,
                'last_oi_status': 3,
            }
            DashboardInfo().upload_candidate_resume(candidate_id=candidate_id, data=data)

        elif action_type == "shine_reusme" and order_pk and candidate_id:
            if resume_id:
                response = ShineCandidateDetail().get_shine_candidate_resume(
                    candidate_id=candidate_id,
                    resume_id=resume_id)
            if not response:
                resume_info = DashboardInfo().fetch_user_shine_resume(
                    candidate_id=candidate_id, request=request)
                if resume_info:
                    response = ShineCandidateDetail().get_shine_candidate_resume(
                        candidate_id=candidate_id,
                        resume_id=resume_info['id'])
            if response and response.status_code == 200:
                file = ContentFile(response.content)
                data = {
                    "list_ids": order_item_ids,
                    "candidate_resume": file,
                    'last_oi_status': 13,
                    'is_shine': True,
                    'extension': resume_info['extension']
                }
                DashboardInfo().upload_candidate_resume(candidate_id=candidate_id, data=data)
        if not response or response.status_code != 200:
            return Response({"error_message": "Could not able to upload candidate resume.", "success": False}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error_message": "", "success": True}, status=status.HTTP_200_OK)
