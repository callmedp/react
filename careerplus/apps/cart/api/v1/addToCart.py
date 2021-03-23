# Core Python Imports
import logging
from datetime import datetime, date

# Django Imports
from django.conf import settings

# inter app imports
from cart.models import Cart

# Inter-App Imports
from cart.mixins import CartMixin
from cart.tasks import cart_drop_out_mail, create_lead_on_crm
from shop.models import Product
from payment.tasks import make_logging_request

# DRF Import
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class AddToCartApiView(CartMixin, APIView):
    permission_classes = (AllowAny,)

    def __init__(self):
        self.category = None

    def post(self, request, *args, **kwargs):

        pass
