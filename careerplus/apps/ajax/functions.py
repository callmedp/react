import logging

from django.utils import timezone
from django.conf import settings
from emailers.tasks import send_email_task
from order.functions import create_short_url

def draft_upload_mail(oi=None, to_emails=[], mail_type=None, email_dict={}):
    email_sets = list(oi.emailorderitemoperation_set.all().values_list('email_oi_status',flat=True).distinct())
    sms_sets = list(oi.emailorderitemoperation_set.all().values_list('sms_oi_status',flat=True).distinct())
    if oi.product.type_flow == 1 :
        if oi.draft_counter == 1 and (22 not in email_sets and 22 not in sms_sets):
            email_dict['subject'] = "Your developed document has been uploaded" 
            return_val = send_email_task.delay(to_emails, mail_type, email_dict)
            if return_val.result:
                oi.emailorderitemoperation_set.create(email_oi_status=22)
                
            try:
                urlshortener = create_short_url(login_url=email_dict)
                email_dict.update({'url': urlshortener.get('url')})
                SendSMS().send(sms_type=mail_type, data=email_dict)
                oi.smsorderitemoperation_set.create(sms_oi_status=22)
            except Exception as e:
                logging.getLogger('sms_log').error("%s - %s" % (str(mail_type), str(e)))

        elif oi.draft_counter == 2 and (23 not in email_sets and 23 not in sms_sets):
            email_dict['subject'] = "Your developed document is ready"
            return_val = send_email_task.delay(to_emails, mail_type, email_dict)
            if return_val.result:
                oi.emailorderitemoperation_set.create(email_oi_status=23)
            try:
                urlshortener = create_short_url(login_url=email_dict)
                email_dict.update({'url': urlshortener.get('url')})
                SendSMS().send(sms_type=mail_type, data=email_dict)
                oi.emailorderitemoperation_set.create(email_oi_status=23)
            except Exception as e:
                logging.getLogger('sms_log').error("%s - %s" % (str(mail_type), str(e)))

        elif oi.draft_counter == settings.DRAFT_MAX_LIMIT and (24 not in email_sets and 24 not in sms_sets):
            email_dict['subject'] = "Your final document is ready"
            return_val = send_email_task.delay(to_emails, mail_type, email_dict)
            if return_val.result:
                oi.emailorderitemoperation_set.create(email_oi_status=24)
            try:
                urlshortener = create_short_url(login_url=email_dict)
                email_dict.update({'url': urlshortener.get('url')})
                SendSMS().send(sms_type=mail_type, data=email_dict)
                oi.smsorderitemoperation_set.create(email_oi_status=24)
            except Exception as e:
                logging.getLogger('sms_log').error("%s - %s" % (str(mail_type), str(e)))

    elif oi.product.type_flow == 12 :
        if oi.draft_counter == 1 and (142 not in email_sets and 142 not in sms_sets):
            email_dict['subject'] = "Your developed document has been uploaded" 
            return_val = send_email_task.delay(to_emails, mail_type, email_dict)
            if return_val.result:
                oi.emailorderitemoperation_set.create(email_oi_status=142)
            try:
                urlshortener = create_short_url(login_url=email_dict)
                email_dict.update({'url': urlshortener.get('url')})
                SendSMS().send(sms_type=mail_type, data=email_dict)
                oi.smsorderitemoperation_set.create(sms_oi_status=142)
            except Exception as e:
                logging.getLogger('sms_log').error("%s - %s" % (str(mail_type), str(e)))

        elif oi.draft_counter == 2 and (143 not in email_sets and 143 not in sms_sets):
            email_dict['subject'] = "Your developed document is ready"
            return_val = send_email_task.delay(to_emails, mail_type, email_dict)
            if return_val.result:
                oi.emailorderitemoperation_set.create(email_oi_status=143)
            try:
                urlshortener = create_short_url(login_url=email_dict)
                email_dict.update({'url': urlshortener.get('url')})
                SendSMS().send(sms_type=mail_type, data=email_dict)
                oi.emailorderitemoperation_set.create(sms_oi_status=143)
            except Exception as e:
                logging.getLogger('sms_log').error("%s - %s" % (str(mail_type), str(e)))

        elif oi.draft_counter == settings.DRAFT_MAX_LIMIT and (144 not in email_sets and 144 not in sms_sets):
            email_dict['subject'] = "Your final document is ready"
            return_val = send_email_task.delay(to_emails, mail_type, email_dict)
            if return_val.result:
                oi.emailorderitemoperation_set.create(email_oi_status=144)
            try:
                urlshortener = create_short_url(login_url=email_dict)
                email_dict.update({'url': urlshortener.get('url')})
                SendSMS().send(sms_type=mail_type, data=email_dict)
                oi.smsorderitemoperation_set.create(sms_oi_status=144)
            except Exception as e:
                logging.getLogger('sms_log').error("%s - %s" % (str(mail_type), str(e)))

    elif oi.product.type_flow == 13 :
        if oi.draft_counter == 1 and (152 not in email_sets and 152 not in sms_sets):
            email_dict['subject'] = "Your developed document has been uploaded" 
            return_val = send_email_task.delay(to_emails, mail_type, email_dict)
            if return_val.result:
                oi.emailorderitemoperation_set.create(email_oi_status=152)
            try:
                urlshortener = create_short_url(login_url=email_dict)
                email_dict.update({'url': urlshortener.get('url')})
                SendSMS().send(sms_type=mail_type, data=email_dict)
                oi.smsorderitemoperation_set.create(sms_oi_status=152)
            except Exception as e:
                logging.getLogger('sms_log').error("%s - %s" % (str(mail_type), str(e)))

        elif oi.draft_counter == 2 and (153 not in email_sets and 153 not in sms_sets):
            email_dict['subject'] = "Your developed document is ready"
            return_val = send_email_task.delay(to_emails, mail_type, email_dict)
            if return_val.result:
                oi.emailorderitemoperation_set.create(email_oi_status=153)
            try:
                urlshortener = create_short_url(login_url=email_dict)
                email_dict.update({'url': urlshortener.get('url')})
                SendSMS().send(sms_type=mail_type, data=email_dict)
                oi.smsorderitemoperation_set.create(sms_oi_status=153)
            except Exception as e:
                logging.getLogger('sms_log').error("%s - %s" % (str(mail_type), str(e)))

        elif oi.draft_counter == settings.DRAFT_MAX_LIMIT and (154 not in email_sets and 154 not in sms_sets):
            email_dict['subject'] = "Your final document is ready"
            return_val = send_email_task.delay(to_emails, mail_type, email_dict)
            if return_val.result:
                oi.emailorderitemoperation_set.create(email_oi_status=154)
            try:
                urlshortener = create_short_url(login_url=email_dict)
                email_dict.update({'url': urlshortener.get('url')})
                SendSMS().send(sms_type=mail_type, data=email_dict)
                oi.smsorderitemoperation_set.create(sms_oi_status=154)
            except Exception as e:
                logging.getLogger('sms_log').error("%s - %s" % (str(mail_type), str(e)))
    else:
        pass