#rest imports
from rest_framework import serializers

#app imports
from order.models import CustomerFeedback,OrderItemFeedback,OrderItemFeedbackOperation,OrderItem
from shared.rest_addons.mixins import ListSerializerContextMixin,ListSerializerDataMixin
from users.models import User


class FeedbackQueueSerializer(serializers.ModelSerializer):
    status_text = serializers.CharField()
    assigned_to_text = serializers.CharField()
    class Meta:
        model = CustomerFeedback
        include= ('status_text')
        exclude = ('candidate_id','mobile','email','comment')

class CustomerFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerFeedback
        exclude = ('candidate_id','added_on','assigned_to','last_payment_date')



class OrderItemFeedbackSerializer(ListSerializerContextMixin,ListSerializerDataMixin,serializers.ModelSerializer,):
    list_lookup_fields = ['order_item_id']
    fields_required_mapping = {'order_item_id': ['product_name', 'order_payment_date', 'get_oi_status','order_id']}
    field_model_mapping = {'order_item_id':OrderItem}

    class Meta:
        model = OrderItemFeedback
        exclude = ('customer_feedback',)


class OrderItemFeedbackOperationSerializer(ListSerializerContextMixin,ListSerializerDataMixin,serializers.ModelSerializer):
    category_text = serializers.CharField()
    resolution_text = serializers.CharField()
    assigned_to_text = serializers.CharField()
    oi_type_text = serializers.CharField()
    list_lookup_fields = ['order_item_id']
    fields_required_mapping = {'order_item_id': ['product_name',]}
    field_model_mapping = {'order_item_id':OrderItem}

    class Meta:
        model = OrderItemFeedbackOperation
        exclude = ('customer_feedback','assigned_to','category','resolution','oi_type','id')


