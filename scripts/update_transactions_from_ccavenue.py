# python imports
import codecs
from datetime import datetime, timedelta
import os, django, sys, json, ast, re, pytz, logging

# Settings imports
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "careerplus.config.settings_live")
ROOT_FOLDER = os.path.realpath(os.path.dirname(__file__))
ROOT_FOLDER = ROOT_FOLDER[:ROOT_FOLDER.rindex('/')]
if ROOT_FOLDER not in sys.path:
    sys.path.insert(1, ROOT_FOLDER + '/')
django.setup()

# django imports
from django.conf import settings
from django.utils import timezone

# local imports

# inter app imports
from order.models import Order
from payment.models import PaymentTxn
from payment.mixin import PaymentMixin

# third party imports
import requests
from hashlib import md5
from Crypto.Cipher import AES
from requests.models import Request

# Global Constants
CCAVENUE_API_URL_BASE = "https://api.ccavenue.com/apis/servlet/DoWebTrans"
ESCAPE_CHARS = ['\r', '\n', '\x06', '\x08', '\x02', '\x04']
SUCCESSFUL_TRANSACTIONS = 0


class CCAvenueCrypto:

    def pad(self, data):
        length = 16 - (len(data)%16)
        data += chr(length)*length
        return data

    def encrypt(self, plainText, workingKey):
        iv = '\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f'
        plainText = self.pad(plainText)
        encDigest = md5()
        encDigest.update(workingKey.encode())
        enc_cipher = AES.new(encDigest.digest(), AES.MODE_CBC, iv)
        encryptedText = enc_cipher.encrypt(plainText).hex()
        return encryptedText

    def decrypt(self, cipherText, workingKey):
        iv = '\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f'
        decDigest = md5()
        decDigest.update(workingKey.encode())
        encryptedText = codecs.decode(cipherText, "hex")
        dec_cipher = AES.new(decDigest.digest(), AES.MODE_CBC, iv)
        decryptedText = dec_cipher.decrypt(encryptedText)
        return decryptedText.decode()


def get_clean_string(string):
    for escape_char in ESCAPE_CHARS:
        string = string.replace(escape_char, '')
    return string


def close_cart_obj(cart_obj):
    if not cart_obj:
        return
    last_status = cart_obj.status
    cart_obj.status = 5
    cart_obj.last_status = last_status
    cart_obj.date_closed = timezone.now()
    cart_obj.save()


def update_transaction_object(order_status_data, txn_obj):
    order_id = txn_obj.order_id
    order_status = order_status_data.get('order_status', '')
    order = Order.objects.get(pk=order_id)
    txn_obj.txn_info = str(order_status_data)

    global SUCCESSFUL_TRANSACTIONS

    if order_status.upper() in ["SUCCESSFUL", "SHIPPED"]:
        txn_obj.status = 1
        SUCCESSFUL_TRANSACTIONS += 1

        close_cart_obj(txn_obj.cart)
        payment_mixin_obj = PaymentMixin()
        request_obj = Request()
        setattr(request_obj, "session", {})

        payment_mixin_obj.process_payment_method(
            payment_type='CCAVENUE', request=request_obj,
            txn_obj=txn_obj,
            data={'order_id': order.pk, 'txn_id': txn_obj.txn})

    elif order_status.upper() == "UNSUCCESSFUL":
        txn_obj.status = 2
        txn_obj.txn_info = order_status_data.get(
            'failure_message', '')

    elif order_status.upper() == "ABORTED":
        txn_obj.status = 3
        txn_obj.txn_info = order_status_data.get(
            'failure_message', '')

    elif order_status.upper() in ["INVALID", "INITIATED"]:
        txn_obj.status = 4
        txn_obj.txn_info = order_status_data.get(
            'failure_message', order_status_data.get('status_message', ''))

    else:
        pass

    txn_obj.save()


if __name__ == "__main__":
    utc_tz = pytz.timezone('UTC')
    current_utc_time = datetime.utcnow().replace(tzinfo=utc_tz)
    time_intervals_to_check = [5, 15, 240, 1440]

    for interval in time_intervals_to_check:
        sdt = (current_utc_time - timedelta(minutes=interval)).replace(tzinfo=utc_tz)
        edt = (sdt + timedelta(minutes=2)).replace(tzinfo=utc_tz)  # Hour + buffer
        all_initiated_transactions = PaymentTxn.objects.filter(status__in=[0, 2, 3, 4, 5],\
                                                               payment_mode__in=[5, 7], created__gte=sdt,
                                                               created__lte=edt, order__site=1)

        logging.getLogger('info_log').info(\
            "Total initiated transactions for interval {} minutes - {}".format(\
                interval, all_initiated_transactions.count()))

        for txn in all_initiated_transactions:
            get_params_mapping = {"command": "orderStatusTracker",
                                  "request_type": "JSON",
                                  "response_type": "JSON",
                                  "access_code": settings.RSHINE_CCAVENUE_ACCESS_CODE,
                                  "order_no": txn.txn
                                  }

            url_get_string = "&".join(["{}={}".format(key, value) for key, value in get_params_mapping.items()])

            obj = CCAvenueCrypto()
            encrypted_data = obj.encrypt(json.dumps(get_params_mapping), settings.RSHINE_CCAVENUE_WORKING_KEY)
            json_data = json.dumps({"encRequest": url_get_string + "&enc_request=" + encrypted_data,\
                                    "order_no": txn.txn})

            request_url = CCAVENUE_API_URL_BASE + "?" + url_get_string + "&enc_request=" + encrypted_data
            response = requests.post(request_url, data=json_data)
            if not response or not response.status_code == 200:
                logging.getLogger('info_log').info(\
                    "CCAvenue Response code failure - {} {}".format(response.status_code, txn.txn))
                continue

            text_response = get_clean_string(response.text)
            ampersand_split_string_parts = text_response.split("&")
            response_dict = {get_clean_string(part.split("=")[0]): get_clean_string(part.split("=")[1])\
                             for part in ampersand_split_string_parts if len(part.split("=")) == 2}

            if not response_dict.get('status') == '0' or not response_dict.get('enc_response'):
                logging.getLogger('info_log').info("CCAvenue Enc response - {} {} {}".format(response.text, response_dict, txn.txn))
                continue
            decrypted_text = get_clean_string(obj.decrypt(response_dict.get('enc_response'),settings.RSHINE_CCAVENUE_WORKING_KEY).strip())
            start_index = 0
            end_index = 0
            try:
                start_index = decrypted_text.find("{")
                end_index = decrypted_text.rfind("}")
                decrypted_text = decrypted_text[start_index:end_index + 1]
                decrypted_dict = ast.literal_eval(decrypted_text)
            except Exception as e:
                decrypted_dict = {}
                logging.getLogger('error_log').error("Unable to decrypt CCAvenue reponse {} {} {}".format(str(e), txn.txn, decrypted_text))

            if not decrypted_dict:
                logging.getLogger('error_log').error("CCAvenue Unable to decrypt {} {}".format(decrypted_dict, txn.txn))
                continue

            order_status_data = decrypted_dict.get('Order_Status_Result')
            logging.getLogger('info_log').info(order_status_data)
            if not order_status_data:
                logging.getLogger('info_log').info("Order Status Failure - {} {}".format(order_status_data, txn.txn))
                continue
            update_transaction_object(order_status_data, txn)

    logging.getLogger('info_log').info("Total successful transactions - {}".format(SUCCESSFUL_TRANSACTIONS))



