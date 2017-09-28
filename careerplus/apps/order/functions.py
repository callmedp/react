import logging
import json
import requests

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
    if order:
        orderitems = order.orderitems.filter(no_process=False).select_related('order', 'product', 'partner')
        for oi in orderitems:
            data = {}
            mail_type = "PENDING_ITEMS"
            to_emails = [oi.order.email]
            token = AutoLogin().encode(oi.order.email, oi.order.candidate_id, days=None)
            data.update({
                'subject': 'To initiate your service(s) fulfil these pending requirements',
                'username': oi.order.first_name if oi.order.first_name else oi.order.candidate_id,
                'type_flow': oi.product.type_flow,
                'product_name': oi.product.name,
                'mobile': oi.order.mobile,
            })
            email_sets = list(oi.emailorderitemoperation_set.all().values_list('email_oi_status',flat=True).distinct())
            sms_sets = list(oi.smsorderitemoperation_set.all().values_list('sms_oi_status',flat=True).distinct())
            try:
                if oi.product.type_flow == 1:
                    if 21 not in email_sets and 21 not in sms_sets:
                        data.update({
                            'upload_url': "%s://%s/autologin/%s/?next=dashboard" % (settings.SITE_PROTOCOL, settings.SITE_DOMAIN, token.decode())     
                        })
                        send_email_task.apply_async((to_emails, mail_type, data, 21, oi.pk), countdown=900)
                        try:
                            urlshortener = create_short_url(login_url=data)
                            data.update({'url': urlshortener.get('url')})
                            SendSMS().send(sms_type=mail_type, data=data)
                            oi.smsorderitemoperation_set.create(sms_oi_status=21)
                        except Exception as e:
                            logging.getLogger('sms_log').error("%s - %s" % (str(mail_type), str(e)))

                elif oi.product.type_flow == 3:
                    data.update({
                        'upload_url': "%s://%s/autologin/%s/?next=dashboard" % (settings.SITE_PROTOCOL, settings.SITE_DOMAIN, token.decode())     
                    })
                    if 41 not in email_sets and 41 not in sms_sets:
                        send_email_task.apply_async((to_emails, mail_type, data, 41, oi.pk), countdown=900)
                        try:
                            urlshortener = create_short_url(login_url=data)
                            data.update({'url': urlshortener.get('url')})
                            SendSMS().send(sms_type=mail_type, data=data)
                            oi.smsorderitemoperation_set.create(sms_oi_status=41)
                        except Exception as e:
                            logging.getLogger('sms_log').error("%s - %s" % (str(mail_type), str(e)))

                elif oi.product.type_flow == 4:
                    data.update({
                        'upload_url': "%s://%s/autologin/%s/?next=dashboard" % (settings.SITE_PROTOCOL, settings.SITE_DOMAIN, token.decode())     
                    })
                    if 61 not in email_sets and 61 not in sms_sets:
                        send_email_task.apply_async((to_emails, mail_type, data, 61, oi.pk), countdown=900)
                        try:
                            urlshortener = create_short_url(login_url=data)
                            data.update({'url': urlshortener.get('url')})
                            SendSMS().send(sms_type=mail_type, data=data)
                            oi.smsorderitemoperation_set.create(sms_oi_status=61)
                        except Exception as e:
                            logging.getLogger('sms_log').error("%s - %s" % (str(mail_type), str(e)))

                elif oi.product.type_flow == 5:
                    data.update({
                        'upload_url': "%s://%s/autologin/%s/?next=dashboard" % (settings.SITE_PROTOCOL, settings.SITE_DOMAIN, token.decode())     
                    })
                    if 71 not in email_sets and 71 not in sms_sets:
                        send_email_task.apply_async((to_emails, mail_type, data, 71, oi.pk), countdown=900)
                        try:
                            urlshortener = create_short_url(login_url=data)
                            data.update({'url': urlshortener.get('url')})
                            SendSMS().send(sms_type=mail_type, data=data)
                            oi.smsorderitemoperation_set.create(sms_oi_status=71)
                        except Exception as e:
                            logging.getLogger('sms_log').error("%s - %s" % (str(mail_type), str(e)))

                elif oi.product.type_flow == 7:
                    data.update({
                        'upload_url': "%s://%s/autologin/%s/?next=dashboard" % (settings.SITE_PROTOCOL, settings.SITE_DOMAIN, token.decode())     
                    })
                    if 91 not in email_sets and 91 not in sms_sets:
                        send_email_task.apply_async((to_emails, mail_type, data, 91, oi.pk), countdown=900)
                        try:
                            urlshortener = create_short_url(login_url=data)
                            data.update({'url': urlshortener.get('url')})
                            SendSMS().send(sms_type=mail_type, data=data)
                            oi.smsorderitemoperation_set.create(sms_oi_status=91)
                        except Exception as e:
                            logging.getLogger('sms_log').error("%s - %s" % (str(mail_type), str(e)))

                elif oi.product.type_flow == 12:
                    data.update({
                        'upload_url': "%s://%s/autologin/%s/?next=dashboard" % (settings.SITE_PROTOCOL, settings.SITE_DOMAIN, token.decode())     
                    })
                    if 141 not in email_sets and 141 not in sms_sets:
                        send_email_task.apply_async((to_emails, mail_type, data, 141, oi.pk), countdown=900)
                        try:
                            urlshortener = create_short_url(login_url=data)
                            data.update({'url': urlshortener.get('url')})
                            SendSMS().send(sms_type=mail_type, data=data)
                            oi.smsorderitemoperation_set.create(sms_oi_status=141)
                        except Exception as e:
                            logging.getLogger('sms_log').error("%s - %s" % (str(mail_type), str(e)))

                elif oi.product.type_flow == 13:
                    data.update({
                        'upload_url': "%s://%s/autologin/%s/?next=dashboard" % (settings.SITE_PROTOCOL, settings.SITE_DOMAIN, token.decode())     
                    })
                    if 151 not in email_sets and 151 not in sms_sets:
                        send_email_task.apply_async((to_emails, mail_type, data, 151, oi.pk), countdown=900)
                        try:
                            urlshortener = create_short_url(login_url=data)
                            data.update({'url': urlshortener.get('url')})
                            SendSMS().send(sms_type=mail_type, data=data)
                            oi.smsorderitemoperation_set.create(sms_oi_status=151)
                        except Exception as e:
                            logging.getLogger('sms_log').error("%s - %s" % (str(mail_type), str(e)))

                elif oi.product.type_flow == 8:
                    data.update({
                        'counselling_form': "%s://%s/linkdin/counsellingform/%s" % (settings.SITE_PROTOCOL, settings.SITE_DOMAIN, oi.pk),
                    })
                    if 108 not in email_sets and 108 not in sms_sets:
                        send_email_task.apply_async((to_emails, mail_type, data, 108, oi.pk), countdown=900)
                        try:
                            urlshortener = create_short_url(login_url=data)
                            data.update({'url': urlshortener.get('url')})
                            SendSMS().send(sms_type=mail_type, data=data)
                            oi.smsorderitemoperation_set.create(sms_oi_status=108)
                        except Exception as e:
                            logging.getLogger('sms_log').error("%s - %s" % (str(mail_type), str(e)))

                elif oi.product.type_flow == 9:
                    data.update({
                        'complete_profile': "%s://%s/dashboard/roundone/profile/" % (settings.SITE_PROTOCOL, settings.SITE_DOMAIN) 
                    })
                    if 121 not in email_sets and 121 not in sms_sets:
                        send_email_task.apply_async((to_emails, mail_type, data, 121, oi.pk), countdown=900)
                        try:
                            urlshortener = create_short_url(login_url=data)
                            data.update({'url': urlshortener.get('url')})
                            SendSMS().send(sms_type=mail_type, data=data)
                            oi.smsorderitemoperation_set.create(sms_oi_status=121)
                        except Exception as e:
                            logging.getLogger('sms_log').error("%s - %s" % (str(mail_type), str(e)))

                elif oi.product.type_flow == 10:
                    data.update({
                        'test_url': "%s/dashboard" % (settings.SITE_DOMAIN) 
                    })
                    if 131 not in email_sets and 131 not in sms_sets:
                        send_email_task.apply_async((to_emails, mail_type, data, 131, oi.pk), countdown=900)
                        try:
                            urlshortener = create_short_url(login_url=data)
                            data.update({'url': urlshortener.get('url')})
                            SendSMS().send(sms_type=mail_type, data=data)
                            oi.smsorderitemoperation_set.create(sms_oi_status=131)
                        except Exception as e:
                            logging.getLogger('sms_log').error("%s - %s" % (str(mail_type), str(e)))

            except Exception as e:
                raise e


