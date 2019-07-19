import logging
from celery.decorators import task
from django.conf import settings

from linkedin.autologin import AutoLogin

from order.functions import (
    create_short_url,
    send_email
)
from emailers.sms import SendSMS
from emailers.email import SendMail
from payment.models import PaymentTxn
from core.mixins import InvoiceGenerate
from coupon.mixins import CouponMixin
from api.config import LOCATION_MAPPING, INDUSTRY_MAPPING, DESIRED_SALARY_MAPPING
from shine.core import ShineCandidateDetail
from crmapi.config import (
    EXPERIENCE_IN_YEARS_MODEL_CHOICES
)

from shop.models import ProductUserProfile

@task(name="invoice_generation_order")
def invoice_generation_order(order_pk=None):
    from order.models import Order
    try:
        order = Order.objects.get(pk=order_pk)
        InvoiceGenerate().save_order_invoice_pdf(order=order)
    except Exception as e:
        logging.getLogger('error_log').error("invoice generation failed%s" % (str(e)))


@task(name="pending_item_email")
def pending_item_email(pk=None):
    from order.models import Order
    order = None
    try:
        order = Order.objects.get(pk=pk)
    except Exception as e:
        logging.getLogger('error_log').error(" unable to get order object %s - %s" % (str(order), str(e)))

    if order:
        orderitems = order.orderitems.filter(no_process=False).select_related(
            'order', 'product', 'partner')
        mail_flag_flow12 = False
        sms_flag_flow12 = False

        mail_flag_flow4 = False
        sms_flag_flow4 = False
        for oi in orderitems:
            data = {}
            mail_type = "PENDING_ITEMS"
            to_emails = [oi.order.get_email()]
            token = AutoLogin().encode(
                oi.order.email, oi.order.candidate_id, days=None)
            product_name = ''
            if oi.product.type_flow in [4, 12]:
                ois = orderitems.filter(
                    product__type_flow__in=[4, 12])
                for oi_item in ois:
                    product_name = product_name + oi_item.product.name + ','
            else:
                product_name = oi.product.name

            data.update({
                'subject': 'To initiate your services fulfil these details',
                'user': oi.order.first_name,
                'type_flow': oi.product.type_flow,
                'product_name': product_name,
                'product_url': oi.product.get_url(),
                'mobile': oi.order.get_mobile(),
                'parent_name': oi.parent.product.name if oi.parent else ""

            })
            email_sets = list(oi.emailorderitemoperation_set.all().values_list(
                'email_oi_status', flat=True).distinct())
            sms_sets = list(oi.smsorderitemoperation_set.all().values_list(
                'sms_oi_status', flat=True).distinct())
            try:
                if oi.product.type_flow == 1:
                    if 21 not in email_sets and 21 not in sms_sets:
                        data.update({
                            'upload_url': "%s://%s/autologin/%s/?next=/dashboard" % (
                                settings.SITE_PROTOCOL, settings.SITE_DOMAIN,
                                token)
                        })
                        send_email(to_emails, mail_type, data, 21, oi.pk)
                        try:
                            urlshortener = create_short_url(login_url=data)
                            data.update({'url': urlshortener.get('url')})
                            SendSMS().send(sms_type=mail_type, data=data)
                            oi.smsorderitemoperation_set.create(
                                sms_oi_status=21,
                                to_mobile=data.get('mobile'),
                                status=1)
                        except Exception as e:
                            logging.getLogger('error_log').error(
                                "%s - %s" % (str(mail_type), str(e)))

                elif oi.product.type_flow == 3:
                    data.update({
                        'upload_url': "%s://%s/autologin/%s/?next=/dashboard" % (
                            settings.SITE_PROTOCOL, settings.SITE_DOMAIN,
                            token)
                    })
                    if 41 not in email_sets and 41 not in sms_sets:
                        send_email(to_emails, mail_type, data, 41, oi.pk)
                        try:
                            urlshortener = create_short_url(login_url=data)
                            data.update({'url': urlshortener.get('url')})
                            SendSMS().send(sms_type=mail_type, data=data)
                            oi.smsorderitemoperation_set.create(
                                sms_oi_status=41,
                                to_mobile=data.get('mobile'),
                                status=1)
                        except Exception as e:
                            logging.getLogger('error_log').error(
                                "%s - %s" % (str(mail_type), str(e)))

                elif oi.product.type_flow == 4:
                    data.update({
                        'upload_url': "%s://%s/autologin/%s/?next=/dashboard" % (
                            settings.SITE_PROTOCOL, settings.SITE_DOMAIN,
                            token)
                    })

                    if not mail_flag_flow4 and 61 not in email_sets:
                        send_email(to_emails, mail_type, data, 61, oi.pk)
                        mail_flag_flow4 = True
                    elif 61 not in email_sets:
                        to_email = to_emails[0] if to_emails else oi.order.get_email()
                        oi.emailorderitemoperation_set.create(
                            email_oi_status=61, to_email=to_email,
                            status=1)

                    if not sms_flag_flow4 and 61 not in sms_sets:
                        try:
                            urlshortener = create_short_url(login_url=data)
                            data.update({'url': urlshortener.get('url')})
                            SendSMS().send(sms_type=mail_type, data=data)
                            oi.smsorderitemoperation_set.create(
                                sms_oi_status=61,
                                to_mobile=data.get('mobile'),
                                status=1)
                            sms_flag_flow4 = True
                        except Exception as e:
                            logging.getLogger('error_log').error("%s - %s" % (
                                str(mail_type), str(e)))
                    elif 61 not in sms_sets:
                        oi.smsorderitemoperation_set.create(
                            sms_oi_status=61,
                            to_mobile=data.get('mobile'),
                            status=1)


                    # if 61 not in email_sets and 61 not in sms_sets:
                    #     send_email(to_emails, mail_type, data, 61, oi.pk)
                    #     try:
                    #         urlshortener = create_short_url(login_url=data)
                    #         data.update({'url': urlshortener.get('url')})
                    #         SendSMS().send(sms_type=mail_type, data=data)
                    #         oi.smsorderitemoperation_set.create(
                    #             sms_oi_status=61,
                    #             to_mobile=data.get('mobile'),
                    #             status=1)
                    #     except Exception as e:
                    #         logging.getLogger('error_log').error("%s - %s" % (
                    #             str(mail_type), str(e)))

                elif oi.product.type_flow == 5:
                    data.update({
                        'upload_url': "%s://%s/autologin/%s/?next=/dashboard" % (
                            settings.SITE_PROTOCOL, settings.SITE_DOMAIN,
                            token)
                    })
                    if 71 not in email_sets and 71 not in sms_sets:
                        send_email(to_emails, mail_type, data, 71, oi.pk)
                        try:
                            urlshortener = create_short_url(login_url=data)
                            data.update({'url': urlshortener.get('url')})
                            SendSMS().send(sms_type=mail_type, data=data)
                            oi.smsorderitemoperation_set.create(
                                sms_oi_status=71,
                                to_mobile=data.get('mobile'),
                                status=1)
                        except Exception as e:
                            logging.getLogger('error_log').error(
                                "%s - %s" % (str(mail_type), str(e)))

                elif oi.product.type_flow  in  [7, 15]:
                    data.update({
                        'upload_url': "%s://%s/autologin/%s/?next=/dashboard" % (
                            settings.SITE_PROTOCOL, settings.SITE_DOMAIN,
                            token)
                    })
                    if 91 not in email_sets and 91 not in sms_sets:
                        send_email(to_emails, mail_type, data, 91, oi.pk)
                        try:
                            urlshortener = create_short_url(login_url=data)
                            data.update({'url': urlshortener.get('url')})
                            SendSMS().send(sms_type=mail_type, data=data)
                            oi.smsorderitemoperation_set.create(
                                sms_oi_status=91,
                                to_mobile=data.get('mobile'),
                                status=1)
                        except Exception as e:
                            logging.getLogger('error_log').error(
                                "%s - %s" % (str(mail_type), str(e)))

                elif oi.product.type_flow == 12:
                    data.update({
                        'upload_url': "%s://%s/autologin/%s/?next=/dashboard" % (
                            settings.SITE_PROTOCOL, settings.SITE_DOMAIN,
                            token)
                    })

                    if not mail_flag_flow12 and 141 not in email_sets:
                        send_email(to_emails, mail_type, data, 141, oi.pk)
                        mail_flag_flow12 = True
                    elif 141 not in email_sets:
                        to_email = to_emails[0] if to_emails else oi.order.get_email()
                        oi.emailorderitemoperation_set.create(
                            email_oi_status=141, to_email=to_email,
                            status=1)

                    if not sms_flag_flow12 and 141 not in sms_sets:
                        try:
                            urlshortener = create_short_url(login_url=data)
                            data.update({'url': urlshortener.get('url')})
                            SendSMS().send(sms_type=mail_type, data=data)
                            oi.smsorderitemoperation_set.create(
                                sms_oi_status=141,
                                to_mobile=data.get('mobile'),
                                status=1)
                            sms_flag_flow12 = True
                        except Exception as e:
                            logging.getLogger('error_log').error(
                                "%s - %s" % (str(mail_type), str(e)))
                    elif 141 not in sms_sets:
                        oi.smsorderitemoperation_set.create(
                            sms_oi_status=141,
                            to_mobile=data.get('mobile'),
                            status=1)

                    # if 141 not in email_sets and 141 not in sms_sets:
                    #     send_email(to_emails, mail_type, data, 141, oi.pk)
                    #     try:
                    #         urlshortener = create_short_url(login_url=data)
                    #         data.update({'url': urlshortener.get('url')})
                    #         SendSMS().send(sms_type=mail_type, data=data)
                    #         oi.smsorderitemoperation_set.create(
                    #             sms_oi_status=141,
                    #             to_mobile=data.get('mobile'),
                    #             status=1)
                    #     except Exception as e:
                    #         logging.getLogger('error_log').error(
                    #             "%s - %s" % (str(mail_type), str(e)))

                elif oi.product.type_flow == 13:
                    data.update({
                        'upload_url': "%s://%s/autologin/%s/?next=/dashboard" % (
                            settings.SITE_PROTOCOL, settings.SITE_DOMAIN,
                            token)
                    })
                    if 151 not in email_sets and 151 not in sms_sets:
                        send_email(to_emails, mail_type, data, 151, oi.pk)
                        try:
                            urlshortener = create_short_url(login_url=data)
                            data.update({'url': urlshortener.get('url')})
                            SendSMS().send(sms_type=mail_type, data=data)
                            oi.smsorderitemoperation_set.create(
                                sms_oi_status=151,
                                to_mobile=data.get('mobile'),
                                status=1)
                        except Exception as e:
                            logging.getLogger('error_log').error(
                                "%s - %s" % (str(mail_type), str(e)))

                elif oi.product.type_flow == 8:
                    data.update({
                        'upload_url': "%s://%s/autologin/%s/?next=/dashboard" % (
                            settings.SITE_PROTOCOL, settings.SITE_DOMAIN,
                            token)
                    })
                    if 108 not in email_sets and 108 not in sms_sets:
                        send_email(to_emails, mail_type, data, 108, oi.pk)
                        try:
                            urlshortener = create_short_url(login_url=data)
                            data.update({'url': urlshortener.get('url')})
                            SendSMS().send(sms_type=mail_type, data=data)
                            oi.smsorderitemoperation_set.create(
                                sms_oi_status=108,
                                to_mobile=data.get('mobile'),
                                status=1)
                        except Exception as e:
                            logging.getLogger('error_log').error(
                                "%s - %s" % (str(mail_type), str(e)))

                elif oi.product.type_flow == 9:
                    data.update({
                        'upload_url': "%s://%s/autologin/%s/?next=/dashboard/roundone/profile/" % (
                            settings.SITE_PROTOCOL, settings.SITE_DOMAIN,
                            token)
                    })
                    if 121 not in email_sets and 121 not in sms_sets:
                        send_email(to_emails, mail_type, data, 121, oi.pk)
                        try:
                            urlshortener = create_short_url(login_url=data)
                            data.update({'url': urlshortener.get('url')})
                            SendSMS().send(sms_type=mail_type, data=data)
                            oi.smsorderitemoperation_set.create(
                                sms_oi_status=121,
                                to_mobile=data.get('mobile'),
                                status=1)
                        except Exception as e:
                            logging.getLogger('error_log').error(
                                "%s - %s" % (str(mail_type), str(e)))

                elif oi.product.type_flow == 10:
                    data.update({
                        'test_url': "%s/dashboard" % (settings.SITE_DOMAIN)
                    })
                    if 131 not in email_sets and 131 not in sms_sets:
                        send_email(to_emails, mail_type, data, 131, oi.pk)
                        try:
                            urlshortener = create_short_url(login_url=data)
                            data.update({'url': urlshortener.get('url')})
                            SendSMS().send(sms_type=mail_type, data=data)
                            oi.smsorderitemoperation_set.create(
                                sms_oi_status=131,
                                to_mobile=data.get('mobile'),
                                status=1)
                        except Exception as e:
                            logging.getLogger('error_log').error(
                                "%s - %s" % (str(mail_type), str(e)))

            except Exception as e:
                logging.getLogger('error_log').error("%s" % (str(e)))


