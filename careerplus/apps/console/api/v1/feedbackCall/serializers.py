from rest_framework import serializers
from order.models import CustomerFeedback,OrderItemFeedback,OrderItemFeedbackOperation,OrderItem
from shared.rest_addons.mixins import ListSerializerContextMixin,ListSerializerDataMixin
from users.models import User


class FeedbackQueueSerializer(serializers.ModelSerializer):
    follow_
    up_date = serializers.DateTimeField()
    
    class Meta:
        model = CustomerFeedback
        fields = ('id','full_name','last_payment_date', 'added_on', 'status_text', 'assigned_to_text', 'follow_up_date')


class CustomerFeedbackSerializer(serializers.ModelSerializer):
    follow_up_date = serializers.DateTimeField()

    class Meta:
        model = CustomerFeedback
        fields = ('id','full_name','mobile', 'email', 'ltv_value','comment','follow_up_date','status')


class OrderItemFeedbackSerializer(ListSerializerContextMixin,ListSerializerDataMixin,serializers.ModelSerializer,):
    list_lookup_fields = ['order_item_id']
    fields_required_mapping = {'order_item_id': ['product_name', 'order_payment_date', 'order_status_text',]}
    field_model_mapping = {'order_item_id':OrderItem}

    class Meta:
        model = OrderItemFeedback
        fields = ('id','category','resolution', 'order_item','comment')


class OrderItemFeedbackOperationSerializer(ListSerializerContextMixin,ListSerializerDataMixin,serializers.ModelSerializer):
    list_lookup_fields = ['order_item_id']
    fields_required_mapping = {'order_item_id': ['product_name',]}
    field_model_mapping = {'order_item_id':OrderItem}

    class Meta:
        model = OrderItemFeedbackOperation
        fields = ('added_on','category_text','resolution_text','comment','assigned_to_text','order_item')


