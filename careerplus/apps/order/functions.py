import logging

from django.utils import timezone
from django.conf import settings

from emailers.email import SendMail
from emailers.tasks import send_email_task
from emailers.sms import SendSMS
from core.mixins import InvoiceGenerate
from payment.models import PaymentTxn
from linkedin.autologin import AutoLogin


def update_initiat_orderitem_sataus(order=None):
    if order:
        orderitems = order.orderitems.filter(no_process=False).select_related('order', 'product', 'partner')

        # update initial status
        for oi in orderitems:
            if oi.product.type_flow in [1, 3, 12, 13]:
                last_oi_status = oi.oi_status
                oi.oi_status = 2
                oi.last_oi_status = last_oi_status
                oi.save()
                oi.orderitemoperation_set.create(
                    oi_status=oi.oi_status,
                    last_oi_status=last_oi_status,
                    assigned_to=oi.assigned_to)

            elif oi.product.type_flow == 2:
                last_oi_status = oi.oi_status
                oi.oi_status = 5
                oi.last_oi_status = last_oi_status
                oi.save()
                oi.orderitemoperation_set.create(
                    oi_status=oi.oi_status,
                    last_oi_status=last_oi_status,
                    assigned_to=oi.assigned_to)

            elif oi.product.type_flow == 4:
                if oi.order.orderitems.filter(product__type_flow=12, no_process=False).exists():
                    last_oi_status = oi.oi_status
                    oi.oi_status = 61
                    oi.last_oi_status = last_oi_status
                    oi.save()
                    oi.orderitemoperation_set.create(
                        oi_status=oi.oi_status,
                        last_oi_status=last_oi_status,
                        assigned_to=oi.assigned_to)
                else:
                    last_oi_status = oi.oi_status
                    oi.oi_status = 2
                    oi.last_oi_status = last_oi_status
                    oi.save()
                    oi.orderitemoperation_set.create(
                        oi_status=oi.oi_status,
                        last_oi_status=last_oi_status,
                        assigned_to=oi.assigned_to)

            elif oi.product.type_flow == 5:
                if oi.order.orderitems.filter(product__type_flow=1, no_process=False).exists():
                    last_oi_status = oi.oi_status
                    oi.oi_status = 61
                    oi.last_oi_status = last_oi_status
                    oi.save()
                    oi.orderitemoperation_set.create(
                        oi_status=oi.oi_status,
                        last_oi_status=last_oi_status,
                        assigned_to=oi.assigned_to)
                else:
                    last_oi_status = oi.oi_status
                    oi.oi_status = 2
                    oi.last_oi_status = last_oi_status
                    oi.save()
                    oi.orderitemoperation_set.create(
                        oi_status=oi.oi_status,
                        last_oi_status=last_oi_status,
                        assigned_to=oi.assigned_to)

            elif oi.product.type_flow == 6:
                last_oi_status = oi.oi_status
                oi.oi_status = 82
                oi.last_oi_status = last_oi_status
                oi.save()
                oi.orderitemoperation_set.create(
                    oi_status=oi.oi_status,
                    last_oi_status=last_oi_status,
                    assigned_to=oi.assigned_to)

            elif oi.product.type_flow == 7:
                depending_ois = order.orderitems.filter(
                    product__type_flow=1, no_process=False)

                if depending_ois.exists():
                    last_oi_status = oi.oi_status
                    oi.oi_status = 61
                    oi.last_oi_status = last_oi_status
                    oi.save()
                    oi.orderitemoperation_set.create(
                        oi_status=oi.oi_status,
                        last_oi_status=last_oi_status,
                        assigned_to=oi.assigned_to)

            # elif oi.product.type_flow == 8:
            #     last_oi_status = oi.oi_status
            #     oi.oi_status = 49
            #     oi.last_oi_status = last_oi_status
            #     oi.save()
            #     oi.orderitemoperation_set.create(
            #         oi_status=oi.oi_status,
            #         last_oi_status=last_oi_status,
            #         assigned_to=oi.assigned_to)

            elif oi.product.type_flow == 10:
                last_oi_status = oi.oi_status
                oi.oi_status = 101
                oi.last_oi_status = last_oi_status
                oi.save()
                oi.orderitemoperation_set.create(
                    oi_status=oi.oi_status,
                    last_oi_status=last_oi_status,
                    assigned_to=oi.assigned_to)


def get_upload_path_order_invoice(instance, filename):
    return "invoice/order/{order_id}/{filename}".format(
        order_id=instance.id, filename=filename)


