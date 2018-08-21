import logging
import datetime

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings
from linkedin.autologin import AutoLogin
from order.models import OrderItem
from emailers.tasks import send_email_task
from emailers.sms import SendSMS
from order.functions import create_short_url


class Command(BaseCommand):
    """
        Daily Cron for draft reminder mail/Sms
    """

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def handle(self, *args, **options):
        draft_reminder_mail_for_linkedin()


def draft_reminder_mail_for_linkedin():
    try:
        orderitems = OrderItem.objects.filter(
            oi_status=46, product__type_flow=8).select_related('order', 'product')
        count = 0
        for oi in orderitems:
            if not oi.approved_on:
                oi.approved_on = timezone.now()
                oi.save()
            approved_date = oi.approved_on.date()
            today_date = timezone.now().date()
            draft_level = oi.draft_counter
            email_sets = oi.emailorderitemoperation_set.filter(email_oi_status=106) if draft_level == 1 else oi.emailorderitemoperation_set.filter(email_oi_status=107)
            token = AutoLogin().encode(
                oi.order.email, oi.order.candidate_id, days=None)
            if draft_level == 1 and today_date >= approved_date + datetime.timedelta(days=8) and len(email_sets) == 0:
                to_emails = [oi.order.get_email()]
                mail_type = 'REMINDER'
                data = {}
                data.update({
                    "subject": "Reminder:Your developed resume document has been uploaded",
                    "draft_level": draft_level,
                    "first_name": oi.order.first_name,
                    'mobile': oi.order.get_mobile(),
                    'days': 22,
                    'upload_url': "%s://%s/autologin/%s/?next=/dashboard" % (
                        settings.SITE_PROTOCOL, settings.SITE_DOMAIN, token),
                })
                send_email_task.delay(
                    to_emails, mail_type, data, status=106, oi=oi.pk)
                try:
                    urlshortener = create_short_url(login_url=data)
                    data.update({'url': urlshortener.get('url')})
                    SendSMS().send(sms_type=mail_type, data=data)
                    logging.getLogger('info_log').info(
                        "{} 8 day linkedin SMS Sent".format(count))
                except Exception as e:
                    logging.getLogger('error_log').error(
                        "%s - %s" % (str(mail_type), str(e)))

            elif draft_level == 1 and today_date >= approved_date + datetime.timedelta(days=15) and len(email_sets) == 1:

                to_emails = [oi.order.get_email()]
                mail_type = 'REMINDER'
                data = {}
                data.update({
                    "subject": "Reminder:Your developed resume document has been uploaded",
                    "draft_level": draft_level,
                    "first_name": oi.order.first_name,
                    'mobile': oi.order.get_mobile(),
                    'days': 15,
                    'upload_url': "%s://%s/autologin/%s/?next=/dashboard" % (
                        settings.SITE_PROTOCOL, settings.SITE_DOMAIN, token),
                })
                send_email_task.delay(to_emails, mail_type, data, status=106, oi=oi.pk)
                try:
                    SendSMS().send(sms_type=mail_type, data=data)
                    logging.getLogger('info_log').info(
                        "{} 15 day linkedin SMS & Email Sent".format(count))
                except Exception as e:
                    logging.getLogger('error_log').error("%s - %s" % (str(mail_type), str(e)))

            elif draft_level == 1 and today_date >= approved_date + datetime.timedelta(days=22) and len(email_sets) == 2:
                to_emails = [oi.order.get_email()]
                mail_type = 'REMINDER'
                data = {}
                data.update({
                    "subject": "Reminder:Your developed resume document has been uploaded",
                    "draft_level": draft_level,
                    "first_name": oi.order.first_name,
                    'mobile': oi.order.get_mobile(),
                    'days': 7,
                    'upload_url': "%s://%s/autologin/%s/?next=/dashboard" % (
                        settings.SITE_PROTOCOL, settings.SITE_DOMAIN, token),
                })
                send_email_task.delay(
                    to_emails, mail_type, data, status=106, oi=oi.pk)
                try:
                    urlshortener = create_short_url(login_url=data)
                    data.update({'url': urlshortener.get('url')})
                    SendSMS().send(sms_type=mail_type, data=data)
                    logging.getLogger('info_log').info(
                        "{} 22 day linkedin SMS & Email Sent".format(count))
                except Exception as e:
                    logging.getLogger('error_log').error(
                        "%s - %s" % (str(mail_type), str(e)))

            elif draft_level == 1 and today_date >= approved_date + datetime.timedelta(days=29) and len(email_sets) == 3:
                to_emails = [oi.order.get_email()]
                mail_type = 'WRITING_SERVICE_CLOSED'
                email_dict = {}
                email_dict.update({
                    "subject": 'Closing your ' + oi.product.name + ' service',
                    "username": oi.order.first_name,
                    'draft_added': oi.draft_added_on,
                    'mobile': oi.order.get_mobile(),
                    'upload_url': "%s://%s/autologin/%s/?next=/dashboard" % (
                        settings.SITE_PROTOCOL, settings.SITE_DOMAIN, token),
                })
                send_email_task.delay(
                    to_emails, mail_type, email_dict, status=9, oi=oi.pk)
                try:
                    urlshortener = create_short_url(login_url=email_dict)
                    data.update({'url': urlshortener.get('url')})
                    SendSMS().send(sms_type=mail_type, data=email_dict)
                    logging.getLogger('info_log').info(
                        "{} linekdin Service closed SMS & Email Sent".format(count))
                except Exception as e:
                    logging.getLogger('error_log').error(
                        "%s - %s" % (str(mail_type), str(e)))

                last_oi_status = oi.oi_status
                oi.oi_status = 4
                oi.last_oi_status = last_oi_status
                oi.closed_on = timezone.now()
                oi.save()
                oi.orderitemoperation_set.create(
                    oi_status=oi.oi_status,
                    last_oi_status=oi.last_oi_status,
                    assigned_to=oi.assigned_to)

            elif draft_level == 2 and today_date >= approved_date + datetime.timedelta(days=4) and len(email_sets) == 0:
                to_emails = [oi.order.get_email()]
                mail_type = 'REMINDER'
                data = {}
                data.update({
                    "subject": "Reminder:Your developed resume document has been uploaded",
                    "draft_level": draft_level,
                    "first_name": oi.order.first_name,
                    'mobile': oi.order.get_mobile(),
                    'days': 7,
                    'upload_url': "%s://%s/autologin/%s/?next=/dashboard" % (
                        settings.SITE_PROTOCOL, settings.SITE_DOMAIN, token),
                })
                send_email_task.delay(
                    to_emails, mail_type, data, status=107, oi=oi.pk)
                try:
                    urlshortener = create_short_url(login_url=data)
                    data.update({'url': urlshortener.get('url')})
                    SendSMS().send(sms_type=mail_type, data=data)
                    logging.getLogger('info_log').info(
                        "{} level 2 linkedin SMS Sent".format(count))
                except Exception as e:
                    logging.getLogger('error_log').error("%s - %s" % (str(mail_type), str(e)))

            elif draft_level == 2 and today_date >= approved_date + datetime.timedelta(days=7) and len(email_sets) == 1:
                to_emails = [oi.order.get_email()]
                mail_type = 'REMINDER'
                data = {}
                data.update({
                    "subject": "Reminder:Your developed resume document has been uploaded",
                    "draft_level": draft_level,
                    "first_name": oi.order.first_name,
                    'mobile': oi.order.get_mobile(),
                    'days': 3,
                    'upload_url': "%s://%s/autologin/%s/?next=/dashboard" % (
                        settings.SITE_PROTOCOL, settings.SITE_DOMAIN, token),
                })
                send_email_task.delay(
                    to_emails, mail_type, data, status=107, oi=oi.pk)
                try:
                    urlshortener = create_short_url(login_url=data)
                    data.update({'url': urlshortener.get('url')})
                    SendSMS().send(sms_type=mail_type, data=data)
                    logging.getLogger('info_log').info(
                        "{} level 2 7 day linkedin SMS Sent".format(count))
                except Exception as e:
                    logging.getLogger('error_log').error(
                        "%s - %s" % (str(mail_type), str(e)))

            elif draft_level == 2 and today_date >= approved_date + datetime.timedelta(days=10) and len(email_sets) == 2:
                to_emails = [oi.order.get_email]
                mail_type = 'WRITING_SERVICE_CLOSED'
                email_dict = {}
                email_dict.update({
                    "subject": 'Closing your ' + oi.product.name + ' service',
                    "username": oi.order.first_name,
                    'draft_added': oi.draft_added_on,
                    'mobile': oi.order.get_mobile(),
                    'upload_url': "%s://%s/autologin/%s/?next=/dashboard" % (
                        settings.SITE_PROTOCOL, settings.SITE_DOMAIN, token),
                })

                try:
                    send_email_task.delay(
                        to_emails, mail_type, email_dict,
                        status=9, oi=oi.pk)
                    logging.getLogger('info_log').info(
                        "{} Service closed Email Sent".format(count))
                except Exception as e:
                    logging.getLogger('error_log').error(
                        "%s - %s - %s" % (
                            str(to_emails), str(e), str(mail_type)))

                try:
                    SendSMS().send(sms_type=mail_type, data=email_dict)
                    logging.getLogger('info_log').info(
                        "{} SService closed SMS Sent".format(count))
                except Exception as e:
                    logging.getLogger('error_log').error(
                        "%s - %s" % (str(mail_type), str(e)))

                last_oi_status = oi.oi_status
                oi.oi_status = 4
                oi.last_oi_status = last_oi_status
                oi.closed_on = timezone.now()
                oi.save()
                oi.orderitemoperation_set.create(
                    oi_status=oi.oi_status,
                    last_oi_status=oi.last_oi_status,
                    assigned_to=oi.assigned_to)
    except Exception as e:
        logging.getLogger('error_log').error("%s - %s" % (
            "Reminder mail cron", str(e)))