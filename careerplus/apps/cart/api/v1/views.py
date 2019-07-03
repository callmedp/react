# app import
from shop.models import Product, ProductClass
from cart.mixins import CartMixin
from cart.models import Cart
# django imports
from django.conf import settings
from shared.rest_addons.authentication import ShineUserAuthentication
from rest_framework.permissions import IsAuthenticated
from cart.tasks import cart_drop_out_mail, create_lead_on_crm
import logging

# third parth imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class CartOrderView(APIView, CartMixin):
    authentication_classes = (ShineUserAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = None

    def post(self, request, *args, **kwargs):
        import ipdb;
        ipdb.set_trace();
        data = {"status": -1}
        cart_type = request.data.get('cart_type')
        prod_id = request.data.get('prod_id', '')
        cart_pk = request.session.get('cart_pk', '')
        is_resume_template = request.data.get('add_resume', False)
        candidate_id = request.data.get('candidate_id', '')
        # get product
        product = Product.objects.filter(id=int(prod_id)).first()
        # get cart obj
        cart_obj = Cart.objects.filter(pk=cart_pk).first()

        if not cart_obj:
            logging.getLogger('error_log').error('unable to get cart object.')
            cart_obj = None

        if not product:
            data['error_message'] = "No product is available with id {}.".format(prod_id)
            logging.getLogger('error_log').error("No product is available with id {}.".format(prod_id))
        else:
            addons = request.data.get('addons')
            req_options = request.data.get('req_options')
            cv_id = request.data.get('cv_id')
            data['status'] = self.updateCart(product, addons, cv_id, cart_type, req_options, is_resume_template)

            logging.getLogger('info_log').info(
                "Cart Obj:{}, candidate_ID: {}, Owner ID:{}".format(cart_obj, candidate_id, cart_obj.owner_id))

            if cart_obj and (candidate_id == cart_obj.owner_id) and not request.ip_restricted:
                first_name = request.session.get('first_name', '')
                last_name = request.session.get('last_name', '')
                email = request.session.get('email', '')
                name = "{}{}".format(first_name, last_name)

                source_type = "cart_drop_out"

                create_lead_on_crm.apply_async(
                    (cart_obj.pk, source_type, name),
                    countdown=settings.CART_DROP_OUT_LEAD)

        return Response({"detail": "Cart Successfully Created"}, status=status.HTTP_200_OK)
