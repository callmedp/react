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
            cart_user = Cart.objects.get(owner_id=candidate_id, status=2)
        except Cart.DoesNotExist:
            logging.getLogger('error_log').error('Cart not exist for the candidate, {}'.format(str(candidate_id)))
            cart_user = Cart.objects.create(owner_id=candidate_id, status=2, session_id=sessionid)
        except Cart.MultipleObjectsReturned:
            logging.getLogger('error_log').error('Multiple cart exist for candidate, {}'.format(str(candidate_id)))
            cart_user = Cart.objects.filter(owner_id=candidate_id, status=2).first()

        # update cart_obj in session
        if cart_user:
            # before updating the cart in session updating the utm params in
            # cart objects
            if utm_params:
                cart_user.utm_params = utm_params
                cart_user.save()

            cart_count = self.get_cart_count(None, cart_user.pk)
            data = {'count': cart_count}
            return APIResponse(data=data, message='Candidate Cart Count Success', status=status.HTTP_200_OK)

        return APIResponse(message='Something went wrong, Please try again!', error=True, status=status.HTTP_400_BAD_REQUEST)