@task(name="process_mailer")
def process_mailer(pk=None):
    from order.models import Order
    order = None
    try:
        order = Order.objects.get(pk=pk)
    except Exception as e:
        logging.getLogger('error_log').error('unable to get order object%s' % str(e))
        raise e
    if order.status == 1:
        orderitems = order.orderitems.filter(no_process=False).select_related(
            'order', 'product', 'partner')
        for oi in orderitems:
            token = AutoLogin().encode(
                oi.order.email, oi.order.candidate_id, days=None)
            try:
                email_sets = list(oi.emailorderitemoperation_set.all().values_list(
                    'email_oi_status', flat=True).distinct())
                sms_sets = list(oi.smsorderitemoperation_set.all().values_list(
                    'sms_oi_status', flat=True).distinct())
                to_emails = [oi.order.get_email()]
                mail_type = "PROCESS_MAILERS"
                data = {}
                data.update({
                    'subject': 'Your service details related to order <' + str(oi.order.id) + '>',
                    'username': oi.order.first_name,
                    'type_flow': oi.product.type_flow,
                    'sub_type_flow': oi.product.sub_type_flow,
                    'pk': oi.pk,
                    'oi': oi,
                    'product_name': oi.product.name,
                    'product_url': oi.product.get_url(),
                    'vendor_name': oi.product.vendor.name,
                    'email': oi.order.get_email(),
                    'candidateid': oi.order.email,
                    'mobile': oi.order.get_mobile(),
                    'parent_name': oi.parent.product.name if oi.parent else None
                })
                if oi.product.type_flow in [1, 12, 13]:
                    data.update({
                        'upload_url': "%s://%s/autologin/%s/?next=/dashboard" % (
                            settings.SITE_PROTOCOL, settings.SITE_DOMAIN,
                            token),
                    })
                    if 25 not in email_sets and 25 not in sms_sets:
                        send_email(to_emails, mail_type, data, 25, oi.pk)
                        try:
                            SendSMS().send(sms_type=mail_type, data=data)
                            oi.smsorderitemoperation_set.create(
                                sms_oi_status=25,
                                to_mobile=data.get('mobile'),
                                status=1)
                        except Exception as e:
                            logging.getLogger('error_log').error(
                                "%s - %s" % (str(mail_type), str(e)))

                elif oi.product.type_flow == 3:
                    data.update({
                        'upload_url': "%s://%s/autologin/%s/?next=/dashboard" % (
                            settings.SITE_PROTOCOL, settings.SITE_DOMAIN,
                            token),
                    })
                    if 44 not in email_sets and 44 not in sms_sets:
                        send_email(to_emails, mail_type, data, 44, oi.pk)
                        try:
                            SendSMS().send(sms_type=mail_type, data=data)
                            oi.smsorderitemoperation_set.create(
                                sms_oi_status=44,
                                to_mobile=data.get('mobile'),
                                status=1)
                        except Exception as e:
                            logging.getLogger('error_log').error(
                                "%s - %s" % (str(mail_type), str(e)))

                elif oi.product.type_flow == 4:
                    data.update({
                        'upload_url': "%s://%s/autologin/%s/?next=/dashboard" % (
                            settings.SITE_PROTOCOL, settings.SITE_DOMAIN,
                            token),
                    })
                    if 64 not in email_sets and 64 not in sms_sets:
                        send_email(to_emails, mail_type, data, 64, oi.pk)
                        try:
                            SendSMS().send(sms_type=mail_type, data=data)
                            oi.smsorderitemoperation_set.create(
                                sms_oi_status=64,
                                to_mobile=data.get('mobile'),
                                status=1)
                        except Exception as e:
                            logging.getLogger('error_log').error(
                                "%s - %s" % (str(mail_type), str(e)))

                elif oi.product.type_flow == 5:
                    data.update({
                        'upload_url': "%s://%s/autologin/%s/?next=/dashboard" % (
                            settings.SITE_PROTOCOL, settings.SITE_DOMAIN,
                            token),
                    })
                    if 74 not in email_sets and 74 not in sms_sets:
                        send_email(to_emails, mail_type, data, 74, oi.pk)
                        try:
                            SendSMS().send(sms_type=mail_type, data=data)
                            oi.smsorderitemoperation_set.create(
                                sms_oi_status=74,
                                to_mobile=data.get('mobile'),
                                status=1)
                        except Exception as e:
                            logging.getLogger('error_log').error(
                                "%s - %s" % (str(mail_type), str(e)))

                elif oi.product.type_flow == 12:
                    data.update({
                        'upload_url': "%s://%s/autologin/%s/?next=/dashboard" % (
                            settings.SITE_DOMAIN, settings.SITE_DOMAIN,
                            token),
                    })
                    if 145 not in email_sets and 145 not in sms_sets:
                        send_email(to_emails, mail_type, data, 145, oi.pk)
                        try:
                            SendSMS().send(sms_type=mail_type, data=data)
                            oi.smsorderitemoperation_set.create(
                                sms_oi_status=145,
                                to_mobile=data.get('mobile'),
                                status=1)
                        except Exception as e:
                            logging.getLogger('error_log').error(
                                "%s - %s" % (str(mail_type), str(e)))

                elif oi.product.type_flow == 13:
                    data.update({
                        'upload_url': "%s://%s/autologin/%s/?next=/dashboard" % (
                            settings.SITE_PROTOCOL, settings.SITE_DOMAIN,
                            token),
                    })
                    if 155 not in email_sets and 155 not in sms_sets:
                        send_email(to_emails, mail_type, data, 155, oi.pk)
                        try:
                            SendSMS().send(sms_type=mail_type, data=data)
                            oi.smsorderitemoperation_set.create(
                                sms_oi_status=155,
                                to_mobile=data.get('mobile'),
                                status=1)
                        except Exception as e:
                            logging.getLogger('error_log').error(
                                "%s - %s" % (str(mail_type), str(e)))

                elif oi.product.type_flow in [7, 15]:
                    data.update({
                        'upload_url': "%s://%s/autologin/%s/?next=/dashboard" % (
                            settings.SITE_PROTOCOL, settings.SITE_DOMAIN,
                            token),
                    })
                    if 94 not in email_sets and 94 not in sms_sets:
                        send_email(to_emails, mail_type, data, 94, oi.pk)
                        try:
                            SendSMS().send(sms_type=mail_type, data=data)
                            oi.smsorderitemoperation_set.create(
                                sms_oi_status=94,
                                to_mobile=data.get('mobile'),
                                status=1)
                        except Exception as e:
                            logging.getLogger('error_log').error(
                                "%s - %s" % (str(mail_type), str(e)))

                elif oi.product.type_flow == 2:
                    if 161 not in email_sets and 161 not in sms_sets:
                        send_email(to_emails, mail_type, data, 161, oi.pk)
                        try:
                            SendSMS().send(sms_type=mail_type, data=data)
                            oi.smsorderitemoperation_set.create(
                                sms_oi_status=161,
                                to_mobile=data.get('mobile'),
                                status=1)
                        except Exception as e:
                            logging.getLogger('error_log').error(
                                "%s - %s" % (str(mail_type), str(e)))

                elif oi.product.type_flow == 14:
                    if 191 not in email_sets and 191 not in sms_sets:
                        send_email(to_emails, mail_type, data, 191, oi.pk)
                        try:
                            SendSMS().send(sms_type=mail_type, data=data)
                            oi.smsorderitemoperation_set.create(
                                sms_oi_status=191,
                                to_mobile=data.get('mobile'),
                                status=1)
                        except Exception as e:
                            logging.getLogger('error_log').error(
                                "%s - %s" % (str(mail_type), str(e)))

                elif oi.product.type_flow == 6:
                    if 171 not in email_sets and 171 not in sms_sets:
                        send_email(to_emails, mail_type, data, 171, oi.pk)
                        try:
                            SendSMS().send(sms_type=mail_type, data=data)
                            oi.smsorderitemoperation_set.create(
                                sms_oi_status=171,
                                to_mobile=data.get('mobile'),
                                status=1)
                        except Exception as e:
                            logging.getLogger('error_log').error(
                                "%s - %s" % (str(mail_type), str(e)))

                elif oi.product.type_flow == 8:
                    data.update({
                        'upload_url': "%s://%s/autologin/%s/?next=/dashboard" % (
                            settings.SITE_PROTOCOL, settings.SITE_DOMAIN,
                            token),
                    })
                    if 105 not in email_sets and 105 not in sms_sets:
                        send_email(to_emails, mail_type, data, 105, oi.pk)
                        try:
                            SendSMS().send(sms_type=mail_type, data=data)
                            oi.smsorderitemoperation_set.create(
                                sms_oi_status=105,
                                to_mobile=data.get('mobile'),
                                status=1)
                        except Exception as e:
                            logging.getLogger('error_log').error(
                                "%s - %s" % (str(mail_type), str(e)))

                elif oi.product.type_flow == 9:
                    data.update({
                        'upload_url': "%s://%s/autologin/%s/?next=/dashboard/roundone/profile/" % (
                            settings.SITE_PROTOCOL, settings.SITE_DOMAIN,
                            token)
                    })
                    if 122 not in email_sets and 122 not in sms_sets:
                        send_email(to_emails, mail_type, data, 122, oi.pk)
                        try:
                            SendSMS().send(sms_type=mail_type, data=data)
                            oi.smsorderitemoperation_set.create(
                                sms_oi_status=122,
                                to_mobile=data.get('mobile'),
                                status=1)
                        except Exception as e:
                            logging.getLogger('error_log').error(
                                "%s - %s" % (str(mail_type), str(e)))
            except Exception as e:
                logging.getLogger('error_log').error(str(e))
                raise e