def process_mailer(order=None):
    if order.status == 1:
        orderitems = order.orderitems.filter(no_process=False).select_related('order', 'product', 'partner')
        for oi in orderitems:
            data = {}
            to_emails = [oi.order.email]
            mail_type = "PROCESS_MAILERS"
            data['subject'] = 'Your service details related to order <'+str(oi.order.id)+'>'
            data['username'] = oi.order.first_name if oi.order.first_name else oi.order.candidate_id,
            token = AutoLogin().encode(oi.order.email, oi.order.candidate_id, days=None)
            try:
                email_sets = list(oi.emailorderitemoperation_set.all().values_list('email_oi_status',flat=True).distinct())
                sms_sets = list(oi.smsorderitemoperation_set.all().values_list('sms_oi_status',flat=True).distinct())
                to_emails = [oi.order.email]
                mail_type = "PROCESS_MAILERS"
                data = {}
                data.update({
                    'subject': 'Your service details related to order <'+str(oi.order.id)+'>',
                    'username': oi.order.first_name if oi.order.first_name else oi.order.candidate_id,
                    'type_flow': oi.product.type_flow,
                    'pk': oi.pk,
                    'email': oi.order.email,
                    'candidateid': oi.order.email,
                })
                if oi.product.type_flow == 1:
                    data.update({
                        'upload_url': "%s://%s/autologin/%s/?next=dashboard" % (settings.SITE_PROTOCOL, settings.SITE_DOMAIN, token.decode()),
                    })
                    if 25 not in email_sets and 25 not in sms_sets:
                        send_email_task.apply_async((to_emails, mail_type, data, 25, oi.pk), countdown=600)
                        try:
                            SendSMS().send(sms_type=mail_type, data=data)
                            oi.smsorderitemoperation_set.create(sms_oi_status=25)
                        except Exception as e:
                            logging.getLogger('sms_log').error("%s - %s" % (str(mail_type), str(e)))

                elif oi.product.type_flow == 3:
                    data.update({
                        'upload_url': "%s://%s/autologin/%s/?next=dashboard" % (settings.SITE_PROTOCOL, settings.SITE_DOMAIN, token.decode()),
                    })
                    if 44 not in email_sets and 44 not in sms_sets:
                        send_email_task.apply_async((to_emails, mail_type, data, 44, oi.pk), countdown=600)
                        try:
                            SendSMS().send(sms_type=mail_type, data=data)
                            oi.smsorderitemoperation_set.create(sms_oi_status=44)
                        except Exception as e:
                            logging.getLogger('sms_log').error("%s - %s" % (str(mail_type), str(e)))

                elif oi.product.type_flow == 4:
                    data.update({
                        'upload_url': "%s://%s/autologin/%s/?next=dashboard" % (settings.SITE_PROTOCOL, settings.SITE_DOMAIN, token.decode()),
                    })
                    if 64 not in email_sets and 64 not in sms_sets:
                        send_email_task.apply_async((to_emails, mail_type, data, 64, oi.pk), countdown=600)
                        try:
                            SendSMS().send(sms_type=mail_type, data=data)
                            oi.smsorderitemoperation_set.create(sms_oi_status=64)
                        except Exception as e:
                            logging.getLogger('sms_log').error("%s - %s" % (str(mail_type), str(e)))

                elif oi.product.type_flow == 5:
                    data.update({
                        'upload_url': "%s://%s/autologin/%s/?next=dashboard" % (settings.SITE_PROTOCOL, settings.SITE_DOMAIN, token.decode()),
                    })
                    if 74 not in email_sets and 74 not in sms_sets:
                        send_email_task.apply_async((to_emails, mail_type, data, 74, oi.pk), countdown=600)
                        try:
                            SendSMS().send(sms_type=mail_type, data=data)
                            oi.smsorderitemoperation_set.create(sms_oi_status=74)
                        except Exception as e:
                            logging.getLogger('sms_log').error("%s - %s" % (str(mail_type), str(e)))

                elif oi.product.type_flow == 12:
                    data.update({
                        'upload_url': "%s://%s/autologin/%s/?next=dashboard" % (settings.SITE_DOMAIN, token.decode()),
                    })
                    if 145 not in email_sets and 145 not in sms_sets:
                        send_email_task.apply_async((to_emails, mail_type, data, 145, oi.pk), countdown=600)
                        try:
                            SendSMS().send(sms_type=mail_type, data=data)
                            oi.smsorderitemoperation_set.create(sms_oi_status=145)
                        except Exception as e:
                            logging.getLogger('sms_log').error("%s - %s" % (str(mail_type), str(e)))

                elif oi.product.type_flow == 13:
                    data.update({
                        'upload_url': "%s://%s/autologin/%s/?next=dashboard" % (settings.SITE_PROTOCOL, settings.SITE_DOMAIN, token.decode()),
                    })
                    if 155 not in email_sets and 155 not in sms_sets:
                        send_email_task.apply_async((to_emails, mail_type, data, 155, oi.pk), countdown=600)
                        try:
                            SendSMS().send(sms_type=mail_type, data=data)
                            oi.smsorderitemoperation_set.create(sms_oi_status=155)
                        except Exception as e:
                            logging.getLogger('sms_log').error("%s - %s" % (str(mail_type), str(e)))
                
                elif oi.product.type_flow == 7:
                    data.update({
                        'upload_url': "%s://%s/autologin/%s/?next=dashboard" % (settings.SITE_PROTOCOL, settings.SITE_DOMAIN, token.decode()),
                    })
                    if 94 not in email_sets and 94 not in sms_sets:
                        send_email_task.apply_async((to_emails, mail_type, data, 94, oi.pk), countdown=600)
                        try:
                            SendSMS().send(sms_type=mail_type, data=data)
                            oi.smsorderitemoperation_set.create(sms_oi_status=94)
                        except Exception as e:
                            logging.getLogger('sms_log').error("%s - %s" % (str(mail_type), str(e)))

                elif oi.product.type_flow == 2:
                    if 161 not in email_sets and 161 not in sms_sets:
                        send_email_task.apply_async((to_emails, mail_type, data, 161, oi.pk), countdown=600)
                        try:
                            SendSMS().send(sms_type=mail_type, data=data)
                            oi.smsorderitemoperation_set.create(sms_oi_status=161)
                        except Exception as e:
                            logging.getLogger('sms_log').error("%s - %s" % (str(mail_type), str(e)))

                elif oi.product.type_flow == 6:
                    if 171 not in email_sets and 171 not in sms_sets:
                        send_email_task.apply_async((to_emails, mail_type, data, 171, oi.pk), countdown=600)
                        try:
                            SendSMS().send(sms_type=mail_type, data=data)
                            oi.smsorderitemoperation_set.create(sms_oi_status=171)
                        except Exception as e:
                            logging.getLogger('sms_log').error("%s - %s" % (str(mail_type), str(e)))
                    
                elif oi.product.type_flow == 8:
                    data.update({
                        'counselling_form': "%s://%s/linkdin/counsellingform/%s" % (settings.SITE_PROTOCOL, settings.SITE_DOMAIN, oi.pk),
                    })
                    if 105 not in email_sets and 105 not in sms_sets:
                        send_email_task.apply_async((to_emails, mail_type, data, 105, oi.pk), countdown=600)
                        try:
                            SendSMS().send(sms_type=mail_type, data=data)
                            oi.smsorderitemoperation_set.create(sms_oi_status=105)
                        except Exception as e:
                            logging.getLogger('sms_log').error("%s - %s" % (str(mail_type), str(e)))
                    
                elif oi.product.type_flow == 9:
                    data.update({
                        'complete_profile': "%s://%s/dashboard/roundone/profile/" % (settings.SITE_PROTOCOL, settings.SITE_DOMAIN),
                    })
                    if 122 not in email_sets and 122 not in sms_sets:
                        send_email_task.apply_async((to_emails, mail_type, data, 122, oi.pk), countdown=600)
                        try:
                            SendSMS().send(sms_type=mail_type, data=data)
                            oi.smsorderitemoperation_set.create(sms_oi_status=122)
                        except Exception as e:
                            logging.getLogger('sms_log').error("%s - %s" % (str(mail_type), str(e)))
            except Exception as e:
                raise e


