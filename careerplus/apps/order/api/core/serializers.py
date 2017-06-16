from rest_framework import serializers
from order import models


class OrderItemSerializer(serializers.ModelSerializer):
    """
        Serializer for `OrderItem` model
    """
    class Meta:
        model = models.OrderItem
        fields = '__all__'
        read_only_fields = ('id',)
