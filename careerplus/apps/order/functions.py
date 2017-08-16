import logging

from django.utils import timezone

from emailers.email import SendMail
from emailers.sms import SendSMS


def update_initiat_orderitem_sataus(order=None):
    if order:
        orderitems = order.orderitems.all().select_related('order', 'product', 'partner')
        midout_services = orderitems.filter(
            product__type_flow__in=[1, 3, 4, 5, 12, 13])

        # mai and sms
        if midout_services.exists() and order.status == 1:
            to_emails = [order.email]
            mail_type = "MIDOUT"
            data = {}
            data.update({
                "info": 'Upload Your resume',
                "subject": 'Upload Your Resume',
                "name": order.first_name + ' ' + order.last_name,
                "mobile": order.mobile,
            })
            try:
                SendMail().send(to_emails, mail_type, data)
                order.midout_sent_on = timezone.now()
                order.save()
            except Exception as e:
                logging.getLogger('email_log').error("reminder cron %s - %s - %s" % (str(to_emails), str(mail_type), str(e)))

            try:
                SendSMS().send(sms_type=mail_type, data=data)
            except Exception as e:
                logging.getLogger('sms_log').error("%s - %s" % (str(mail_type), str(e)))

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


def get_upload_path_order_invoice(instance, filename):
    return "invoice/order/{order_id}/{filename}".format(
        order_id=instance.id, filename=filename)