# import python module
import logging

# import django module
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import datetime

# import apps module
from order.models import WelcomeCallOperation,CustomerFeedback,OrderItemFeedback,OrderItemFeedbackOperation
from order.utils import get_ltv


class Command(BaseCommand):
    def handle(self, *args, **options):
        feedback_call_entry()

def feedback_call_entry():
    start_date = timezone.now() - timedelta(days=7)
    end_date = timezone.now() - timedelta(days=3)
    welcome_operations = WelcomeCallOperation.objects.filter(created__range=[start_date,end_date],order__welcome_call_done=True)
    if not welcome_operations.exists():
        return
    for operation in welcome_operations:
        candidate_id = operation.order.candidate_id
        ltv = get_ltv(candidate_id)
        if ltv<30000:
            continue
        customer_name = (operation.order.first_name + " " if operation.order.first_name else '') + (operation.order.last_name if operation.order.last_name else '')
        mobile = operation.order.mobile
        email = operation.order.email
        payment_date = operation.order.payment_date
        customer_feedback = CustomerFeedback.objects.filter(candidate_id=candidate_id,status=1).first()
        if not customer_feedback:
            customer_feedback = CustomerFeedback.objects.create(candidate_id=candidate_id,full_name=customer_name,mobile=mobile,email=email,last_payment_date=payment_date)
        if customer_feedback.last_payment_date < payment_date:
            customer_feedback.last_payment_date = payment_date
            customer_feedback.save()
        assigned_to = customer_feedback.assigned_to
        for order_item in operation.order.orderitems.all():
            OrderItemFeedback.objects.get_or_create(order_item=order_item,customer_feedback=customer_feedback)
            if assigned_to:
                OrderItemFeedbackOperation.create(order_item=order_item,customer_feedback=customer_feedback,assigned_to=assigned_to)


    


