# python imports
import ast, logging

# django imports
from django.utils import timezone
# local imports


# inter app imports
from order.models import Order, OrderItem
from cart.models import Cart, LineItem

# third party imports
from rest_framework import serializers
from datetime import timedelta


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'


class LineItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = LineItem
        fields = '__all__'