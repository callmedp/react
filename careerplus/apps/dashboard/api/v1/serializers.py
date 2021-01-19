from rest_framework import serializers

# app imports
from order.models import OrderItem, Order
from datetime import datetime

class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ('id', 'title', 'quantity', 'product', 'oi_status')

    def to_representation(self, instance):
        data = super(OrderItemSerializer, self).to_representation(instance)
        data.update({
            'productUrl': instance.product.get_absolute_url() if instance.product_id else '',
            'product_type_flow': instance.product.type_flow if instance.product_id else '', 
            'parent': instance.parent_id,
            'parent_heading': instance.parent.product.heading if instance.parent_id and instance.parent.product_id else '',
            'get_user_oi_status': instance.get_user_oi_status,
            'heading': instance.product.heading if instance.product_id else '',
            'get_name': instance.product.get_name if instance.product_id else '',
            'get_exp_db': instance.product.get_exp_db() if instance.product_id else '',
            'get_studymode_db': instance.product.get_studymode_db() if instance.product_id else '',
            'get_coursetype_db': instance.product.get_coursetype_db() if instance.product_id else '',
            'get_duration_in_day': instance.product.get_duration_in_ddmmyy() if instance.product_id and
                                                                                              instance.product.get_duration_in_day() else '',
        })
        return data


class OrderSerializer(serializers.ModelSerializer):
    """
        Serializer for `Order` model
    """

    order_status = serializers.ReadOnlyField(source='get_status')
    class Meta:
        model = Order
        exclude = ('co_id', 'archive_json', 'site', 'assigned_to', 'wc_cat', 'wc_sub_cat', 'wc_status',
            'wc_follow_up', 'welcome_call_done', 'welcome_call_records', 'midout_sent_on', 'paid_by', 'invoice',
            'crm_sales_id', 'crm_lead_id', 'sales_user_info', 'auto_upload', 'created', 'modified')

    def to_representation(self, instance):
        data = super(OrderSerializer, self).to_representation(instance)
        data['date_placed'] = instance.date_placed.date().strftime('%d %b %Y') if instance.date_placed else None
        data['currency'] = instance.get_currency()
        return data
