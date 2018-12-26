#python imports
import sys,os,django
import csv
from io import StringIO
from dateutil import relativedelta
from datetime import datetime,timedelta
from collections import OrderedDict
import logging
#django imports
from django.utils import timezone

#Settings imports
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "careerplus.config.settings")
ROOT_FOLDER = os.path.realpath(os.path.dirname(__file__))
ROOT_FOLDER = ROOT_FOLDER[:ROOT_FOLDER.rindex('/')]
if ROOT_FOLDER not in sys.path:
    sys.path.insert(1, ROOT_FOLDER + '/')
django.setup()

from django.conf import settings

#internal imports
from order.models import Order,WelcomeCallOperation
from emailers.email import SendMail



def date_diff(date1,date2):
   datediff = relativedelta.relativedelta(date1, date2)
   return str(datediff.days) + '-days-' + str(datediff.hours)+'-hours-'\
          +str(datediff.minutes)+'-minutes'

def date_timezone_convert(date=None):
    from pytz import timezone
    if not date:
        return 'N.A'
    return date.astimezone(timezone(settings.TIME_ZONE))

def get_na_list(param=5):
    return ['NA'] * param


def mail_report(csvfile):
    send_dict = {}
    send_dict['subject'] = "Welcome call Report Generated on " + timezone.now().strftime("%Y-%m-%d ")
    send_dict['to'] = ["vishal.gupta@hindustantimes.com", "purnima.ganguly@shine.com", "vinod@shine.com",
        "nishant.shukla@hindustantimes.com"]
    send_dict['cc'] = ["sidharth.gupta1@hindustantimes.com"]
    send_dict['body'] = 'Please find attached .csv file containing information \
            about welcome call '
    send_dict['from_email'] = settings.DEFAULT_FROM_EMAIL
    file_name = "%s.csv" % ('welcome_call_report' + timezone.now().strftime("%Y-%m-%d "))
    SendMail().base_send_mail(subject=send_dict['subject'], body=send_dict['body'], to=send_dict['to'],
        cc=send_dict['cc'], from_email=send_dict['from_email'],
        attachments=[file_name, csvfile.getvalue(), 'text/csv'], mimetype='text/csv')
    logging.getLogger('info_log').info("welcome call generated")

def generate_report(duration_report):
    cur_datetime = timezone.now()
    cur_datetime = datetime(cur_datetime.year, cur_datetime.month \
        , cur_datetime.day, 0, 0, 0)
    #setting last_duration for a week
    last_duration = cur_datetime - timedelta(days=7)
    if duration_report == 'monthly':
        #setting last_duration for a month
        last_duration = cur_datetime + relativedelta.relativedelta(months=-1)
    order_objects = Order.objects.filter(created__range=[last_duration,cur_datetime],status__in=[1,2,3])
    if not order_objects:
        logging.getLogger('error_log').info("welcome call not generated")
        return

    try:
        csvfile = StringIO()
        csvwriter = csv.writer(csvfile, delimiter=',', quotechar="'", \
            quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(['Order ID', 'Order_payment_date', 'Order_created_date', \
            'First_Touch_Assigned_to','First_Touch_Welcome call Date','First_Touch_Welcome call Status',\
            'First_Touch_Welcome Call Status - Category',
            'First_Touch_Welcome Call Status - SubCategory',\
            'First_Touch_Create_Difference','Current_Touch_Assigned_to',
            'Current_Touch_Welcome call Date', 'Current_Touch_Welcome call Status', \
            'Current_Touch_Welcome Call Status - Category',\
            'Current_Touch_Welcome Call Status - SubCategory', \
            'Current_Touch_Create_Difference','Final_Touch_Assigned_to', \
            'Final_Touch_Welcome call Date',\
            'Final_Touch_Welcome call Status', \
            'Final_Touch_Welcome Call Status - Category', \
            'Final_Touch_Welcome Call Status - SubCategory', \
            'Final_Touch_Create_Difference',
            ])

        for order in order_objects:
            row = []
            pay_date_order = date_timezone_convert(order.payment_date) #order payment date
            row.append('CP' + str(order.pk))
            row.append(date_timezone_convert(order.payment_date)\
                .strftime('%m/%d/%Y %H:%M:%S'))
            row.append(date_timezone_convert(order.created)\
                .strftime('%m/%d/%Y %H:%M:%S'))
            welc_objects = WelcomeCallOperation.objects.filter(order_id=order.id)\
                .exclude(wc_status=1).order_by('id')
            if welc_objects:
                welc_obj = welc_objects.first()
                agent_info=welc_obj.assigned_to
                row.append(agent_info.name if agent_info else "N.A")
                row.append(date_timezone_convert(welc_obj.created)\
                    .strftime('%m/%d/%Y %H:%M:%S'))
                ist_date_welcome = date_timezone_convert(welc_obj.created)
                row.append(welc_obj.get_wc_status("N.A"))
                row.append(welc_obj.get_wc_cat("N.A"))
                row.append(welc_obj.get_wc_sub_cat("N.A"))
                row.append(date_diff(ist_date_welcome,pay_date_order))
                curren_welcome_obj = welc_objects.exclude(wc_status__in=[41,42,63])\
                    .order_by('id').last()
                if curren_welcome_obj:
                    agent_info = curren_welcome_obj.assigned_to
                    row.append(agent_info.name if agent_info else "N.A")
                    row.append(date_timezone_convert(curren_welcome_obj.created)\
                        .strftime(
                        '%m/%d/%Y %H:%M:%S'))
                    ist_date_welcome = date_timezone_convert(curren_welcome_obj.created)
                    row.append(curren_welcome_obj.get_wc_status("N.A"))
                    row.append(curren_welcome_obj.get_wc_cat("N.A"))
                    row.append(curren_welcome_obj.get_wc_sub_cat("N.A"))
                    row.append(date_diff(ist_date_welcome, pay_date_order))
                else:
                    row += get_na_list(6)
                closed_welcome = welc_objects.filter(wc_status__in=[41,42,63])\
                        .order_by('id').last()
                if closed_welcome:
                    agent_info = closed_welcome.assigned_to
                    row.append(agent_info.name if agent_info else "N.A")
                    row.append(date_timezone_convert(closed_welcome.created)\
                        .strftime('%m/%d/%Y %H:%M:%S'))
                    ist_date_welcome = date_timezone_convert(closed_welcome.created)
                    row.append(closed_welcome.get_wc_status("N.A"))
                    row.append(closed_welcome.get_wc_cat("N.A"))
                    row.append(closed_welcome.get_wc_sub_cat("N.A"))
                    row.append(date_diff(ist_date_welcome, pay_date_order))
                else:
                    row += get_na_list(6)
                csvwriter.writerow(row)
            else:
                row += get_na_list(param=18)
                csvwriter.writerow(row)
        mail_report(csvfile)

    except Exception as e:
        logging.getLogger('error_log').error('unable to create welcome call report%s' % str(e))

if __name__ == "__main__":
    duration_report = None
    if 'monthly' in sys.argv:
        duration_report = 'monthly'
    generate_report(duration_report)