def pending_item_email(order=None):
    if order.status == 1:
        orderitems = order.orderitems.filter(no_process=False).select_related('order', 'product', 'partner')
        for oi in orderitems:
            data = {}
            mail_type = "PENDING_ITEMS"
            to_emails = [oi.order.email]
            data.update({
                'site': 'http://' + settings.SITE_DOMAIN + settings.STATIC_URL,
                'subject': 'To initiate your service(s) fulfil these pending requirements',
                'username': oi.order.first_name if oi.order.first_name else oi.order.candidate_id,
                'type_flow': oi.product.type_flow,
                'product_name': oi.product.name,
            })
            email_sets = list(oi.emailorderitemoperation_set.all().values_list('email_oi_status',flat=True).distinct())
            try:
                if oi.product.type_flow == 1 and 21 not in email_sets:
                    token = AutoLogin().encode(oi.order.email, oi.order.candidate_id, oi.order.id)
                    data.update({
                        'upload_url': "http://%s/autologin/%s/?next=dashboard" % (settings.SITE_DOMAIN, token.decode())     
                    })

                    return_val = send_email_task.delay(to_emails, mail_type, data)

                    if return_val:
                        oi.emailorderitemoperation_set.create(email_oi_status=21)
                    try:
                        SendSMS().send(sms_type=mail_type, data=data)
                    except Exception as e:
                        logging.getLogger('sms_log').error("%s - %s" % (str(mail_type), str(e)))

                elif oi.product.type_flow == 3 and 41 not in email_sets:
                    token = AutoLogin().encode(oi.order.email, oi.order.candidate_id, oi.order.id)
                    data.update({
                        'upload_url': "http://%s/autologin/%s/?next=dashboard" % (settings.SITE_DOMAIN, token.decode())     
                    })
                    
                    return_val = send_email_task.delay(to_emails, mail_type, data)

                    if return_val:
                        oi.emailorderitemoperation_set.create(email_oi_status=41)
                    try:
                        SendSMS().send(sms_type=mail_type, data=data)
                    except Exception as e:
                        logging.getLogger('sms_log').error("%s - %s" % (str(mail_type), str(e)))

                elif oi.product.type_flow == 4 and 61 not in email_sets:
                    token = AutoLogin().encode(oi.order.email, oi.order.candidate_id, oi.order.id)
                    data.update({
                        'upload_url': "http://%s/autologin/%s/?next=dashboard" % (settings.SITE_DOMAIN, token.decode())     
                    })
                    
                    return_val = send_email_task.delay(to_emails, mail_type, data)

                    if return_val:
                        oi.emailorderitemoperation_set.create(email_oi_status=61)
                    try:
                        SendSMS().send(sms_type=mail_type, data=data)
                    except Exception as e:
                        logging.getLogger('sms_log').error("%s - %s" % (str(mail_type), str(e)))

                elif oi.product.type_flow == 5 and 71 not in email_sets:
                    token = AutoLogin().encode(oi.order.email, oi.order.candidate_id, oi.order.id)
                    data.update({
                        'upload_url': "http://%s/autologin/%s/?next=dashboard" % (settings.SITE_DOMAIN, token.decode())     
                    })
                    
                    return_val = send_email_task.delay(to_emails, mail_type, data)

                    if return_val:
                        oi.emailorderitemoperation_set.create(email_oi_status=71)
                    try:
                        SendSMS().send(sms_type=mail_type, data=data)
                    except Exception as e:
                        logging.getLogger('sms_log').error("%s - %s" % (str(mail_type), str(e)))

                elif oi.product.type_flow == 7 and 91 not in email_sets:
                    token = AutoLogin().encode(oi.order.email, oi.order.candidate_id, oi.order.id)
                    data.update({
                        'upload_url': "http://%s/autologin/%s/?next=dashboard" % (settings.SITE_DOMAIN, token.decode())     
                    })
                    
                    return_val = send_email_task.delay(to_emails, mail_type, data)

                    if return_val:
                        oi.emailorderitemoperation_set.create(email_oi_status=91)
                    try:
                        SendSMS().send(sms_type=mail_type, data=data)
                    except Exception as e:
                        logging.getLogger('sms_log').error("%s - %s" % (str(mail_type), str(e)))

                elif oi.product.type_flow == 12 and 141 not in email_sets:
                    token = AutoLogin().encode(oi.order.email, oi.order.candidate_id, oi.order.id)
                    data.update({
                        'upload_url': "http://%s/autologin/%s/?next=dashboard" % (settings.SITE_DOMAIN, token.decode())     
                    })
                    
                    return_val = send_email_task.delay(to_emails, mail_type, data)

                    if return_val:
                        oi.emailorderitemoperation_set.create(email_oi_status=141)
                    try:
                        SendSMS().send(sms_type=mail_type, data=data)
                    except Exception as e:
                        logging.getLogger('sms_log').error("%s - %s" % (str(mail_type), str(e)))

                elif oi.product.type_flow == 13 and 151 not in email_sets:
                    token = AutoLogin().encode(oi.order.email, oi.order.candidate_id, oi.order.id)
                    data.update({
                        'upload_url': "http://%s/autologin/%s/?next=dashboard" % (settings.SITE_DOMAIN, token.decode())     
                    })
                    
                    return_val = send_email_task.delay(to_emails, mail_type, data)

                    if return_val:
                        oi.emailorderitemoperation_set.create(email_oi_status=151)
                    try:
                        SendSMS().send(sms_type=mail_type, data=data)
                    except Exception as e:
                        logging.getLogger('sms_log').error("%s - %s" % (str(mail_type), str(e)))

                elif oi.product.type_flow == 8 and 108 not in email_sets:
                    data.update({
                        'counselling_form': "http://%s/linkedin/counsellingform/%s" % (settings.SITE_DOMAIN, oi.pk) 
                    })
                    return_val = send_email_task.delay(to_emails, mail_type, data)
                    if return_val:
                        oi.emailorderitemoperation_set.create(email_oi_status=151)

                    try:
                        SendSMS().send(sms_type=mail_type, data=data)
                    except Exception as e:
                        logging.getLogger('sms_log').error("%s - %s" % (str(mail_type), str(e)))

                elif oi.product.type_flow == 9 and 121 not in email_sets:
                    data.update({
                        'complete_profile': "http://%s/dashboard/roundone/profile/" % (settings.SITE_DOMAIN) 
                    })

                    return_val = send_email_task.delay(to_emails, mail_type, data)
                    if return_val:
                        oi.emailorderitemoperation_set.create(email_oi_status=151)

                    try:
                        SendSMS().send(sms_type=mail_type, data=data)
                    except Exception as e:
                        logging.getLogger('sms_log').error("%s - %s" % (str(mail_type), str(e)))

                elif oi.product.type_flow == 10 and 131 not in email_sets:
                    data.update({
                        'test_url': "http://%s/dashboard" % (settings.SITE_DOMAIN) 
                    })

                    return_val = send_email_task.delay(to_emails, mail_type, data)
                    if return_val:
                        oi.emailorderitemoperation_set.create(email_oi_status=151)

                    try:
                        SendSMS().send(sms_type=mail_type, data=data)
                    except Exception as e:
                        logging.getLogger('sms_log').error("%s - %s" % (str(mail_type), str(e)))

            except Exception as e:
                raise e


