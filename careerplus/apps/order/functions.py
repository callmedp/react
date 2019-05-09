import logging
import json
import requests
from django.conf import settings
from emailers.email import SendMail
from dateutil import relativedelta
from emailers.email import SendMail
from emailers.sms import SendSMS
from django.utils import timezone


def update_initiat_orderitem_sataus(order=None):
    if order:
        orderitems = order.orderitems.filter(
            no_process=False).select_related('order', 'product', 'partner')

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

            elif oi.product.type_flow in [2, 14]:
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
                    if oi.product.sub_type_flow == 502:
                        oi.oi_status = 5
                    else:
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

            elif oi.product.type_flow in [7, 15]:
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
                else:
                    last_oi_status = oi.oi_status
                    oi.oi_status = 2
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

            elif oi.product.type_flow == 16:
                last_oi_status = oi.oi_status
                oi.oi_status = 5
                oi.last_oi_status = last_oi_status
                oi.save()
                oi.orderitemoperation_set.create(
                    oi_status=oi.oi_status,
                    last_oi_status=last_oi_status,
                    assigned_to=oi.assigned_to)


def get_upload_path_order_invoice(instance, filename):
    return "invoice/order/{order_id}/{filename}".format(
        order_id=instance.id, filename=filename)


def create_short_url(login_url={}):
    short_url = {}
    data = {}
    data['longUrl'] = login_url.get('upload_url')
    google_api = "%s?key=%s" % (
        settings.URL_SHORTENER_API, settings.URL_SHORTENER_ACCESS_KEY)
    response = requests.post(
        url=google_api, data=json.dumps(data),
        headers={'Content-Type': 'application/json'})
    if response.ok:
        resp = response.json()
        short_url.update({'url': resp.get('id')})
    return short_url


def send_email(to_emails, mail_type, email_dict, status=None, oi=None):
    try:
        SendMail().send(to_emails, mail_type, email_dict)
        if oi:
            from order.models import OrderItem
            obj = OrderItem.objects.filter(pk=oi)
            for oi_item in obj:
                to_email = to_emails[0] if to_emails else oi_item.order.get_email()
                oi_item.emailorderitemoperation_set.create(
                    email_oi_status=status, to_email=to_email,
                    status=1)
    except Exception as e:
        logging.getLogger('error_log').error(
            "email sending failed %s - %s - %s" % (str(to_emails), str(e), str(mail_type)))


def send_email_from_base(subject=None, body=None, to=[], headers=None, oi=None, status=None):
    try:
        SendMail().base_send_mail(subject, body, to=[], headers=None, bcc=[settings.DEFAULT_FROM_EMAIL])
        if oi:
            from order.models import OrderItem
            obj = OrderItem.objects.get(pk=oi)
            to = to[0] if to else obj.order.get_email()
            obj.emailorderitemoperation_set.create(
                email_oi_status=status,
                to_email=to, status=1)
    except Exception as e:
        logging.getLogger('error_log').error(
            "%s - %s - %s" % (str(to), str(e)))


def date_timezone_convert(date=None):
    from pytz import timezone
    if not date:
        return 'N.A'
    return date.astimezone(timezone(settings.TIME_ZONE))



def date_diff(date1,date2):
    datediff = relativedelta.relativedelta(date1, date2)
    # return str(datediff.days) + '-days-' + str(datediff.hours)+'-hours-'\
    #        +str(datediff.minutes)+'-minutes'
    #only returning days difference
    return str(datediff.days)


def close_resume_booster_ois(ois_to_update):
    from order.models import OrderItem
    for oi in OrderItem.objects.filter(id__in=ois_to_update):
        last_oi_status = oi.oi_status
        oi.oi_status = 4
        oi.last_oi_status = 6
        oi.closed_on = timezone.now()
        oi.save()
        # status as tuple (status, last_status)
        # if order is in service under progress create three operation
        # resume boosted, service progress and order closed.
        # else create single operation resume boosted.
        if last_oi_status == 5:
            oi_statuses = ((62, last_oi_status), (6, 62), (4, 6))
        else:
            oi_statuses = ((62, last_oi_status),)

        for status, last_status in oi_statuses:
            oi.orderitemoperation_set.create(
                oi_status=status,
                last_oi_status=last_status,
                assigned_to=oi.assigned_to,
            )
        oi.emailorderitemoperation_set.create(email_oi_status=92)
