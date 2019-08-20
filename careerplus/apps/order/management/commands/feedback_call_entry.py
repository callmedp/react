# import python module
import logging
from datetime import timedelta
import datetime

# import django module
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings

# import apps module
from order.utils import get_ltv
from emailers.tasks import send_email_task
from order.models import WelcomeCallOperation,CustomerFeedback,OrderItemFeedback,OrderItemFeedbackOperation


class Command(BaseCommand):
    def handle(self, *args, **options):
        feedback_call_entry()

def feedback_call_entry():
    start_time = timezone.now()
    start_date = timezone.now() - timedelta(days=7)
    end_date = start_date + timedelta(days=1)
    
    total_feedbacks_created = []
    total_feedbacks_updated = []
    total_feedbacks_failed = 0

    logging.getLogger("info_log").info("Feedback Cron Started for {},{}".format(start_date,end_date))
    welcome_operations = WelcomeCallOperation.objects.filter(\
        wc_status__in=[41,42,63],created__range=[start_date,end_date],order__status=1)
    
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
        
        if payment_date and (not customer_feedback.last_payment_date or \
            customer_feedback.last_payment_date < payment_date):
            customer_feedback.last_payment_date = payment_date
        
        customer_feedback.ltv = ltv
        try:
            customer_feedback.save()
        except Exception as e:
            total_feedbacks_failed += 1
            logging.getLogger('error_log').error(\
                "Error in creating feedback {},{}".format(operation.order.id,e))
        assigned_to = customer_feedback.assigned_to
        
        for order_item in operation.order.orderitems.all():
            OrderItemFeedback.objects.get_or_create(order_item=order_item,customer_feedback=customer_feedback)
            
            if assigned_to:
                logging.getLogger("info_log").info(\
                    "Feedback was already assigned {},{}".format(customer_feedback.id,assigned_to))
                OrderItemFeedbackOperation.objects.create(order_item=order_item,\
                    customer_feedback=customer_feedback,assigned_to=assigned_to)
    
    end_time = timezone.now()
    email_dict = {
                "subject": 'Feedback Call Cron completed',
                "new_feedback_entries": len(total_feedbacks_created),
                "updated_feedback_entries": len(total_feedbacks_updated),
                "failed_feedback_entries": total_feedbacks_failed,
                "start_time": start_time,
                "end_time":end_time,
    }
    to_emails = ['hitesh.rexwal@hindustantimes.com',"animesh.sharma@hindustantimes.com",\
        "vishal.gupta@hindustantimes.com","vinod@shine.com","purnima.ganguly@shine.com"]

    mail_type = 'FEEDBACK_CALL_CRON'
    send_email_task(to_emails,mail_type,email_dict)
    body = render_to_string('emailers/console/feedback_call_cron.html', email_dict)
    try:
        emsg = EmailMessage(email_dict.get('subject'), body=body, to=to_emails, from_email=settings.CONSULTANTS_EMAIL)
        emsg.content_subtype = 'html'
        emsg.send()
    except Exception as e:
        logging.getLogger('error_log').error("%s - %s" % ('Mail Failed', str(e)))
    
    logging.getLogger('info_log').info("Total Feedbacks Created {}".format(len(set(total_feedbacks_created))))
    logging.getLogger('info_log').info("Total Feedbacks Updated {}".format(len(set(total_feedbacks_updated))))


    