@task(name="payment_pending_mailer")
def payment_pending_mailer(pk=None):
    from order.models import Order
    order = None
    try:
        order = Order.objects.get(pk=pk)
    except Exception as e:
        logging.getLogger('error_log').error("%s - %s" % (str(order), str(e)))
    try:
        pymt_objs = PaymentTxn.objects.filter(
            order=order, payment_mode__in=[1, 4])
        if pymt_objs.exists():
            orderitems = order.orderitems.filter(
                no_process=False).select_related('order', 'product', 'partner')

            mail_flag = False
            sms_flag = False

            for oi in orderitems:
                pymt_obj = oi.order.ordertxns.get(order=order)
                email_sets = list(
                    oi.emailorderitemoperation_set.all().values_list(
                        'email_oi_status', flat=True).distinct())
                sms_sets = list(
                    oi.smsorderitemoperation_set.all().values_list(
                        'sms_oi_status', flat=True).distinct())

                data = {}
                data.update({
                    "subject": 'Your Shine Payment Confirmation pending',
                    "username": order.first_name,
                    "txn": pymt_obj.txn,
                    'mobile': oi.order.get_mobile(),
                })
                mail_type = "PAYMENT_PENDING"
                sms_type = 'OFFLINE_PAYMENT'

                to_emails = [order.get_email()]
                if not mail_flag and 1 not in email_sets:
                    send_email(to_emails, mail_type, data, status=1, oi=oi.pk)
                    mail_flag = True
                elif 1 not in email_sets:
                    to_email = to_emails[0] if to_emails else oi.order.get_email()
                    oi.emailorderitemoperation_set.create(
                        email_oi_status=1, to_email=to_email,
                        status=1)

                if not sms_flag and 1 not in sms_sets:
                    try:
                        SendSMS().send(sms_type=sms_type, data=data)
                        oi.smsorderitemoperation_set.create(
                            sms_oi_status=1,
                            to_mobile=data.get('mobile'),
                            status=1)
                    except Exception as e:
                        logging.getLogger('error_log').error(
                            "%s - %s" % (str(sms_type), str(e)))
                elif 1 not in sms_sets:
                    oi.smsorderitemoperation_set.create(
                        sms_oi_status=1,
                        to_mobile=data.get('mobile'),
                        status=1)

                # if 1 not in email_sets and 1 not in sms_sets:
                #     to_emails = [order.email]
                #     mail_type = "PAYMENT_PENDING"
                #     sms_type = 'OFFLINE_PAYMENT'
                #     data = {}
                #     data.update({
                #         "subject": 'Your Shine Payment Confirmation pending',
                #         "username": order.first_name,
                #         "txn": pymt_obj.txn,
                #         'mobile': oi.order.mobile,
                #     })
                #     send_email(to_emails, mail_type, data, status=1, oi=oi.pk)
                #     try:
                #         SendSMS().send(sms_type=sms_type, data=data)
                #         oi.smsorderitemoperation_set.create(
                #             sms_oi_status=1,
                #             to_mobile=data.get('mobile'),
                #             status=1)
                #     except Exception as e:
                #         logging.getLogger('error_log').error(
                #             "%s - %s" % (str(sms_type), str(e)))
    except Exception as e:
        logging.getLogger('error_log').error("%s - %s" % (str(mail_type), str(e)))


