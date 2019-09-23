#python imports
from datetime import datetime, timedelta
import os,django,sys,json,pytz,logging

#Settings imports
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "careerplus.config.settings")
ROOT_FOLDER = os.path.realpath(os.path.dirname(__file__))
ROOT_FOLDER = ROOT_FOLDER[:ROOT_FOLDER.rindex('/')]
if ROOT_FOLDER not in sys.path:
    sys.path.insert(1, ROOT_FOLDER + '/')
django.setup()


#django imports

#local imports

#inter app imports

from payment.utils import ZestMoneyUtil
from payment.models import PaymentTxn

#third party imports

#Global Constants
SUCCESSFUL_TRANSACTIONS = 0
DAYS_DELTA = 7

status_text_mapping = {
                     'applicationinprogress': 'Loan application is in progress',
                     'approved': 'Loan application has been approved',
                     'bankaccountdetailscomplete': 'Customer has completed his bank account details',
                     'cancelled': 'Loan application has been cancelled',
                     'customercancelled': 'Loan application has been cancelled by the customer',
                     'declined': 'Loan application was declined',
                     'depositpaid': 'The customer has either made the downpayment, or chose to pay on delivery (if available)',
                     'documentscomplete': 'The customer has uploaded all the required documents',
                     'loanagreementaccepted': 'The customer has signed the loan agreement',
                     'merchantcancelled': 'Loan application was cancelled by the merchant',
                     'outofstock': 'Some of the items in the order are out of stock and the loan application was cancelled',
                     'preaccepted': 'Loan application was pre-accepted by automated risk process',
                     'riskpending': 'Risk decision pending',
                     'timeoutcancelled': 'Loan application was cancelled by a timeout mechanism (customer did not complete the application in time)'
                     }

zest_status_payment_status_mapping = {"cancelled":5,
                                    "customercancelled":5,
                                    "declined":2,
                                    "merchantcancelled":5,
                                    "outofstock":5,
                                    "timeoutcancelled":3,
                                    }

approval_pending_status = ["bankaccountdetailscomplete","applicationinprogress","depositpaid",\
                            "documentscomplete","loanagreementaccepted","riskpending"]

if __name__ == "__main__":
    utc_tz = pytz.timezone('UTC')
    current_utc_time = datetime.utcnow().replace(tzinfo=utc_tz)
    zest_obj = ZestMoneyUtil()

    for delta in range(DAYS_DELTA+1):
        edt = (current_utc_time - timedelta(days=delta)).replace(tzinfo=utc_tz)
        sdt = (edt - timedelta(days=delta+1)).replace(tzinfo=utc_tz)
        all_initiated_transactions = PaymentTxn.objects.filter(status__in=[0,2,3,4,5],\
                payment_mode=14,created__gte=sdt,created__lte=edt,order__site=0)
        logging.getLogger('info_log').info("number {}".format(len(all_initiated_transactions)))

        for transaction in all_initiated_transactions:
            order_status = zest_obj.fetch_order_status(transaction).lower()
            
            if order_status in ["preaccepted","approved","active"]:
                transaction.status = 1
                pay_day = datetime.now()
                transaction.payment_date = pay_day
                success_text = status_text_mapping.get (order_status, "")
                success_text = json.dumps(success_text)
                transaction.txn_info = success_text
                transaction.save()
                order = transaction.order
                order.status = 1
                order.payment_date = pay_day
                order.save()
                SUCCESSFUL_TRANSACTIONS += 1
                continue
            
            if order_status in approval_pending_status:
                success_text = status_text_mapping.get(order_status, "")
                success_text = json.dumps(success_text)
                transaction.txn_info = success_text
                transaction.status = 0
                transaction.save()
                continue

            failure_text = status_text_mapping.get(order_status,"")
            failure_status = zest_status_payment_status_mapping.get(order_status,0)
            logging.getLogger('info_log').info("Zest Order Update {},{}".\
                    format(order_status,transaction.id))

            transaction.txn_status = failure_status
            transaction.failure_desc = failure_text
            transaction.save()

    logging.getLogger('info_log').info(\
        "Total successful transactions - {}".format(SUCCESSFUL_TRANSACTIONS))




