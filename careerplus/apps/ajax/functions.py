import logging

from django.conf import settings
from emailers.tasks import send_email_task
from emailers.sms import SendSMS
from order.functions import create_short_url
from microsite.roundoneapi import RoundOneAPI


def draft_upload_mail(oi=None, to_emails=[], mail_type=None, email_dict={}):
    email_sets = list(oi.emailorderitemoperation_set.all().values_list('email_oi_status',flat=True).distinct())
    sms_sets = list(oi.smsorderitemoperation_set.all().values_list('sms_oi_status',flat=True).distinct())
    if oi.product.type_flow == 1:
        if oi.draft_counter == 1 and (22 not in email_sets and 22 not in sms_sets):
            email_dict['subject'] = "Your developed document has been uploaded" 
            send_email_task.delay(to_emails, mail_type, email_dict, status=22, oi=oi.pk)    
            try:
                urlshortener = create_short_url(login_url=email_dict)
                email_dict.update({'url': urlshortener.get('url')})
                SendSMS().send(sms_type=mail_type, data=email_dict)
                oi.smsorderitemoperation_set.create(
                    sms_oi_status=22,
                    to_mobile=email_dict.get('mobile'),
                    status=1)
            except Exception as e:
                logging.getLogger('error_log').error("%s - %s" % (str(mail_type), str(e)))

        elif oi.draft_counter == 2 and (23 not in email_sets and 23 not in sms_sets):
            email_dict['subject'] = "Your developed document is ready"
            send_email_task.delay(to_emails, mail_type, email_dict, status=23, oi=oi.pk)
            try:
                urlshortener = create_short_url(login_url=email_dict)
                email_dict.update({'url': urlshortener.get('url')})
                SendSMS().send(sms_type=mail_type, data=email_dict)
                oi.smsorderitemoperation_set.create(
                    sms_oi_status=23,
                    to_mobile=email_dict.get('mobile'),
                    status=1)
            except Exception as e:
                logging.getLogger('error_log').error("%s - %s" % (str(mail_type), str(e)))

        elif oi.draft_counter == settings.DRAFT_MAX_LIMIT and (24 not in email_sets and 24 not in sms_sets):
            email_dict['subject'] = "Your final document is ready"
            send_email_task.delay(to_emails, mail_type, email_dict, status=24, oi=oi.pk)
            try:
                urlshortener = create_short_url(login_url=email_dict)
                email_dict.update({'url': urlshortener.get('url')})
                SendSMS().send(sms_type=mail_type, data=email_dict)
                oi.smsorderitemoperation_set.create(
                    sms_oi_status=24,
                    to_mobile=email_dict.get('mobile'),
                    status=1)
            except Exception as e:
                logging.getLogger('error_log').error("%s - %s" % (str(mail_type), str(e)))

    elif oi.product.type_flow == 12:
        if oi.draft_counter == 1 and (142 not in email_sets and 142 not in sms_sets):
            email_dict['subject'] = "Your developed document has been uploaded" 
            send_email_task.delay(to_emails, mail_type, email_dict, status=142, oi=oi.pk)
            try:
                urlshortener = create_short_url(login_url=email_dict)
                email_dict.update({'url': urlshortener.get('url')})
                SendSMS().send(sms_type=mail_type, data=email_dict)
                oi.smsorderitemoperation_set.create(
                    sms_oi_status=142,
                    to_mobile=email_dict.get('mobile'),
                    status=1)
            except Exception as e:
                logging.getLogger('error_log').error("%s - %s" % (str(mail_type), str(e)))

        elif oi.draft_counter == 2 and (143 not in email_sets and 143 not in sms_sets):
            email_dict['subject'] = "Your developed document is ready"
            send_email_task.delay(to_emails, mail_type, email_dict, status=143, oi=oi.pk)
            try:
                urlshortener = create_short_url(login_url=email_dict)
                email_dict.update({'url': urlshortener.get('url')})
                SendSMS().send(sms_type=mail_type, data=email_dict)
                oi.smsorderitemoperation_set.create(
                    sms_oi_status=143,
                    to_mobile=email_dict.get('mobile'),
                    status=1)
            except Exception as e:
                logging.getLogger('error_log').error("%s - %s" % (str(mail_type), str(e)))

        elif oi.draft_counter == settings.DRAFT_MAX_LIMIT and (144 not in email_sets and 144 not in sms_sets):
            email_dict['subject'] = "Your final document is ready"
            send_email_task.delay(to_emails, mail_type, email_dict, status=144, oi=oi.pk)
            try:
                urlshortener = create_short_url(login_url=email_dict)
                email_dict.update({'url': urlshortener.get('url')})
                SendSMS().send(sms_type=mail_type, data=email_dict)
                oi.smsorderitemoperation_set.create(
                    sms_oi_status=144,
                    to_mobile=email_dict.get('mobile'),
                    status=1)
            except Exception as e:
                logging.getLogger('error_log').error("%s - %s" % (str(mail_type), str(e)))

    elif oi.product.type_flow == 13:
        if oi.draft_counter == 1 and (152 not in email_sets and 152 not in sms_sets):
            email_dict['subject'] = "Your developed document has been uploaded"
            send_email_task.delay(to_emails, mail_type, email_dict, status=152, oi=oi.pk)
            try:
                urlshortener = create_short_url(login_url=email_dict)
                email_dict.update({'url': urlshortener.get('url')})
                SendSMS().send(sms_type=mail_type, data=email_dict)
                oi.smsorderitemoperation_set.create(
                    sms_oi_status=152,
                    to_mobile=email_dict.get('mobile'),
                    status=1)
            except Exception as e:
                logging.getLogger('error_log').error("%s - %s" % (str(mail_type), str(e)))

        elif oi.draft_counter == 2 and (153 not in email_sets and 153 not in sms_sets):
            email_dict['subject'] = "Your developed document is ready"
            send_email_task.delay(to_emails, mail_type, email_dict, status=153, oi=oi.pk)
            try:
                urlshortener = create_short_url(login_url=email_dict)
                email_dict.update({'url': urlshortener.get('url')})
                SendSMS().send(sms_type=mail_type, data=email_dict)
                oi.smsorderitemoperation_set.create(
                    sms_oi_status=153,
                    to_mobile=email_dict.get('mobile'),
                    status=1)
            except Exception as e:
                logging.getLogger('error_log').error("%s - %s" % (str(mail_type), str(e)))

        elif oi.draft_counter == settings.DRAFT_MAX_LIMIT and (154 not in email_sets and 154 not in sms_sets):
            email_dict['subject'] = "Your final document is ready"
            send_email_task.delay(to_emails, mail_type, email_dict, status=154, oi=oi.pk)
            try:
                urlshortener = create_short_url(login_url=email_dict)
                email_dict.update({'url': urlshortener.get('url')})
                SendSMS().send(sms_type=mail_type, data=email_dict)
                oi.smsorderitemoperation_set.create(
                    sms_oi_status=154,
                    to_mobile=email_dict.get('mobile'),
                    status=1)
            except Exception as e:
                logging.getLogger('error_log').error("%s - %s" % (str(mail_type), str(e)))
    else:
        pass


def roundone_product(order=None):
    try:
        if order.status == 1:
            orderitems = order.orderitems.filter(
                no_process=False,
                product__type_flow=9).select_related(
                'order', 'product', 'partner')
            for oi in orderitems:
                if oi.product.type_flow == 9:
                    last_oi_status = oi.oi_status
                    oi.oi_status = 141
                    oi.last_oi_status = last_oi_status
                    oi.save()
                    oi.orderitemoperation_set.create(
                        oi_status=oi.oi_status,
                        last_oi_status=last_oi_status)
                    RoundOneAPI().create_roundone_order(order)
    except Exception as e:
        logging.getLogger('error_log').error("%s - %s" % (str(order), str(e)))