def payment_pending_mailer(order=None):
    try:
        pymt_objs = PaymentTxn.objects.filter(order=order, payment_mode__in=[1,4])
        if pymt_objs.exists():
            orderitems = order.orderitems.filter(no_process=False).select_related('order', 'product', 'partner')

            for oi in orderitems:
                pymt_obj = oi.order.ordertxns.get(order=order)
                email_sets = list(oi.emailorderitemoperation_set.all().values_list('email_oi_status',flat=True).distinct())
                sms_sets = list(oi.smsorderitemoperation_set.all().values_list('sms_oi_status',flat=True).distinct())
                if 1 not in email_sets and 1 not in sms_sets:
                    to_emails = [order.email]
                    mail_type = "PAYMENT_PENDING"
                    sms_type = 'OFFLINE_PAYMENT'
                    data = {}
                    data.update({
                        "subject": 'Your Shine Payment Confirmation pending',
                        "first_name": order.first_name if order.first_name else order.candidate_id,
                        "txn": pymt_obj.txn,
                        'mobile': oi.order.mobile,
                    })
                    send_email_task.delay(to_emails, mail_type, data, status=1, oi=oi.pk)
                    try:
                        SendSMS().send(sms_type=sms_type, data=data)
                        oi.smsorderitemoperation_set.create(sms_oi_status=1)
                    except Exception as e:
                        logging.getLogger('sms_log').error("%s - %s" % (str(sms_type), str(e)))

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
                    'site': 'https://' + settings.SITE_DOMAIN + settings.STATIC_URL,
                })
                try:
                    SendMail().send(to_emails, mail_type, invoice_data)
                except Exception as e:
                    logging.getLogger('email_log').error("payment pending %s - %s - %s" % (str(to_emails), str(mail_type), str(e)))
    except Exception as e:
        raise e