def process_mailer(order=None):
    if order.status == 1:
        orderitems = order.orderitems.filter(no_process=False).select_related('order', 'product', 'partner')
        for oi in orderitems:
            try:
                email_sets = list(oi.emailorderitemoperation_set.all().values_list('email_oi_status',flat=True).distinct())
                to_emails = [oi.order.email]
                mail_type = "PROCESS_MAILERS"
                data = {}
                data.update({
                    'subject': 'Your service details related to order <'+str(oi.order.id)+'>',
                    'username': oi.order.first_name if oi.order.first_name else oi.order.candidate_id,
                    'oi': oi,
                    'pk': oi.pk,
                    'email': oi.order.email,
                    'candidateid': oi.order.email,
                    'site': 'http://' + settings.SITE_DOMAIN + settings.STATIC_URL
                })

                if 2 not in email_sets:
                    return_val = send_email_task.delay(to_emails, mail_type, data)
                    if return_val:
                        oi.emailorderitemoperation_set.create(email_oi_status=2)
            except Exception as e:
                raise e


def payment_pending_mailer(order=None):
    try:
        pymt_objs = PaymentTxn.objects.filter(order=order, payment_mode__in=[1,4])
        if pymt_objs.exists():
            orderitems = order.orderitems.filter(no_process=False).select_related('order', 'product', 'partner')

            for oi in orderitems:
                email_sets = list(oi.emailorderitemoperation_set.all().values_list('email_oi_status',flat=True).distinct())
                if 1 not in email_sets:
                    to_emails = [order.email]
                    mail_type = "PAYMENT_PENDING"
                    data = {}
                    data.update({
                        "subject": 'Your Shine Payment Confirmation pending',
                        "first_name": order.first_name if order.first_name else order.candidate_id,
                        "txn": pymt_obj.txn,
                        'site': 'http://' + settings.SITE_DOMAIN + settings.STATIC_URL,
                    })
                    return_val = send_email_task.delay(to_emails, mail_type, data)
                    if return_val:
                        oi.emailorderitemoperation_set.create(email_oi_status=1)
    except Exception as e:
        raise e

def payment_realisation_mailer(order=None):
    try:
        invoice_data = InvoiceGenerate().get_invoice_data(order=order)
        pymt_objs = PaymentTxn.objects.filter(order=order)
        for pymt_obj in pymt_objs:
            if pymt_obj.status == 1:
                to_emails = [order.email]
                mail_type = "SHINE_PAYMENT_CONFIRMATION"
                invoice_data.update({
                    'subject': 'Your Shine Payment Confirmation',
                    "first_name": order.first_name if order.first_name else order.candidate_id,
                    "txn": pymt_obj.txn,
                    "order_id": order.id,
                    'site': 'http://' + settings.SITE_DOMAIN + settings.STATIC_URL,
                })
                try:
                    SendMail().send(to_emails, mail_type, invoice_data)
                except Exception as e:
                    logging.getLogger('email_log').error("payment pending %s - %s - %s" % (str(to_emails), str(mail_type), str(e)))
    except Exception as e:
        raise e
  