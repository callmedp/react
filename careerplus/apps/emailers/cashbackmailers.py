import logging
from django.conf import settings

from datetime import datetime, timedelta, date

from .sms import SendSMS
from .email import SendMail
from emailers import mailers_config

from wallet.models import WalletTransaction, Wallet
from core.common import CampaignUrl

from order.models import Order

TODAY = date.today()

DATEBACK_THREE = TODAY + timedelta(days=-3)
DATEBACK_THREE_START = datetime(DATEBACK_THREE.year, DATEBACK_THREE.month,
                                DATEBACK_THREE.day, 0, 0, 0)
DATEBACK_THREE_END = datetime(DATEBACK_THREE.year, DATEBACK_THREE.month,
                              DATEBACK_THREE.day, 23, 59, 59)

DATEFWD_THREE = TODAY + timedelta(days=3)
DATEFWD_THREE_START = datetime(DATEFWD_THREE.year, DATEFWD_THREE.month,
                               DATEFWD_THREE.day, 0, 0, 0)
DATEFWD_THREE_END = datetime(DATEFWD_THREE.year, DATEFWD_THREE.month,
                             DATEFWD_THREE.day, 23, 59, 59)

DATE_TODAY_START = datetime(TODAY.year, TODAY.month,
                            TODAY.day, 0, 0, 0)
DATE_TODAY_END = datetime(TODAY.year, TODAY.month,
                          TODAY.day, 23, 59, 59)


def get_eligible_orders():
    try:
        email_sent = []
        wallet_tran = WalletTransaction.objects.filter(
            txn_type=1, status=1,
            created_on__range=[DATEBACK_THREE_START, DATEBACK_THREE_END])

        for wallet_tran_obj in wallet_tran:
            wallet_details = wallet_tran_obj.get_cashback_details()
            wallet_details['mailer_type'] = 2
            try:
                order = Order.objects.get(id=wallet_details.get('order_id'))
                email = order.candidate.email
                mobile = order.get_mobile()
            except Exception as e:
                logging.getLogger('error_log').error('unable to fetch order object/object-deails %s'%str(e))
                # user_info = wallet_tran_obj.get_user_info()
                # email = user_info.get('email', '')
                # mobile = user_info.get('mobile', '')

            if len(email) > 0 and len(mobile) > 0:
                if email not in email_sent:
                    # wallet_details.update(CampaignUrl().generate(
                    #     data={'email': email, 'mobile': mobile,
                    #           'x_mailertag': 'cashback_3days'}))

                    wallet_details['SITE_DOMAIN_EMAIL'] =\
                        settings.MAIN_DOMAIN_PREFIX

                    wallet_details['STATIC_MEDIA_URL'] =\
                        settings.MEDIA_URL

                    wallet_details['STATIC_JS_URL'] =\
                        settings.STATIC_JS_URL

                    wallet_details['STATIC_CSS_URL'] =\
                        settings.STATIC_CSS_URL

                    try:
                        SendMail().send(mail_type='CASHBACK_MAILER',
                                        to=[email], data=wallet_details)
                        SendSMS().send(
                            sms_type=mailers_config.SMS_TYPE[6],
                            data={'mobile': mobile,
                                  'name': wallet_details.get('name', ''),
                                  'total_credits':
                                  wallet_details.get('total_credits', ''),
                                  'sms_type': 2})

                        email_sent.append(email)
                    except Exception as e:
                        logging.getLogger('error_log').error(
                            "OrderID#%s - %s" % (str(order.pk), str(e)))
            else:
                logging.getLogger('error_log').error("%s-%s" % (
                    str(wallet_tran_obj.id), "email and mobile not fetched"))
    except Exception as e:
        logging.getLogger('error_log').error('unable to get eligible order details %s'%str(e))


