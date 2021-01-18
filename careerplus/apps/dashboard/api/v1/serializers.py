from rest_framework import serializers

# app imports
from order.models import OrderItem, Order

class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ('id', 'title', 'quantity', 'product', 'item_oi_status')

class OrderSerializer(serializers.ModelSerializer):
    """
        Serializer for `Order` model
    """

    order_status = serializers.ReadOnlyField(source='get_status')
    class Meta:
        model = Order
        exclude = ('co_id', 'archive_json', 'site', 'status', 'assigned_to', 'wc_cat', 'wc_sub_cat', 'wc_status',
            'wc_follow_up', 'welcome_call_done', 'welcome_call_records', 'midout_sent_on', 'paid_by', 'invoice',
            'crm_sales_id', 'crm_lead_id', 'sales_user_info', 'auto_upload', 'id')
