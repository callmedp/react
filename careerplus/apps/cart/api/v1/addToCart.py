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

    def maintain_tracking_info(self, product=None):
        if not product:
            return -1
        if product.sub_type_flow == 501:
            return 1
        if product.sub_type_flow == 503:
            return 2
        if product.sub_type_flow == 504:
            return 3
        if product.type_flow == 18:
            return 4
        if product.type_flow == 19:
            return 5
        if product.type_flow == 1:
            return 6
        if product.sub_type_flow == 502:
            return 7
        if product.type_flow == 16:
            return 8
        if product.type_flow == 2:
            return 9
        if product.type_flow == 17:
            return 11

    def post(self, request, *args, **kwargs):
        from payment.tasks import make_logging_request
        data = {"status": -1}
        cart_type = request.data.get('cart_type')
        prod_id = request.data.get('prod_id', None)
        cart_pk = request.data.get('cart_pk', None)  # TODO handle this
        is_resume_template = request.data.get('add_resume', False)
        resume_shine_cart = request.data.get('resume_shine', False)
        tracking_id = request.data.get('tracking_id', '')
        emailer = int(request.data.get('emailer', 0))
        domain = 3
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
                if tracking_id:
                    u_id = request.data.get('u_id', '')
                    trigger_point = request.data.get('trigger_point', '')
                    position = request.data.get('position', '')
                    utm_campaign = request.data.get('utm_campaign', '')
                    tracking_product_id = prod_id
                    product_tracking_mapping_id = self.maintain_tracking_info(product)

                    if tracking_product_id and product_tracking_mapping_id and emailer:
                        make_logging_request.delay(
                                tracking_product_id, product_tracking_mapping_id, tracking_id, 'clicked', position, trigger_point, u_id, utm_campaign, domain)

                    cart_drop_out_mail.apply_async(
                        (cart_pk, email, "SHINE_CART_DROP", name, 
                            tracking_id, u_id, tracking_product_id, 
                            product_tracking_mapping_id, trigger_point, 
                            position, utm_campaign, domain),
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
