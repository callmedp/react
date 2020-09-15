# python imports
from datetime import datetime, timedelta
import os, django, sys, pytz, logging ,json

# Settings imports
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "careerplus.config.settings_staging")
ROOT_FOLDER = os.path.realpath(os.path.dirname(__file__))
ROOT_FOLDER = ROOT_FOLDER[:ROOT_FOLDER.rindex('/')]
if ROOT_FOLDER not in sys.path:
    sys.path.insert(1, ROOT_FOLDER + '/')
django.setup()

# django imports
from django.utils import timezone

# local imports

# inter app imports
from payment.models import PaymentTxn
from payment.razor import RazorPaymentUtil
from requests.models import Request
from payment.mixin import PaymentMixin


def close_cart_obj(cart_obj):
    if not cart_obj:
        return
    last_status = cart_obj.status
    cart_obj.status = 5
    cart_obj.last_status = last_status
    cart_obj.date_closed = timezone.now()
    cart_obj.save()



def update_transaction(txn_obj,r_id):
    payment_mixin_obj = PaymentMixin()
    order = txn_obj.order
    close_cart_obj(txn_obj.cart)
    request_obj = Request()
    setattr(request_obj, "session", {})
    txn_obj.txn_info = str(txn_obj)
    payment_mixin_obj.process_payment_method(
        payment_type='RAZORPAY', request=request_obj,
        txn_obj=txn_obj,
        data={'order_id': order.pk, 'razorpay_payment_id': r_id})



if __name__ == "__main__":
    utc_tz = pytz.timezone('UTC')
    current_utc_time = datetime.utcnow().replace(tzinfo=utc_tz)
    time_intervals_to_check = [5, 15, 240, 1440]
    razor_object = RazorPaymentUtil()

    for interval in time_intervals_to_check:
        sdt = (current_utc_time - timedelta(minutes=interval)).replace(tzinfo=utc_tz)
        edt = (sdt + timedelta(minutes=2)).replace(tzinfo=utc_tz)  # Hour + buffer
        all_initiated_transactions = PaymentTxn.objects.filter(status__in=[0, 2, 3, 4, 5],\
                                                               payment_mode=15, created__gte=sdt,
                                                               created__lte=edt)
        logging.getLogger('info_log').info(\
            "Total razorpay initiated transactions for interval {} minutes - {}".format(\
                interval, all_initiated_transactions.count()))

        for txn in all_initiated_transactions:
            if not txn.razor_order_id:
                logging.getLogger('info_log').info("Razor Order id not found for {}".format(txn.id))
                continue
            txn_response = razor_object.fetch_payment(txn.razor_order_id)
            if not txn_response:
                logging.getLogger('info_log').info('No response from razorpay for {}'.format(txn.id))
                continue
            txn_response = txn_response.json()
            if not txn_response.get('count', False):
                logging.getLogger('info_log').info("No Payment fetched from razorpay {}".format(txn.id))
                continue
            txn_obj = txn_response.get('items')
            if not txn_obj or not isinstance(txn_obj,list):
                logging.getLogger('info_log').info('no item found for txn {}'.format(txn.id))
                continue
            txn_obj = txn_obj[0]
            payment_date = datetime.utcfromtimestamp(int(txn_obj.get('created_at'))) if txn_obj.get('created_at',
                                                                                                 '') else datetime.utcnow().replace(tzinfo=utc_tz)

            if txn_obj.get('status','').lower() == 'captured' and txn_obj.get('id'):
                update_transaction(txn,txn_obj.get('id'))


            if txn_obj.get('status','').lower() == 'failed':
                txn.txn_info  = json.dumps(txn_obj)
                txn.status = 2
                txn.save()





