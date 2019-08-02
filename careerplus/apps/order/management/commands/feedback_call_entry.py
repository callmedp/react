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
    start_date = timezone.now() - timedelta(days=4)
    end_date = timezone.now() - timedelta(days=3)
    
    total_feedbacks_created = []
    total_feedbacks_updated = []

    logging.getLogger("info_log").info("Feedback Cron Started for {},{}".format(start_date,end_date))
    welcome_operations = WelcomeCallOperation.objects.filter(\
        wc_status__in=[41,42,63],created__range=[start_date,end_date])
    
    if not welcome_operations.exists():
        return
    
    for operation in welcome_operations:
        logging.getLogger('info_log').info("Processing Order {}".format(operation.order.id))

        candidate_id = operation.order.candidate_id
        ltv = get_ltv(candidate_id) if candidate_id else 0
        customer_name = (operation.order.first_name + " " \
            if operation.order.first_name else '') + (operation.order.last_name if operation.order.last_name else '')
        
        mobile = operation.order.mobile
        email = operation.order.email
        payment_date = operation.order.payment_date
        customer_feedback = CustomerFeedback.objects.filter(\
            candidate_id=candidate_id,status__in=[1,2]).first()
        
        if not customer_feedback:
            customer_feedback = CustomerFeedback.objects.create(\
                candidate_id=candidate_id,full_name=customer_name,\
                mobile=mobile,email=email,last_payment_date=payment_date)
            total_feedbacks_created.append(candidate_id)
            logging.getLogger('info_log').info("Feedback created for {}".format(operation.order.id))

        else:
            total_feedbacks_updated.append(candidate_id)
            logging.getLogger('info_log').info("Feedback updated for {}".format(operation.order.id))
        
        if customer_feedback.last_payment_date < payment_date:
            customer_feedback.last_payment_date = payment_date
        
        customer_feedback.ltv = ltv
        customer_feedback.save()
        assigned_to = customer_feedback.assigned_to
        
        for order_item in operation.order.orderitems.all():
            OrderItemFeedback.objects.get_or_create(order_item=order_item,customer_feedback=customer_feedback)
            
            if assigned_to:
                logging.getLogger("info_log").info(\
                    "Feedback was already assigned {},{}".format(customer_feedback.id,assigned_to))
                OrderItemFeedbackOperation.create(order_item=order_item,\
                    customer_feedback=customer_feedback,assigned_to=assigned_to)

    logging.getLogger('info_log').info("Total Feedbacks Created {}".format(len(set(total_feedbacks_created))))
    logging.getLogger('info_log').info("Total Feedbacks Updated {}".format(len(set(total_feedbacks_updated))))


    


