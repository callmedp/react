# python imports
import base64, json, logging
import random
from datetime import datetime, date

# django imports

# local imports

# inter app imports
from users.mixins import RegistrationLoginApi
from shared.rest_addons.authentication import ShineUserAuthentication
from shared.permissions import IsObjectOwner
from cart.mixins import CartMixin
from cart.models import Cart

# third party imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class EmailStatusView(APIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = None

    def get(self, request, *args, **kwargs):
        email = kwargs.get('email')
        email_status = RegistrationLoginApi.check_email_exist(email)
        return Response(
            email_status, status=status.HTTP_200_OK)


class UpdateCartView(CartMixin, APIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = None

    def post(self, request, *args, **kwargs):
        candidate_id = kwargs.get('candidate_id')
        email = kwargs.get('email')
        first_name = kwargs.get('first_name')

        cart_pk = request.session.get('cart_pk')
        if cart_pk:
            cart_obj = Cart.objects.get(pk=cart_pk)
            cart_obj.email = email
            cart_obj.owner_id = candidate_id
            cart_obj.owner_mail = email
            cart_obj.first_name = first_name
            cart_obj.save()
        import ipdb;
        ipdb.set_trace();
        return Response({}, status=status.HTTP_200_OK)
