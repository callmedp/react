
import datetime
import logging

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings

from order.models import OrderItem
from emailers.email import SendMail
from emailers.sms import SendSMS
from shop.choices import S_ATTR_DICT

SERVICES = {
    501 : {'oi_status': 28, 'product__sub_type_flow': 501, 'product__type_flow': 5},
    503 : {'oi_status': 28, 'product__sub_type_flow': 503, 'product__type_flow': 5}
}

SERVICE_ACTIVE_SATUSES_FILTER = {
    501: {'oi_status': 28},
    503: {'oi_status': 28},
}

days_to_campign_name = {
    7: 'renewalbefore7days',
    3: 'renewalbefore3days',
    0: 'renewalonday',
    -3: 'renewalafter3days',
}

COUNT = 0
class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        # run for following days
        days_to_consider = [7, 3, 0, -3]
        logging.getLogger('info_log').info("Starting service expiry mail send.")
        for day in days_to_consider:
            service_expiry_reminder(day)


def check_if_going_to_expire(oi, days=0):
    """
    this function takes order item service object and days and calculated if service
    if gonna expire after days provided.

    default days is 0: it will check if service is gonna expire today.
    """
    expiry_date = timezone.now() + datetime.timedelta(days=days)
    start_expiry_date = expiry_date.replace(hour=0, minute=0, second=0)
    end_expiry_date = expiry_date.replace(hour=23, minute=59, second=59)
    if days >= 0:
        expiration_date = get_expiry_date(oi)
    else:
        expiration_date = oi.closed_on
    if expiration_date > start_expiry_date and expiration_date < end_expiry_date:
        return True


def get_expiry_date(oi):
    """
    This function takes the order item object and returns expiry datetime for 
    the service.
    if no date exist for service created operation, then return empty string.
    """
    service_obj_op = oi.orderitemoperation_set.filter(
        **SERVICE_ACTIVE_SATUSES_FILTER[oi.product.sub_type_flow]
    ).order_by('id').order_by('id').first()

    if not service_obj_op or not service_obj_op.created:
        logging.getLogger('error_log').error("unable to create activation date%s" % (str(e)))
        return ''

    activation_date = service_obj_op.created
    duration_dict = {
        'service': getattr(oi.product.attr, S_ATTR_DICT.get('FD'), 180),
    }
    duration_days = duration_dict.get(oi.product.product_class.name)
    expiration_date = activation_date + datetime.timedelta(days=duration_days)
    return expiration_date


def service_expiry_reminder(days):
    global COUNT
    for val in SERVICES.values():
        if days >= 0:
            ois = OrderItem.objects.filter(**val)
        else: # this filter is for closed order in the past
            closed_date = timezone.now() + datetime.timedelta(days=days)
            closed_date = closed_date.replace(hour=0, minute=0, second=0)
            if 'oi_status' in val:
                val.update({'oi_status': 4}, )
            ois = OrderItem.objects.filter(**val).filter(oi_status=4, closed_on__gt=closed_date)
        for oi in ois:
            expire_soon = check_if_going_to_expire(oi, days)
            if not expire_soon:
                continue
            COUNT += 1
            send_mail_for_service(oi, days)


def send_mail_for_service(oi, days):
    global COUNT
    if days >= 0:
        mail_type = "SERVICE_EXPIRY_REMINDER"
        subject = "Your service is expiring soon"
    else:
        mail_type = "SERVICE_EXPIRED_REMINDER"
        subject = "Your service has expired"
    to_emails = [oi.order.get_email()]
    email_dict = {}
    product_url = "{}://{}{}".format(
            settings.SITE_PROTOCOL, settings.SITE_DOMAIN,
            oi.product.get_absolute_url())

    # add campaign name in url
    campaign = days_to_campign_name.get(days, '')
    if campaign:
        product_url += '?utm_campaign=' + campaign

    # get expiry date for service
    expiry_date = get_expiry_date(oi)
    if expiry_date:
        expiry_date = expiry_date.strftime('%d %B %Y')
    email_dict.update({
        "subject": subject,
        "candidate_name": oi.order.first_name,
        'oi': oi,
        'product': oi.product.heading,
        'expiration_date': expiry_date,
        'product_url': product_url,
        "mobile": oi.order.mobile,
    })

    try:
        SendMail().send(to_emails, mail_type, email_dict)
    except Exception as e:
        logging.getLogger('error_log').error(
            "%s - %s - %s" % (
                str(to_emails), str(e), str(mail_type)))

    # Send sms only if service is expiring today, as per product requirement
    if days == 0:
        try:
            SendSMS().send(sms_type=mail_type, data=email_dict)
        except Exception as e:
            logging.getLogger('error_log').error(
                "%s - %s - %s" % (
                    str(to_emails), str(e), str(mail_type)))

    logging.getLogger('info_log').info("{} mails has been sent for service expiry reminder.".format(COUNT))
