#python imports
import codecs
from datetime import datetime, timedelta
import os,django,sys,json,ast,re,pytz,logging
from hashlib import sha512

#Settings imports
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "careerplus.config.settings")
ROOT_FOLDER = os.path.realpath(os.path.dirname(__file__))
ROOT_FOLDER = ROOT_FOLDER[:ROOT_FOLDER.rindex('/')]
if ROOT_FOLDER not in sys.path:
    sys.path.insert(1, ROOT_FOLDER + '/')
django.setup()

#django imports
from django.conf import settings
from django.utils import timezone

#local imports

#inter app imports
from order.models import Order
from payment.models import PaymentTxn
from payment.mixin import PaymentMixin

#third party imports
import requests
from requests.models import Request


KEYS=('key','command','var1')
success_payment_updated = 0


def orders_numbers_params(orders):
    if not orders:
        return None
    return "|".join(obj.txn for obj in orders)

def create_params (var,command):

    data = {}
    data.update({'var1': var, 'key': settings.PAYU_INFO.get('merchant_key'), 'command': command})
    hash_value = generate_payu_hash(data)
    data.update({'hash': hash_value})
    return data


def generate_payu_hash(data):
    hash = sha512(b'')
    for key in KEYS:
        hash.update(str.encode("%s%s" % (str(data.get(key, '')), '|')))
    hash.update(str.encode(settings.PAYU_INFO.get('merchant_salt')))
    return hash.hexdigest().lower()


def update_transaction_object(order_status, txn_obj, ):
    global success_payment_updated
    if order_status == 'success':
        payment_mixin_obj = PaymentMixin()
        request_obj = Request()
        setattr(request_obj, "session", {})
        payment_mixin_obj.process_payment_method(
            payment_type='PAYU', request=request_obj,
            txn_obj=txn_obj)
        success_payment_updated += 1

    elif order_status == 'failure':
        txn_obj.status = 2
        txn_obj.save()


if __name__ == "__main__":
    command = "verify_payment"
    utc_tz = pytz.timezone('UTC')
    current_utc_time = datetime.utcnow().replace(tzinfo=utc_tz)
    time_intervals_to_check = [5]

    for interval in time_intervals_to_check:
        sdt = (current_utc_time - timedelta(days=7)).replace(
            tzinfo=utc_tz)
        edt = (sdt + timedelta(minutes=2)).replace(tzinfo=utc_tz) #Hour + buffer
        all_initiated_transactions = PaymentTxn.objects.filter(status__in=[0,2,3,4,5],\
                payment_mode=13,created__gte=sdt,order__site=0)

        logging.getLogger('info_log').info( "Total payu initiated "
         "transactions for interval {} minutes - {}".format(interval,
                                    all_initiated_transactions.count()))

        var1 = orders_numbers_params(all_initiated_transactions)
        if not var1:
            continue
        params_data = create_params(var1, command)
        try:
            res = requests.post(settings.PAYU_INFO.get('web_api_url'),
                                params_data)
        except Exception as e:
            logging.getLogger('error_log').error(
                "Unable to read PayU response %s" % str(e))
            continue

        if not res or not res.status_code == 200:
            logging.getLogger('error_log').error(
                "PAYU Response code failure - {} {}". \
                format(res.status_code, var1))
            continue
        response_json = json.loads(res.text)
        transactions_data = response_json.get('transaction_details', {})
        if not transactions_data or type(transactions_data) != dict:
            continue
        all_txn_keys = transactions_data.keys()
        for txn in all_txn_keys:
            order_desc = ""
            try:
                order_status = json.dumps(transactions_data[txn])
            except Exception as e:
                logging.getLogger('error_log').error("error in creating payu "
                        "txn response dump {}".format(transactions_data[txn]))
                order_status = json.dumps({})
            txn_object = all_initiated_transactions.filter(txn=txn).first()
            txn_object.txn_info = order_status
            txn_object.save()
            update_transaction_object(transactions_data[txn]['status'].lower(),
                                      txn_object)

    logging.getLogger('info_log').info(
        "Total successful transactions - {}".format(success_payment_updated))