@task(name="payment_realisation_mailer")
def payment_realisation_mailer(pk=None):
    from order.models import Order
    order = None
    mail_type = "SHINE_PAYMENT_CONFIRMATION"
    try:
        order = Order.objects.get(pk=pk)
    except Exception as e:
        logging.getLogger('error_log').error('unable to get order object %s'%str(e))
    try:
        invoice_data = InvoiceGenerate().get_invoice_data(order=order)
        pymt_objs = PaymentTxn.objects.filter(order=order)
        for pymt_obj in pymt_objs:
            if pymt_obj.status == 1:
                to_emails = [order.get_email()]
                # feature coupon
                courses_p = order.orderitems.filter(
                    product__product_class__slug__in=settings.COURSE_SLUG)
                if courses_p.exists():
                    coupon_obj = CouponMixin().create_feature_coupon(
                        users=[order.email])
                else:
                    coupon_obj = None
                if coupon_obj:
                    feature_coupon_code = coupon_obj.code
                else:
                    feature_coupon_code = ''
                invoice_data.update({
                    'subject': 'Your Shine Payment Confirmation',
                    "first_name": order.first_name,
                    "txn": pymt_obj.txn,
                    "order_id": order.id,
                    'feature_coupon_code': feature_coupon_code,
                    'site': 'https://' + settings.SITE_DOMAIN + settings.STATIC_URL,
                })
                try:
                    SendMail().send(to_emails, mail_type, invoice_data)
                    logging.getLogger('info_log').info(
                        "payment realisation mail send to %s - %s" % (
                            str(to_emails), str(mail_type)))
                except Exception as e:
                    logging.getLogger('error_log').error(
                        "payment realisation %s - %s - %s" % (
                            str(to_emails), str(mail_type), str(e)))
    except Exception as e:
        logging.getLogger('error_log').error(
            "%s - %s" % (str(mail_type), str(e)))


