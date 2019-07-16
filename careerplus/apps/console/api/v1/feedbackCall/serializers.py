from rest_framework import serializers
from order.models import CustomerFeedback,OrderItemFeedback,OrderItem
from shared.rest_addons.mixins import ListSerializerContextMixin,ListSerializerDataMixin


class FeedbackQueueSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomerFeedback
        fields = ('id','full_name','last_payment_date', 'added_on', 'status_name', 'assigned_to', 'follow_up_date')


class CustomerFeedbackSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomerFeedback
        fields = ('full_name','mobile', 'email', 'ltv')


# class OrderItemSerializer(serializers.ModelSerializer,SerializerFieldsMixin):
#     product_name = serializers.SerializerMethodField()
#     payment_date = serializers.SerializerMethodField()

#     def get_product_name(self,instance):
#         return instance.product.name

#     def get_payment_date(self,instance):
#         return instance.order.payment_date
    
#     class Meta:
#         model = OrderItem
#         exclude = ()
#         # fields = ('id','product_name','payment_date','order_status_text')



class OrderItemFeedbackSerializer(ListSerializerContextMixin,ListSerializerDataMixin,serializers.ModelSerializer,):
    list_lookup_fields = ['order_item_id']
    fields_required_mapping = {'order_item_id': ['product_name', 'order_payment_date', 'order_status_text',]}
    field_model_mapping = {'order_item_id':OrderItem}
    class Meta:
        model = OrderItemFeedback
        fields = ('category','resolution', 'order_item')


