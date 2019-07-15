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
    if welcome_operations.count() > 0 :
        for operation in welcome_operations:
            candidate_id = operatioordern..candidate_id
            # customer_name = operation.order.first_name + " " + operation.order.last_name
            customer_feedback_exist_entry = CustomerFeedback.objects.filter(added_on__contains=timezone.now().date(),candidate_id=candidate_id)
            customer_feedback = None
            if customer_feedback_exist_entry.count() == 0:
                customer_feedback = CustomerFeedback.objects.create(candidate_id=candidate_id)
            else:
                customer_feedback = customer_feedback_exist_entry.first()
            for order_item in operation.order.orderitems.all():
                OrderItemFeedback.objects.create(order_item=order_item,customer_feedback=customer_feedback)


    


