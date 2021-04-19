# Python Core Import
import logging

# Django-Core Import
from django.conf import settings

# Local Imports
from core.common import APIResponse

# Inter-App Import
from users.mixins import RegistrationLoginApi, UserMixin
from shared.rest_addons.authentication import ShineUserAuthentication
from cart.mixins import CartMixin
from cart.models import Cart

# DRF Import
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.generics import (RetrieveUpdateAPIView)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from cart.mixins import CartMixin
from cart.tasks import cart_drop_out_mail, create_lead_on_crm
from shop.models import Product


class CandidateCartCountView(CartMixin, APIView):
    authentication_classes = ()
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        candidate_id = request.data.get('candidate_id')
        # candidate_id = '568a0b20cce9fb485393489b'
        resume_shine_cart = request.data.get('resume_shine', False)
        utm_params = request.data.get('utm', None)
        sessionid = request.session.session_key

        if not candidate_id:
            return APIResponse(message='Candidate Id is required', status=status.HTTP_400_BAD_REQUEST)

        cart_users = Cart.objects.filter(owner_id = candidate_id, status=2)
        cart_sessions = Cart.objects.filter(session_id = sessionid)
        cart_user, cart_session = None, None
        if cart_users:
            for cart in cart_users:
                if cart_user:
                    self.mergeCart(cart, cart_user)
                else:
                    cart_user = cart

        if cart_session:
            for cart in cart_sessions:
                if cart_session:
                    self.mergeCart(cart, cart_session)
                else:
                    cart_session = cart

        if cart_user and cart_session and (cart_user != cart_session):
            self.mergeCart(cart_session, cart)

        if cart_user:
            cart_obj = cart_user
        elif cart_session and candidate_id:
            cart_session.owner_id = candidate_id
            cart_session.status = 2
            cart_session.save()
            cart_obj = cart_session
        elif cart_session:
            cart_obj = cart_session
        elif candidate_id and resume_shine_cart:
            cart_obj = Cart.objects.create(
                owner_id=candidate_id, session_id=sessionid, status=2,
            )
        elif candidate_id:
            cart_obj = Cart.objects.create(
                owner_id=candidate_id, session_id=sessionid, status=2,
            )
        elif sessionid and resume_shine_cart:
            cart_obj = Cart.objects.create(session_id=sessionid, status=0,
                                           )
        elif sessionid:
            cart_obj = Cart.objects.create(session_id=sessionid, status=0,
                                           )

        # update cart_obj in session
        if cart_obj:
            # before updating the cart in session updating the utm params in
            # cart objects
            if utm_params:
                cart_obj.utm_params = utm_params
                cart_obj.save()

        cart_count = self.get_cart_count(None, cart_obj.pk)
        data = {'count': cart_count, 'cart_pk': cart_obj.pk}

        return APIResponse(data=data, message='Candidate Cart Count Loaded', status=status.HTTP_200_OK)
