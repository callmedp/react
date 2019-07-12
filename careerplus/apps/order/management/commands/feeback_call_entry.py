# import python module
import logging

# import django module
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import datetime

# import apps module
from order.models import WelcomeCallOperation,CustomerFeedback,OrderItemFeedback


class Command(BaseCommand):
    def handle(self, *args, **options):
        feedback_call_entry()

def feedback_call_entry():
    start_date = timezone.now() - timedelta(days=7)
    end_date = timezone.now() - timedelta(days=3)
    welcome_operations = WelcomeCallOperation.objects.filter(created__range=[start_date,end_date],order__welcome_call_done=True)
    if welcome.operations.count() > 0 :
        for operation in welcome_operations:
            candidate_id = operation.order.candidate_id
            customer_feedback_exist_entry = CustomerFeedback.objects.filter(added_on__conatins=timezone.now().date(),candidate_id=candidate_id)
            if customer_feedback_exist_entry.count() > 0:
                for order_item in operation.order.orderitems.all():
                    OrderItemFeedback 
            customer_feedback = operation.order.first_name + " " + operation.order.last_name


    import ipdb ; ipdb.set_trace()


