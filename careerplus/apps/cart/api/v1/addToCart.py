# python imports
import base64
import json
import logging
from datetime import datetime, date

# django imports
from django.conf import settings

# local imports

# inter app imports
from cart.mixins import CartMixin
from cart.models import Cart

# third party imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from cart.mixins import CartMixin
from cart.tasks import cart_drop_out_mail, create_lead_on_crm
from shop.models import Product


class AddToCartApiView(CartMixin, APIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = None

    def post(self, request, *args, **kwargs):
        data = {"status": -1}
        cart_type = request.data.get('cart_type')
        prod_id = request.data.get('prod_id', None)
        cart_pk = request.data.get('cart_pk', None)  # TODO handle this
        is_resume_template = request.data.get('add_resume', False)
        resume_shine_cart = request.data.get('resume_shine', False)
        candidate_id = request.data.get(
            'candidate_id', None)  # TODO  handle this
        try:
            # not filter on active because product is coming from solr
            product = Product.objects.filter(id=int(prod_id)).first()
            if not product:
                # TODO  handle response status here.
                return Response({'errror_message': 'No Product with given id ' + prod_id}, status=status.HTTP_400_BAD_REQUEST)
            addons = request.data.get('addons', [])
            req_options = request.data.get('req_options', [])
            cv_id = request.data.get('cv_id')
            result = self.updateCart(product, addons, cv_id, cart_type,
                                     req_options, is_resume_template,
                                     resume_shine_cart)
            data['status'] = result[0]
            cart_pk = result[1] if result[1] else cart_pk
            try:
                cart_obj = Cart.objects.get(pk=cart_pk)
            except Exception as e:
                logging.getLogger('error_log').error(
                    'unable to get cart object %s' % str(e))
                cart_obj = None
            logging.getLogger('info_log').info(
                "Cart Obj:{}, candidate_ID: {}, Owner ID:{}".format(cart_obj, candidate_id, cart_obj.owner_id))
            if cart_obj and (candidate_id == cart_obj.owner_id) and not request.ip_restricted:
                first_name = request.session.get('first_name', '')
                last_name = request.session.get('last_name', '')
                email = request.session.get('email', '')
                name = "{}{}".format(first_name, last_name)
                cart_drop_out_mail.apply_async(
                    (cart_pk, email, "SHINE_CART_DROP", name),
                    countdown=settings.CART_DROP_OUT_EMAIL)
                source_type = "cart_drop_out"

                create_lead_on_crm.apply_async(
                    (cart_obj.pk, source_type, name),
                    countdown=settings.CART_DROP_OUT_LEAD)
        except Exception as e:
            data['error_message'] = str(e)
            logging.getLogger('error_log').error("%s " % str(e))

        # if data['status'] == 1 and cart_type == "express":
        #     data['redirect_url'] = reverse('cart:payment-login')

        data['cart_count'] = str(self.get_cart_count(None, cart_pk))
        data['cart_pk'] = cart_pk

        return Response(data, status=status.HTTP_201_CREATED)
