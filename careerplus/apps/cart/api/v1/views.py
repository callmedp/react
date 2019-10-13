# python imports
import base64, json, logging
import random
from datetime import datetime, date

# django imports

# local imports
from cart.api.core.serializers import CartSerializer

# inter app imports
from users.mixins import RegistrationLoginApi
from shared.rest_addons.authentication import ShineUserAuthentication
from shared.permissions import IsObjectOwner, IsOwner
from cart.mixins import CartMixin
from cart.models import Cart

# third party imports
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.generics import (RetrieveUpdateAPIView)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated



class EmailStatusView(APIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = ()
    serializer_class = None

    def get(self, request, *args, **kwargs):
        email = kwargs.get('email')
        email_status = RegistrationLoginApi.check_email_exist(email)
        return Response(
            email_status, status=status.HTTP_200_OK)


class CartRetrieveUpdateView(RetrieveUpdateAPIView):
    authentication_classes = (ShineUserAuthentication,)
    permission_classes = (IsAuthenticated, )
    serializer_class = CartSerializer

    def get_queryset(self):
        cart_id = int(self.kwargs.get('pk'))
        return Cart.objects.filter(id=cart_id)