def get_eligible_orders_3lastdays():

    try:
        email_sent = []
        wallet_details = {}

        wallet = Wallet.objects.filter(
            amount__gt=0,
            expiring_on__range=[DATEFWD_THREE_START, DATEFWD_THREE_END])

        for wallet_obj in wallet:
            wallet_details['mailer_type'] = 3
            wallet_details.update(wallet_obj.get_wallet_details())

            email = wallet_obj.user.email
            mobile = wallet_obj.user.email if wallet_obj.user.email else ''

            if len(email) > 0 and len(mobile) > 0:
                if email not in email_sent:
                    wallet_details.update(CampaignUrl().generate(
                        data={'email': email, 'mobile': mobile,
                              'x_mailertag': 'cashback_3lastdays'}))

                    wallet_details['SITE_DOMAIN_EMAIL'] =\
                        settings.SITE_DOMAIN_EMAIL

                    wallet_details['STATIC_MEDIA_URL'] =\
                        settings.STATIC_MEDIA_URL
                    wallet_details['STATIC_JS_URL'] =\
                        settings.STATIC_JS_URL

                    wallet_details['STATIC_CSS_URL'] =\
                        settings.STATIC_CSS_URL

                    try:
                        SendMail().send(
                            mail_type=mailers_config.MAIL_TYPE[10],
                            to=[email], data=wallet_details)
                        SendSMS().send(
                            sms_type=mailers_config.SMS_TYPE[6],
                            data={'mobile': str(mobile),
                                  'name': wallet_details.get('name', ''),
                                  'total_credits':
                                  wallet_details.get('total_credits', ''),
                                  'sms_type': 3})

                        email_sent.append(email)
                    except Exception as e:
                        logging.getLogger('error_log').error(
                            "Wallet ID#%s - %s" % (str(wallet_obj.pk), str(e)))
            else:
                logging.getLogger('error_log').error("%s-%s" % (
                    str(wallet_obj.id), "email and mobile not fetched"))
    except Exception as e:
        logging.getLogger('error_log').error('unable to get eligible orders for last 3 days%s'%str(e))


def get_eligible_orders_lastdays():
    try:
        email_sent = []
        wallet_details = {}

        wallet = Wallet.objects.filter(
            amount__gt=0,
            expiring_on__range=[DATE_TODAY_START, DATE_TODAY_END])

        for wallet_obj in wallet:
            wallet_details['mailer_type'] = 4
            wallet_details.update(wallet_obj.get_wallet_details())

            email = wallet_obj.user.email
            mobile = wallet_obj.user.email if wallet_obj.user.email else ''

            if len(email) > 0 and len(mobile) > 0:
                if email not in email_sent:
                    wallet_details.update(CampaignUrl().generate(
                        data={'email': email, 'mobile': mobile,
                              'x_mailertag': 'cashback_3lastdays'}))

                    wallet_details['SITE_DOMAIN_EMAIL'] =\
                        settings.SITE_DOMAIN_EMAIL

                    wallet_details['STATIC_MEDIA_URL'] =\
                        settings.STATIC_MEDIA_URL

                    wallet_details['STATIC_JS_URL'] =\
                        settings.STATIC_JS_URL

                    wallet_details['STATIC_CSS_URL'] =\
                        settings.STATIC_CSS_URL

                    try:
                        SendMail().send(
                            mail_type=mailers_config.MAIL_TYPE[10],
                            to=[email], data=wallet_details)
                        SendSMS().send(
                            sms_type=mailers_config.SMS_TYPE[6],
                            data={'mobile': str(mobile),
                                  'name': wallet_details.get('name', ''),
                                  'total_credits':
                                  wallet_details.get('total_credits', ''),
                                  'sms_type': 4})

                        email_sent.append(email)
                    except Exception as e:
                        logging.getLogger('error_log').error(
                            "Wallet ID#%s - %s" % (str(wallet_obj.pk), str(e)))
            else:
                logging.getLogger('error_log').error("%s-%s" % (
                    str(wallet_obj.id), "email and mobile not fetched"))
    except Exception as e:
        logging.getLogger('error_log').error('unable to get eligible order details for last days%s'%str(e))
