from rest_framework import serializers

#app imports
from order.models import OrderItem,Order,LTVMonthlyRecord


class OrderItemListSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField()

    class Meta:
        model = OrderItem
        fields = ('id','product_name',)


class OrderSerializer(serializers.ModelSerializer):
    """
        Serializer for `Order` model
    """
    class Meta:
        model = Order
        exclude = ('co_id','archive_json','site','status','assigned_to','wc_cat','wc_sub_cat'\
            ,'wc_status','wc_follow_up','welcome_call_done','welcome_call_records','midout_sent_on',\
            'paid_by','invoice','crm_sales_id','crm_lead_id','sales_user_info','auto_upload','id')

class LTVReportSerializer(serializers.ModelSerializer):
    ltv_bracket_text = serializers.CharField()
    total_users = serializers.IntegerField()
    crm_users = serializers.IntegerField()
    crm_order_count = serializers.IntegerField()
    learning_users = serializers.IntegerField()
    learning_order_count = serializers.IntegerField()
    total_order_count = serializers.IntegerField()
    total_item_count = serializers.IntegerField()
    
    class Meta:
        model = LTVMonthlyRecord
        exclude = ('candidate_ids','ltv_bracket','crm_order_ids','learning_order_ids',)