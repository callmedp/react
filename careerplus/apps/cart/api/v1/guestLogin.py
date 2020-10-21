# python imports
import logging
from datetime import datetime, date

# django imports

# local imports
from cart.api.core.serializers import CartSerializer

# inter app imports
from users.mixins import UserMixin
from users.tasks import user_register
from cart.mixins import CartMixin
from cart.models import Cart
from coupon.api.core.serializers import CouponSerializer
from wallet.api.core.serializers import (
    WalletSerializer, WalletTransactionSerializer)

# third party imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from cart.mixins import CartMixin


class GuestLoginView(CartMixin, APIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = None

    def post(self, request, *args, **kwargs):
        cart_pk = request.data.get('cart_pk', None)
        mobile_number = request.data.get('mobile', '')
        guest_name = request.data.get('name', '')
        country_code = request.data.get('country_code', '')
        email = request.data.get('email', '')
        missing_list = []
        if not guest_name:
            missing_list.append('guest_name')
        if not cart_pk:
            missing_list.append('cart_pk')
        if not mobile_number:
            missing_list.append('mobile_number')
        if not country_code:
            missing_list.append('country_code')
        if not email:
            missing_list.append('email')
        if len(missing_list):
            return Response({"error_message": ', '.join(missing_list)
                             + ' are missing.'if len(missing_list) > 1
                             else ', '.join(missing_list) + ' is missing.'},
                            status=status.HTTP_400_BAD_REQUEST)
        first_name = guest_name.strip().split(' ')[0]
        last_name = ' '.join((guest_name + ' ').split(' ')[1:]).strip()

        # update cart info

        cart_obj = Cart.objects.filter(pk=cart_pk).first()
        if not cart_obj:
            return Response({"error_message": 'There is no cart available \
                              with cart id' + cart_pk},
                            status=status.HTTP_400_BAD_REQUEST)

        if cart_obj.coupon_id and cart_obj.owner_email != email:
            return Response({'error_message':'Coupon is already applied with another email.Either remove the coupon '
                                             'or enter the same email address'}, status=status.HTTP_400_BAD_REQUEST)
        cart_obj.email = email
        cart_obj.owner_email = email
        cart_obj.mobile = mobile_number
        cart_obj.first_name = first_name
        cart_obj.last_name = last_name
        cart_obj.country_code = country_code

        # registering user into shine (for getting candidate/owner id )
        data = {}
        data.update({
            "email": cart_obj.email,
            "country_code": cart_obj.country_code,
            "cell_phone": cart_obj.mobile,
            "name": guest_name,
        })
        candidate_id = None
        error = ''
        try:
            candidate_id, error = user_register(data=data)
        except Exception as e:
            return Response({"error_message": "Unable to \
                             create guest User {}".format(e)},
                            status=status.HTTP_400_BAD_REQUEST)

        # setting guest candidate id for thank you upload fix

        # if error:
        #     return Response({"error_message": error},
        #                     status=status.HTTP_400_BAD_REQUEST)

        cart_obj.owner_id = candidate_id

        cart_obj.save()

        return Response({"guest_candidate_id": candidate_id, "cart_pk": cart_pk},
                        status=status.HTTP_200_OK)
