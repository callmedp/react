from rest_framework import serializers
from order import models
from shop.api.core.serializers import ProductSerializer


class OrderSerializer(serializers.ModelSerializer):
    """
        Serializer for `Order` model
    """
    class Meta:
        model = models.Order
        fields = '__all__'
        read_only_fields = ('id',)


class OrderItemSerializer(serializers.ModelSerializer):
    """
        Serializer for `OrderItem` model
    """
    order = OrderSerializer()
    product = ProductSerializer()
    class Meta:
        model = models.OrderItem
        fields = '__all__'
        read_only_fields = ('id',)
