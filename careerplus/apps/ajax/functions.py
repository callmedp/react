import logging

from django.utils import timezone
from django.conf import settings
from emailers.tasks import send_email_task

def draft_upload_mail(oi=None, to_emails=[], mail_type=None, data={}):
    email_sets = list(oi.emailorderitemoperation_set.all().values_list('email_oi_status',flat=True).distinct())
    if obj.product.type_flow == 1 :
        if obj.draft_counter == 1 and 22 not in email_sets:
            email_dict['subject'] = "Your developed document has been uploaded" 
            return_val = send_email_task.delay(to_emails, mail_type, email_dict)
            if return_val.result:
                obj.emailorderitemoperation_set.create(email_oi_status=63)
            try:
                SendSMS().send(sms_type=mail_type, data=email_dict)
            except Exception as e:
                logging.getLogger('sms_log').error("%s - %s" % (str(mail_type), str(e)))

        elif obj.draft_counter == 2 and 23 not in email_sets:
            email_dict['subject'] = "Your developed document is ready"
            return_val = send_email_task.delay(to_emails, mail_type, email_dict)
            if return_val.result:
                obj.emailorderitemoperation_set.create(email_oi_status=23)
            try:
                SendSMS().send(sms_type=mail_type, data=email_dict)
            except Exception as e:
                logging.getLogger('sms_log').error("%s - %s" % (str(mail_type), str(e)))

        elif obj.draft_counter == settings.DRAFT_MAX_LIMIT and 24 not in email_sets :
            email_dict['subject'] = "Your final document is ready"
            return_val = send_email_task.delay(to_emails, mail_type, email_dict)
            if return_val.result:
                obj.emailorderitemoperation_set.create(email_oi_status=24)
            try:
                SendSMS().send(sms_type=mail_type, data=email_dict)
            except Exception as e:
                logging.getLogger('sms_log').error("%s - %s" % (str(mail_type), str(e)))

    elif obj.product.type_flow == 12 :
        if obj.draft_counter == 1 and 142 not in email_sets:
            email_dict['subject'] = "Your developed document has been uploaded" 
            return_val = send_email_task.delay(to_emails, mail_type, email_dict)
            if return_val.result:
                obj.emailorderitemoperation_set.create(email_oi_status=142)
            try:
                SendSMS().send(sms_type=mail_type, data=email_dict)
            except Exception as e:
                logging.getLogger('sms_log').error("%s - %s" % (str(mail_type), str(e)))

        elif obj.draft_counter == 2 and 143 not in email_sets:
            email_dict['subject'] = "Your developed document is ready"
            return_val = send_email_task.delay(to_emails, mail_type, email_dict)
            if return_val.result:
                obj.emailorderitemoperation_set.create(email_oi_status=143)
            try:
                SendSMS().send(sms_type=mail_type, data=email_dict)
            except Exception as e:
                logging.getLogger('sms_log').error("%s - %s" % (str(mail_type), str(e)))

        elif obj.draft_counter == settings.DRAFT_MAX_LIMIT and 144 not in email_sets :
            email_dict['subject'] = "Your final document is ready"
            return_val = send_email_task.delay(to_emails, mail_type, email_dict)
            if return_val.result:
                obj.emailorderitemoperation_set.create(email_oi_status=144)
            try:
                SendSMS().send(sms_type=mail_type, data=email_dict)
            except Exception as e:
                logging.getLogger('sms_log').error("%s - %s" % (str(mail_type), str(e)))

    elif obj.product.type_flow == 13 :
        if obj.draft_counter == 1 and 152 not in email_sets:
            email_dict['subject'] = "Your developed document has been uploaded" 
            return_val = send_email_task.delay(to_emails, mail_type, email_dict)
            if return_val.result:
                obj.emailorderitemoperation_set.create(email_oi_status=152)
            try:
                SendSMS().send(sms_type=mail_type, data=email_dict)
            except Exception as e:
                logging.getLogger('sms_log').error("%s - %s" % (str(mail_type), str(e)))

        elif obj.draft_counter == 2 and 153 not in email_sets:
            email_dict['subject'] = "Your developed document is ready"
            return_val = send_email_task.delay(to_emails, mail_type, email_dict)
            if return_val.result:
                obj.emailorderitemoperation_set.create(email_oi_status=153)
            try:
                SendSMS().send(sms_type=mail_type, data=email_dict)
            except Exception as e:
                logging.getLogger('sms_log').error("%s - %s" % (str(mail_type), str(e)))

        elif obj.draft_counter == settings.DRAFT_MAX_LIMIT and 154 not in email_sets :
            email_dict['subject'] = "Your final document is ready"
            return_val = send_email_task.delay(to_emails, mail_type, email_dict)
            if return_val.result:
                obj.emailorderitemoperation_set.create(email_oi_status=154)
            try:
                SendSMS().send(sms_type=mail_type, data=email_dict)
            except Exception as e:
                logging.getLogger('sms_log').error("%s - %s" % (str(mail_type), str(e)))
    else:
        pass