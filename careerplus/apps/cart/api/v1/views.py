# app import
from shop.models import Product, ProductClass
from cart.mixins import CartMixin

# django imports
from django.conf import settings
from shared.rest_addons.authentication import ShineUserAuthentication
from rest_framework.permissions import IsAuthenticated

# third parth imports
from rest_framework.generics import (APIView)


class CartOrderView(APIView,CartMixin):
    authentication_classes = (ShineUserAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = None

    def post(self, request, *args, **kwargs):
        data = {"status": -1}
        cart_type = request.POST.get('cart_type')
        prod_id = request.POST.get('prod_id', '')
        cart_pk = request.session.get('cart_pk', '')
        is_resume_template = request.POST.get('add_resume', False)
        candidate_id = request.session.get('candidate_id', '')

        try:
            product = Product.objects.get(id=int(prod_id))
            addons = request.POST.getlist('addons[]')
            req_options = request.POST.getlist('req_options[]')
            cv_id = request.POST.get('cv_id')
            data['status'] = self.updateCart(product, addons, cv_id, cart_type, req_options, is_resume_template)

        except Exception as e:
            print('hello')