def service_initiation(order=None):
    try:
        if order:
            orderitems = order.orderitems.filter(no_process=False).select_related('order', 'product', 'partner')
            for oi in orderitems:
                data = {}
                token = token = AutoLogin().encode(oi.order.email, oi.order.candidate_id, days=None)
                sms_type = "SERVICE_INITIATION"
                data.update({
                    'mobile': oi.order.mobile,
                    'upload_url': "%s://%s/autologin/%s/?next=dashboard" % (settings.SITE_PROTOCOL, settings.SITE_DOMAIN, token.decode()),
                })
                sms_sets = list(oi.smsorderitemoperation_set.all().values_list('sms_oi_status',flat=True).distinct())
                if oi.product.type_flow == 2 and 162 not in sms_sets:
                    try:
                        urlshortener = create_short_url(login_url=data)
                        data.update({'url': urlshortener.get('url')})
                        SendSMS().send(sms_type=sms_type, data=data)
                        oi.smsorderitemoperation_set.create(sms_oi_status=162)
                    except Exception as e:
                        logging.getLogger('sms_log').error("%s - %s" % (str(sms_type), str(e)))
                elif oi.product.type_flow == 6 and 172 not in sms_sets:
                    try:
                        urlshortener = create_short_url(login_url=data)
                        data.update({'url': urlshortener.get('url')})
                        SendSMS().send(sms_type=sms_type, data=data)
                        oi.smsorderitemoperation_set.create(sms_oi_status=172)
                    except Exception as e:
                        logging.getLogger('sms_log').error("%s - %s" % (str(sms_type), str(e)))
                elif oi.product.type_flow == 10 and 133 not in sms_sets:
                    try:
                        urlshortener = create_short_url(login_url=data)
                        data.update({'url': urlshortener.get('url')})
                        SendSMS().send(sms_type=sms_type, data=data)
                        oi.smsorderitemoperation_set.create(sms_oi_status=133)
                    except Exception as e:
                        logging.getLogger('sms_log').error("%s - %s" % (str(sms_type), str(e)))
    except Exception as e:
        raise e  


def create_short_url(login_url={}):
    short_url = {}
    data = {}
    data['longUrl'] = login_url.get('upload_url')
    google_api = "%s?key=%s" % (settings.URL_SHORTENER_API, settings.URL_SHORTENER_ACCESS_KEY)
    response = requests.post(url=google_api, data=json.dumps(data), headers={'Content-Type': 'application/json'})
    if response.ok:
        resp = response.json()
        short_url.update({'url': resp.get('id')})
    return short_url
