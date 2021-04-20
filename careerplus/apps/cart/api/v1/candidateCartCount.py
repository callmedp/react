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
from rest_framework import status
from cart.mixins import CartMixin


class CandidateCartCountView(CartMixin, APIView):
    authentication_classes = ()
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        candidate_id = request.data.get('candidate_id')
        utm_params = request.data.get('utm', None)
        sessionid = request.session.session_key

        if not candidate_id:
            return APIResponse(message='Candidate Id is required',  error=True, status=status.HTTP_400_BAD_REQUEST)

        try:
            cart_users = Cart.objects.filter(owner_id = candidate_id, status=2)
            cart_user = None
            if cart_users:
                for cart in cart_users:
                    if cart_user:
                        self.mergeCart(cart, cart_user)
                    else:
                        cart_user = cart

            if cart_user:
                cart_obj = cart_user
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
            data = {'count': cart_count}
            return APIResponse(data=data, message='Candidate Cart Count Success', status=status.HTTP_200_OK)

        except Exception as e:
            logging.getLogger('error_log').error('Error in loading candidate cart api, {}'.format(str(e)))
            return APIResponse(message='Something went wrong, Please try again!', error=True, status=status.HTTP_400_BAD_REQUEST)
