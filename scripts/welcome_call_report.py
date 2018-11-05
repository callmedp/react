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
from django.conf import settings


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "careerplus.config.settings")
ROOT_FOLDER = os.path.realpath(os.path.dirname(__file__))
ROOT_FOLDER = ROOT_FOLDER[:ROOT_FOLDER.rindex('/')]
if ROOT_FOLDER not in sys.path:
    sys.path.insert(1, ROOT_FOLDER + '/')
django.setup()

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


def main(argv):
    cur_datetime = timezone.now()
    cur_date_end = datetime(cur_datetime.year, cur_datetime.month \
        , cur_datetime.day, 23, 59, 59)
    #setting last_duration for a week
    last_duration = cur_datetime - timedelta(days=7)

    if argv == 'monthly':
        #setting last_duration for a month
        last_duration = cur_datetime + relativedelta.relativedelta(months=-1)

    order_objects = Order.objects.filter(created__gte=last_duration,status__in=[1,2,3])

    try:
        send_dict = {}
        csvfile = StringIO()
        csvwriter = csv.writer(csvfile, delimiter=',', quotechar="'", \
            quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(['Order ID', 'Order_payment_date', 'Order_created_date', \
            'Welcome call Date','Welcome call Status','Welcome Call Status - Category',\
            'Welcome Call Status - SubCategory', 'Days difference'])
        def order_status(order):
            row = OrderedDict()
            row['Order ID'] = 'CP' + str(order.pk)
            row['Order_payment_date'] = date_timezone_convert(order.payment_date)\
                .strftime('%m/%d/%Y %H:%M:%S')
            row['Order_created_date'] = date_timezone_convert(order.created)\
                .strftime('%m/%d/%Y %H:%M:%S')
            return row
        for order in order_objects:
            row = OrderedDict()
            welc_objects = WelcomeCallOperation.objects.filter(order_id=order.id)\
                .order_by('created')
            base_dict = order_status(order)

            for welc_obj in welc_objects:
                row = OrderedDict(base_dict)
                row['Welcome Call Date'] = date_timezone_convert(welc_obj.created)\
                    .strftime('%m/%d/%Y %H:%M:%S')
                ist_date_welcome = date_timezone_convert(welc_obj.created)
                ist_date_order = date_timezone_convert(order.created)
                row['Welcome Call Status'] = welc_obj.get_wc_status("N.A")
                row['Welcome Call Status - Category'] = welc_obj.get_wc_cat("N.A")
                row['Welcome Call Status - SubCategory'] = welc_obj.get_wc_sub_cat("N.A")
                row['Days difference'] = date_diff(ist_date_welcome,ist_date_order)
                csvwriter.writerow(row.values())

            if not welc_objects:
                row = OrderedDict(base_dict)
                row['Welcome Call Status'] = "N.A"
                row['Welcome Call Date'] = 'NA'
                row['Welcome Call Status - Category'] = "N.A"
                row['Welcome Call Status - SubCategory'] = "N.A"
                row['Days difference'] = 'NA'
                csvwriter.writerow(row.values())
        send_dict['subject'] = "Welcome call Report"
        send_dict['to'] = ["vishal.gupta@hindustantimes.com","purnima.ganguly@shine.com",\
            "vinod@shine.com","nishant.shukla@hindustantimes.com"]
        send_dict['cc'] = ["sidharth.gupta1@hindustantimes.com"]
        send_dict['body'] = 'Please find attached .csv file containing information \
        about welcome call '
        send_dict['from_email'] = settings.CONSULTANTS_EMAIL
        file_name = "%s.csv" % ('welcome_call_report' + timezone.now().strftime("%Y-%m-%d "))
        if order_objects:
            SendMail().base_send_mail(subject="welcome_call_report", body=send_dict.get('body'),
                to= send_dict.get(
                'to'), cc=send_dict.get('cc'), from_email=send_dict.get('from_email', None),
                attachments=[file_name, csvfile.getvalue(), 'text/csv'], mimetype='text/csv')
            logging.getLogger('info_log').info(
                "welcome call generated")


    except Exception as e:
        logging.getLogger('error_log').error('unable to create welcome call report%s' % str(e))


if __name__ == "__main__":
    param = None
    if 'monthly' in sys.argv:
        param = 'monthly'
    main(param)








