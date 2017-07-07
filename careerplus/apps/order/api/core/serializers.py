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
        read_only_fields = ('id', 'number', 'site', 'cart', 'candidate_id', 'txn', 'instrument_number', 'instrument_issuer', 'instrument_issue_date', 'payment_mode', 'payment_date', 'currency', 'total_incl_tax', 'total_excl_tax', 'date_placed', 'email', 'first_name', 'last_name', 'country_code', 'mobile', 'address', 'pincode', 'state', 'country')


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
