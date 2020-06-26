#python imports
import csv
import logging
from io import StringIO
from collections import OrderedDict

#django imports
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings

#local imports

#inter app imports
from order.models import Order
from emailers.email import SendMail

#third party imports

class Command(BaseCommand):
    def handle(self, *args, **options):
        close_order_report()


def close_order_report():
    """ 
    Closing order report using this cron 
    """

    paid_orders = Order.objects.filter(status=1)
    closed_order = 0
    try:
        send_dict = {}
        csvfile = StringIO()
        spamwriter = csv.writer(
            csvfile, delimiter=',', quotechar="'", quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(['id', 'candidate', 'added_on', 'closed_on'])

        for od in paid_orders:
            row_one = OrderedDict()
            open_ois = od.orderitems.filter(no_process=False).exclude(
                oi_status=4)
            if open_ois.exists():
                continue
            od.status = 3
            od.closed_on = timezone.now()
            od.save()
            row_one['id'] = od.pk
            row_one['candidate'] = od.candidate_id
            row_one['added_on'] = od.created
            row_one['modified_on'] = od.closed_on
            spamwriter.writerow(row_one.values())
            closed_order += 1
            
        send_dict['subject'] = "Order Closure Report"
        send_dict['to'] = ["heena.afshan@hindustantimes.com"]
        send_dict['cc'] = ["nidhish.sharma@hindustantimes.com","gaurav.chopra1@hindustantimes.com"]
        send_dict['body'] = 'Please find attached .csv file containing information about Order Closing '
        send_dict['from_email'] = settings.CONSULTANTS_EMAIL
        file_name = "%s.csv" % (
            'ORDER_CLOSER_REPORT_' + timezone.now().strftime("%Y-%m-%d "))
        if closed_order:
            SendMail().base_send_mail(
                subject="ORDER_CLOSER_REPORT_",
                body=send_dict.get('body'), to=send_dict.get('to'),
                cc=send_dict.get('cc'),
                from_email=send_dict.get('from_email', None),
                attachments=[file_name, csvfile.getvalue(), 'text/csv'],
                mimetype='text/csv')
            logging.getLogger('info_log').info(
                "{} orders are closed out of {}".format(
                    closed_order, paid_orders.count()))
    except Exception as e:
        logging.getLogger('error_log').error('unable SENND order closer report%s' % str(e))
        raise e