@task(name="service_initiation")
def service_initiation(pk=None):
    from order.models import Order
    order = None
    try:
        order = Order.objects.get(pk=pk)
    except Exception as e:
        logging.getLogger('error_log').error('unable to get order object%s'%str(e))
    try:
        if order:
            orderitems = order.orderitems.filter(
                no_process=False).select_related('order', 'product', 'partner')
            for oi in orderitems:
                data = {}
                token = token = AutoLogin().encode(
                    oi.order.get_email(), oi.order.candidate_id, days=None)
                sms_type = "SERVICE_INITIATION"
                data.update({
                    'mobile': oi.order.get_mobile(),
                    'upload_url': "%s://%s/autologin/%s/?next=/dashboard" % (
                        settings.SITE_PROTOCOL, settings.SITE_DOMAIN,
                        token),
                })
                sms_sets = list(
                    oi.smsorderitemoperation_set.all().values_list(
                        'sms_oi_status', flat=True).distinct())

                if oi.product.type_flow == 2 and 162 not in sms_sets:
                    try:
                        urlshortener = create_short_url(login_url=data)
                        data.update({'url': urlshortener.get('url')})
                        SendSMS().send(sms_type=sms_type, data=data)
                        oi.smsorderitemoperation_set.create(
                            sms_oi_status=162,
                            to_mobile=data.get('mobile'),
                            status=1)
                    except Exception as e:
                        logging.getLogger('error_log').error(
                            "%s - %s" % (str(sms_type), str(e)))

                elif oi.product.type_flow == 14 and 192 not in sms_sets:
                    try:
                        urlshortener = create_short_url(login_url=data)
                        data.update({'url': urlshortener.get('url')})
                        SendSMS().send(sms_type=sms_type, data=data)
                        oi.smsorderitemoperation_set.create(
                            sms_oi_status=192,
                            to_mobile=data.get('mobile'),
                            status=1)
                    except Exception as e:
                        logging.getLogger('error_log').error(
                            "%s - %s" % (str(sms_type), str(e)))

                elif oi.product.type_flow == 6 and 172 not in sms_sets:
                    try:
                        urlshortener = create_short_url(login_url=data)
                        data.update({'url': urlshortener.get('url')})
                        SendSMS().send(sms_type=sms_type, data=data)
                        oi.smsorderitemoperation_set.create(
                            sms_oi_status=172,
                            to_mobile=data.get('mobile'),
                            status=1)
                    except Exception as e:
                        logging.getLogger('error_log').error("%s - %s" % (
                            str(sms_type), str(e)))
                elif oi.product.type_flow == 10 and 133 not in sms_sets:
                    try:
                        urlshortener = create_short_url(login_url=data)
                        data.update({'url': urlshortener.get('url')})
                        SendSMS().send(sms_type=sms_type, data=data)
                        oi.smsorderitemoperation_set.create(
                            sms_oi_status=133,
                            to_mobile=data.get('mobile'),
                            status=1)
                    except Exception as e:
                        logging.getLogger('error_log').error(
                            "%s - %s" % (str(sms_type), str(e)))
    except Exception as e:
        logging.getLogger('error_log').error('service initiation failed%s'%str(e))


