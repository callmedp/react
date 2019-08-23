from rest_framework import serializers

#app imports
from order.models import OrderItem


class OrderItemListSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField()

    class Meta:
        model = OrderItem
        fields = ('id','product_name',)