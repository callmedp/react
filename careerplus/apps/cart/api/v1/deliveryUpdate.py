# python imports
import logging
from datetime import datetime, date
from decimal import Decimal
from django.utils import timezone

# django imports

# local imports

# inter app imports
from cart.mixins import CartMixin
from cart.models import Cart

# third party imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class DeliveryUpdateView(CartMixin, APIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = None

    def post(self, request, *args, **kwargs):
        cart_pk = request.data.get('cart_pk', None)
        lineid = request.data.get('lineid', None)
        delivery_type = request.data.get('delivery_type', None)
        missing_list = []
        if lineid is None:
            missing_list.append('lineid')
        if delivery_type is None:
            missing_list.append('delivery_type')
        if cart_pk is None:
            missing_list.append('cart_pk')

        if len(missing_list):
            return Response({"error_message": ', '.join(missing_list)
                             + ' are missing.'if len(missing_list) > 1
                             else ', '.join(missing_list) + ' is missing.'},
                            status=status.HTTP_400_BAD_REQUEST)

        data = {"total_cart_amount": -1, "delivery_charge": -1}
        cart_obj = Cart.objects.filter(pk=cart_pk).first()
        if not cart_obj:
            return Response({"error_message": 'There is no cart available \
                              with cart id' + str(cart_pk)},
                            status=status.HTTP_400_BAD_REQUEST)

        line_obj = cart_obj.lineitems.filter(pk=lineid).first()
        if not line_obj:
            return Response({"error_message": 'There is no Line Item available \
                              with line id' + str(lineid)},
                            status=status.HTTP_400_BAD_REQUEST)

        delivery_services = line_obj.product.get_delivery_types()
        if not delivery_services:
            return Response({"error_message": "No Delivery Services available for lineid " + str(lineid)},
                            status=status.HTTP_400_BAD_REQUEST)
        delivery_obj = delivery_services.filter(pk=delivery_type).first()
        if not delivery_obj:
            return Response({"error_message": "No Delivery Object available for lineid " + str(lineid)},
                            status=status.HTTP_400_BAD_REQUEST)
        line_obj.delivery_service = delivery_obj
        line_obj.save()
        cart_dict = self.get_solr_cart_items(cart_obj=cart_obj)
        total_cart_amount = cart_dict.get('total_amount')
        delivery_charge = delivery_obj.get_price()
        payment_dict = self.getPayableAmount(
            cart_obj, cart_dict.get('total_amount'))
        data.update({
            "total_payable_amount": float(payment_dict['total_payable_amount']),
            "total_cart_amount": float(total_cart_amount),
            "delivery_charge": float(delivery_charge),
            "delivery_service_title": delivery_obj.title,
            "delivery_service_meta_desc": delivery_obj.meta_desc,
            'sgst_amount': float(payment_dict['sgst_amount']),
            "cgst_amount": float(payment_dict['cgst_amount'])
        })

        return Response(data, status=status.HTTP_201_CREATED)
