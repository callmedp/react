import logging

from django.utils import timezone
from django.conf import settings

from emailers.email import SendMail
from emailers.sms import SendSMS
from core.mixins import InvoiceGenerate
from payment.models import PaymentTxn

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

            elif oi.product.type_flow == 8:
                last_oi_status = oi.oi_status
                oi.oi_status = 49
                oi.last_oi_status = last_oi_status
                oi.save()
                oi.orderitemoperation_set.create(
                    oi_status=oi.oi_status,
                    last_oi_status=last_oi_status,
                    assigned_to=oi.assigned_to)

            elif oi.product.type_flow == 10:
                last_oi_status = oi.oi_status
                oi.oi_status = 101
                oi.last_oi_status = last_oi_status
                oi.save()
                oi.orderitemoperation_set.create(
                    oi_status=oi.oi_status,
                    last_oi_status=last_oi_status,
                    assigned_to=oi.assigned_to)

        linkedin_item = orderitems.filter(product__type_flow=8)
        # pending item email send
        # pending_item_email(order=order)

        # send email through process mailers
        # process_mailer(order=order)

        if linkedin_item.exists():
            try:
                obj_oi_linkedin = linkedin_item[o]
                if obj_oi_linkedin.oi_status == 'Couselling form is pending':
                    to_emails = [order.email]
                    mail_type = "Pending Items"
                    data = {}
                    data.update({
                        "subject": 'To initiate your service(s) fulfil these pending requirements',
                        "username": order.first_name if order.first_name else order.candidate_id,
                        'order_item': obj_oi_linkedin.pk,
                        'candidateid': order.candidate_id,
                    })
                    try:
                        SendMail().send(to_emails, mail_type, data)
                    except Exception as e:
                        logging.getLogger('email_log').error("reminder cron %s - %s - %s" % (str(to_emails), str(mail_type), str(e)))

                    try:
                        SendSMS().send(sms_type=mail_type, data=data)
                    except Exception as e:
                        logging.getLogger('sms_log').error("%s - %s" % (str(mail_type), str(e)))
            except:
                pass


def get_upload_path_order_invoice(instance, filename):
    return "invoice/order/{order_id}/{filename}".format(
        order_id=instance.id, filename=filename)


def pending_item_email(order=None):
    if order.status == 1:
        orderitems = order.orderitems.filter(no_process=False).select_related('order', 'product', 'partner')
        for oi in orderitems:
            try:
                if oi.product.type_flow in [1, 3, 4, 5, 12, 13]:
                    to_emails = [oi.order.email]
                    mail_type = "PENDING_ITEMS"
                    data = {}
                    data.update({
                        'subject': 'To initiate your services fulfil these details',
                        'username': oi.order.first_name if oi.order.first_name else oi.order.candidate_id,
                        'type_flow': oi.product.type_flow,
                        'product_name': oi.product.name,
                        'upload_url': "http://%s/dashboard" % (settings.SITE_DOMAIN) 
                    })
                    try:
                        SendMail().send(to_emails, mail_type, data)
                        order.midout_sent_on = timezone.now()
                        order.save()
                    except Exception as e:
                        logging.getLogger('email_log').error("pending items %s - %s - %s" % (str(to_emails), str(mail_type), str(e)))
                if oi.product.type_flow == 8:
                    to_emails = [oi.order.email]
                    mail_type = "PENDING_ITEMS"
                    data = {}
                    data.update({
                        'subject': 'To initiate your services fulfil these details',
                        'username': oi.order.first_name if oi.order.first_name else oi.order.candidate_id,
                        'type_flow': oi.product.type_flow,
                        'counselling_form': "http://%s/linkedin/counsellingform/%s" % (settings.SITE_DOMAIN, oi.pk) 
                    })
                    try:
                        SendMail().send(to_emails, mail_type, data)
                    except Exception as e:
                        logging.getLogger('email_log').error("pending items %s - %s - %s" % (str(to_emails), str(mail_type), str(e)))
                if oi.product.type_flow == 9:
                    to_emails = [oi.order.email]
                    mail_type = "PENDING_ITEMS"
                    data = {}
                    data.update({
                        'subject': 'To initiate your services fulfil these details',
                        'username': oi.order.first_name if oi.order.first_name else oi.order.candidate_id,
                        'type_flow': oi.product.type_flow,
                        'complete_profile': "http://%s/dashboard/roundone/profile/" % (settings.SITE_DOMAIN) 
                    })
                    try:
                        SendMail().send(to_emails, mail_type, data)
                    except Exception as e:
                        logging.getLogger('email_log').error("pending items %s - %s - %s" % (str(to_emails), str(mail_type), str(e)))

                if oi.product.type_flow == 10:
                    to_emails = [oi.order.email]
                    mail_type = "PENDING_ITEMS"
                    data = {}
                    data.update({
                        'subject': 'To initiate your services fulfil these details',
                        'username': oi.order.first_name if oi.order.first_name else oi.order.candidate_id,
                        'type_flow': oi.product.type_flow,
                        'test_url': "http://%s/dashboard" % (settings.SITE_DOMAIN) 
                    })
                    try:
                        SendMail().send(to_emails, mail_type, data)
                    except Exception as e:
                        logging.getLogger('email_log').error("pending items %s - %s - %s" % (str(to_emails), str(mail_type), str(e)))

            except Exception as e:
                raise e


def process_mailer(order=None):
    if order.status == 1:
        orderitems = order.orderitems.filter(no_process=False).select_related('order', 'product', 'partner')
        for oi in orderitems:
            try:
                to_emails = [oi.order.email]
                mail_type = "PROCESS_MAILERS"
                data = {}
                data.update({
                    'subject': 'Your service details related to order <'+oi.id+'>',
                    'username': oi.order.first_name if oi.order.first_name else oi.order.candidate_id,
                    'type_flow': oi.product.type_flow,
                    'partner': oi.product.vender.name,
                    'pk': oi.pk,
                })
                try:
                    SendMail().send(to_emails, mail_type, data)
                except Exception as e:
                    logging.getLogger('email_log').error("process mailers %s - %s - %s" % (str(to_emails), str(mail_type), str(e)))
            except Exception as e:
                raise e


def payment_pending_mailer(order=None):
    try:
        pymt_objs = PaymentTxn.objects.filter(order=order)
        for pymt_obj in pymt_objs:
            if pymt_obj.payment_mode in [1, 4]:
                to_emails = [order.email]
                mail_type = "PAYMENT_PENDING"
                data = {}
                data.update({
                    "subject": 'Your Shine Payment Confirmation pending',
                    "first_name": order.first_name if order.first_name else order.candidate_id,
                    "txn": pymt_obj.txn,
                    'site': 'http://' + settings.SITE_DOMAIN + settings.STATIC_URL,
                })
                try:
                    SendMail().send(to_emails, mail_type, data)
                except Exception as e:
                    logging.getLogger('email_log').error("payment pending %s - %s - %s" % (str(to_emails), str(mail_type), str(e)))

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
  