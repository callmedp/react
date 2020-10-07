import csv
import datetime
import StringIO
import logging

from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils import timezone

from mailers.email import SendMail
from shinecp.theme.models import UserQuries

TODAY = timezone.now()
YESTERDAY = TODAY + datetime.timedelta(days=-1)


class Command(BaseCommand):
    """
        Generate daily report of Shine Roundone JD clicks
    """
    help = 'Generate daily report of Shine Roundone JD clicks'

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def handle(self, *args, **options):
        shine_roundone_report()


def shine_roundone_report():
    try:
        send_dict = {}
        attachments = ['roundone_jd_click']
        send_dict['subject'] = "Daily RounOne Report"
        send_dict['to'] = ['vinod@shine.com','karminder.kaur@hindustantimes.com']
        send_dict['body'] = 'Please find attached .csv file containing \
        information about RoundOne Shine JD clicks on ' + \
            YESTERDAY.strftime("%Y-%m-%d ")
        send_dict['cc'] = ["karminder.kaur@hindustantimes.com"]
        send_dict['from_email'] = settings.CONSULTANTS_EMAIL

        filepath = settings.SHINE_ROUNDONE_CLICK + '/roundone_click' + YESTERDAY.strftime("%Y-%m-%d") +'.csv'
        attachments.append(filepath)
        SendMail().base_send_mail(
            subject="Daily RounOne Report", body=send_dict.get('body'),
            to=send_dict.get('to'), cc=send_dict.get('cc'),
            from_email=send_dict.get('from_email', None),
            attachments=attachments,#[attachments, csvfile.getvalue(), 'text/csv'],
            mimetype='text/csv')
    except Exception as excep:
        logging.getLogger('error_log').error("%s - %s" % (
            "Daily RounOne Report", str(excep)))
