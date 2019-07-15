from rest_framework import serializers
from order.models import CustomerFeedback


class FeedbackQueueSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomerFeedback
        fields = ('id','full_name','last_payment_date', 'added_on', 'status_name', 'assigned_to', 'follow_up_date')