@task(name="process_jobs_on_the_move")
def process_jobs_on_the_move(obj_id=None):
    from order.models import OrderItem
    obj = OrderItem.objects.filter(id=obj_id).first()
    # create jobs on the move profile after welcome call is done.
    if obj:
        if obj.is_combo and obj.parent:
            wc_cat = obj.parent.wc_cat
            wc_sub_cat = obj.parent.wc_sub_cat
        else:
            wc_cat = obj.wc_cat
            wc_sub_cat = obj.wc_sub_cat
        if ((wc_cat == 21 and wc_sub_cat in [41, 42]) or (wc_cat == 22 and wc_sub_cat == 63)) and \
                not getattr(obj, 'whatsapp_profile_orderitem', False):
            other_jobs_on_the_move = OrderItem.objects.filter(
                order__status__in=[1, 3],
                product__type_flow__in=[5],
                oi_status__in=[31, 32],
                product__sub_type_flow=502,
                order__candidate_id=obj.order.candidate_id
            ).exclude(whatsapp_profile_orderitem=None).first()

            desired_industry, desired_location, desired_salary, current_salary, experience, skills = '', '' ,'', '', '', ''

            if other_jobs_on_the_move:
                desired_industry = other_jobs_on_the_move.whatsapp_profile_orderitem.desired_industry
                desired_location = other_jobs_on_the_move.whatsapp_profile_orderitem.desired_location
                desired_salary = other_jobs_on_the_move.whatsapp_profile_orderitem.desired_salary
                current_salary = other_jobs_on_the_move.whatsapp_profile_orderitem.current_salary
                experience = other_jobs_on_the_move.whatsapp_profile_orderitem.experience
                skills = other_jobs_on_the_move.whatsapp_profile_orderitem.skills
            else:
                resp_status = ShineCandidateDetail().get_candidate_detail(email=obj.order.email, shine_id=None)

                if 'total_experience' in resp_status and resp_status['total_experience']:
                    experience_years = resp_status['total_experience'][0].get('experience_in_years', 0)
                    experience_months = resp_status['total_experience'][0].get('experience_in_months', 0)

                    experience_years = dict(EXPERIENCE_IN_YEARS_MODEL_CHOICES).get(experience_years)
                    if experience_months:
                        experience_months = str(experience_months) + ' months' 
                    experience = '{} {}'.format(experience_years, experience_months)

                if 'skills' in resp_status and resp_status['skills']:
                    skills = ','.join([i['value'] for i in resp_status['skills']])[0:99]

                if resp_status and 'desired_job' in resp_status:

                    candidate_data = resp_status['desired_job'][0]

                    # Get canidate location
                    candidate_location = candidate_data['candidate_location']
                    desired_location = ','.join([LOCATION_MAPPING.get(loc, '') for loc in candidate_location])[0:244]

                    # Get candidate industry
                    candidate_industry = candidate_data['industry']
                    desired_industry = ','.join([INDUSTRY_MAPPING.get(ind, '') for ind in candidate_industry])[0:244]

                    # Get desired salary
                    maximum_salary = candidate_data['maximum_salary']
                    expected_min_salary = ','.join([DESIRED_SALARY_MAPPING.get(l, 'N.A') for l in maximum_salary])

                    minimum_salary = candidate_data['minimum_salary']
                    expected_max_salary = ','.join([DESIRED_SALARY_MAPPING.get(l, 'N.A') for l in minimum_salary])

                    desired_salary = expected_min_salary if expected_min_salary else expected_max_salary

                    # get current salary
                    salary_in_lakh = resp_status['workex'][0]['salary_in_lakh']
                    salary_in_thousand = resp_status['workex'][0]['salary_in_thousand']
                    current_salary = str(salary_in_lakh) + 'Lakh ' + str(salary_in_thousand) + 'Thousand'

            ProductUserProfile.objects.create(
                order_item=obj,
                contact_number=obj.order.mobile,
                desired_industry=desired_industry,
                desired_location=desired_location,
                desired_salary=desired_salary,
                current_salary=current_salary,
                experience=experience,
                skills=skills
            )
            obj.update_pending_links_count()


@task
def generate_resume_for_order(order_id):
    from resumebuilder.models import Candidate
    from order.models import Order
    from resumebuilder.utils import ResumeGenerator
    order_obj = Order.objects.get(id=order_id)
    candidate_id = order_obj.candidate_id

    for item in order_obj.orderitems.all():
        if item.product and item.product.type_flow == 17 and item.product.type_product == 2:
            product_id = item.product.id
            break

    is_combo = True if product_id != settings.RESUME_BUILDER_NON_COMBO_PID else False
    selected_template = Candidate.objects.filter(candidate_id = candidate_id).first().selected_template
    builder_obj = ResumeGenerator()
    builder_obj.save_order_resume_pdf(order=order_obj,is_combo=is_combo,index=selected_template)


@task
def send_resume_in_mail_resume_builder(attachment,data):
    to_email = [data.get('email')]
    mail_type = "SEND_RESUME_IN_MAIL_RESUME_BUILDER"
    try:
        SendMail().send(to_email, mail_type, data,attachment=attachment)
    except Exception as e:
        logging.getLogger('error_log').error(
            "%s" % (str(e)))




