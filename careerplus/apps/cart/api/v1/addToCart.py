# Core Python Imports
import logging

# Django Imports
from django.conf import settings
from django.urls import reverse

# inter app imports
from cart.models import Cart

# Inter-App Imports
from cart.mixins import CartMixin
from core.common import APIResponse
from cart.tasks import cart_drop_out_mail, create_lead_on_crm
from shop.models import Product
from crmapi.models import UserQuries

# DRF Import
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView


class AddToCartApiView(CartMixin, APIView):
    permission_classes = (AllowAny,)

    def __init__(self):
        self.data = {'status': False}

    def post(self, request, *args, **kwargs):

        """
        Function to add the product in cart using the existing session of
        cart or creating a new cart using CartMixin.

        1. Explore CartMixin for more internal functionality
        2. Also creating lead for the crm added cart
        """

        cart_type = request.POST.get('cart_type', None)
        prod_id   = request.POST.get('prod_id', None)
        cart_pk   = request.session.get('cart_pk', None)
        is_resume_template = request.POST.get('add_resume', False)
        candidate_id = request.session.get('candidate_id', None)

        if prod_id and cart_type is None:
            return APIResponse(message='Product and Cart type is required', status=status.HTTP_400_BAD_REQUEST,
                               error=True)
        try:
            product = Product.objects.filter(id=int(prod_id)).first()
            if not product:
                return APIResponse(message='Product is not found', status=status.HTTP_400_BAD_REQUEST, error=True)

            addons = request.data.get('addons', [])
            req_options = request.data.get('req_options', [])
            cv_id = request.data.get('cv_id')

            cart_status = CartMixin.updateCart(self, product, addons, cv_id, cart_type, req_options, is_resume_template, False)

            try:
                cart_obj = Cart.objects.get(pk=cart_pk)
            except Exception as e:
                logging.getLogger('error_log').error('unable to get cart objects - {}'.format(str(e)))
                cart_obj = None
                logging.getLogger('info_log').info(
                    "Cart Obj:{}, candidate_ID: {}, Owner ID:{}".format(cart_obj, candidate_id, cart_obj.owner_id))

            if cart_obj and candidate_id and int(prod_id) == int(request.session.get('tracking_product_id', -1)):
                request.session.update({'product_availability': prod_id})

            if cart_obj and (candidate_id == cart_obj.owner_id) and not request.ip_restricted:
                first_name = request.session.get('first_name', '')
                last_name = request.session.get('last_name', '')
                name = "{} {}".format(first_name, last_name)

                source_type = "cart_drop_out"

                create_lead_on_crm.apply_async(
                    (cart_obj.pk, source_type, name),
                    countdown=settings.CART_DROP_OUT_LEAD
                )
                lead = self.request.session.get('product_lead_dropout', '')
                if lead:
                    user_queries = UserQuries.objects.get(id=lead)
                    user_queries.inactive = True
                    user_queries.save()

            if cart_status == 1 and cart_type == 'express':
                self.data['redirect_url'] = reverse('cart:payment-login')

            self.data['cart_count'] = CartMixin.get_cart_count(self)
            self.data['status'] = True if cart_status == 1 else False
            self.data['cart_url'] = reverse('cart:payment-summary')

            return APIResponse(data=self.data, status=status.HTTP_200_OK)

        except Exception as e:
            logging.getLogger('error_log').error("Error in adding cart - {}".format(str(e)))
            return APIResponse(message='Something went wrong', status=status.HTTP_400_BAD_REQUEST, error=True)



