import logging
import datetime

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings

from order.models import OrderItem, Order
from emailers.tasks import send_email_task
from emailers.sms import SendSMS
from users.tasks import user_register
from core.api_mixin import PriorityApplicantUpdate
from shop.choices import S_ATTR_DICT


class Command(BaseCommand):
    def handle(self, *args, **options):
        priority_applicant_creation()
        priority_applicant_removal()


def priority_applicant_creation():
    ''' featured profile cron for feature updation on shine.com'''

    priority_applicant_orderitems = OrderItem.objects.filter(
        order__status__in=[1, 3], product__type_flow=5, product__sub_type_flow=3, oi_status=30)

    priority_applicant_orderitems = priority_applicant_orderitems.select_related('order')

    priority_applicants_creation_count = 0

    for obj in priority_applicant_orderitems:
        candidate_id = None
        if obj.order.candidate_id:
            candidate_id = obj.order.candidate_id
        else:
            user_register(data={}, order=obj.order.pk)

            order = Order.objects.get(pk=obj.order.pk)
            if order.candidate_id:
                candidate_id = obj.order.candidate_id

        if candidate_id:
            try:
                data = {}
                data.update({
                    "ShineCareerPlus": {"xfr": 1},
                    # Temporary commented because of shine profile muddling
                    # "is_email_verified": 1,
                    # "is_cell_phone_verified": 1
                })
                flag = PriorityApplicantUpdate().update_applicant_priority(
                    candidate_id=candidate_id, data=data)
                if flag:
                    priority_applicants_creation_count += 1
                    last_oi_status = obj.oi_status
                    obj.oi_status = 28
                    obj.closed_on = timezone.now()
                    obj.last_oi_status = 6
                    obj.save()
                    obj.orderitemoperation_set.create(
                        oi_status=6,
                        last_oi_status=last_oi_status,
                        assigned_to=obj.assigned_to)
                    obj.orderitemoperation_set.create(
                        oi_status=obj.oi_status,
                        last_oi_status=obj.last_oi_status,
                        assigned_to=obj.assigned_to)

                    # Send mail and sms with subject line as Your Profile updated
                    try:
                        mail_type = "PRIORITY_APPLICANT_MAIL"
                        email_sets = list(
                            obj.emailorderitemoperation_set.all().values_list(
                                'email_oi_status', flat=True).distinct())
                        to_emails = [obj.order.get_email()]
                        data = {}
                        data.update({
                            "subject": 'Your Featured Profile Is Updated',
                            "username": obj.order.first_name,
                            "product_timeline": obj.product.get_duration_in_day(),
                        })

                        if 72 not in email_sets:
                            send_email_task.delay(
                                to_emails, mail_type, data,
                                status=72, oi=obj.pk)
                        SendSMS().send(sms_type=mail_type, data=data)
                    except Exception as e:
                        logging.getLogger('error_log').error((str(e)))
            except Exception as e:
                logging.getLogger('error_log').error((str(e)))

    out_str = out_str = '%s profile given priority out of %s' % (
        priority_applicants_creation_count, priority_applicant_orderitems.count())

    logging.getLogger('info_log').info("{}".format(out_str))


def priority_applicant_removal():
    ''' featured profile cron for closing updated orderitem '''

    priority_applicant_orderitems = OrderItem.objects.filter(
        order__status__in=[1, 3], product__type_flow=5, product__sub_type_flow=3, oi_status=28)
    priority_applicant_orderitems = priority_applicant_orderitems.select_related('order')

    priority_applicant_removal_count = 0

    for obj in priority_applicant_orderitems:
        candidate_id = None
        if obj.order.candidate_id:
            candidate_id = obj.order.candidate_id
        else:
            user_register(data={}, order=obj.order.pk)

            order = Order.objects.get(pk=obj.order.pk)
            if order.candidate_id:
                candidate_id = obj.order.candidate_id
        featured_ops = obj.orderitemoperation_set.filter(oi_status=28)

        try:
            activation_date = featured_ops[0].created
        except Exception as e:
            logging.getLogger('error_log').error("unable to create activation date%s" % (str(e)))
            continue

        if getattr(obj.product.attr, S_ATTR_DICT.get('FD'), None):
            duration_days = getattr(obj.product.attr, S_ATTR_DICT.get('FD'))
        else:
            duration_days = 180  # 6 months

        delta_time = activation_date + datetime.timedelta(days=duration_days)

        if candidate_id and delta_time < timezone.now():
            try:
                data = {}
                data.update({
                    "ShineCareerPlus": {"xfr": 0},
                    # "is_email_verified": 1,
                    # "is_cell_phone_verified": 1
                })
                flag = PriorityApplicantUpdate().update_applicant_priority(
                    candidate_id=candidate_id, data=data)
                if flag:
                    priority_applicant_removal_count += 1
                    last_oi_status = obj.oi_status
                    obj.oi_status = 4
                    obj.closed_on = timezone.now()
                    obj.last_oi_status = 29
                    obj.save()
                    obj.orderitemoperation_set.create(
                        oi_status=29,
                        last_oi_status=last_oi_status,
                        assigned_to=obj.assigned_to)
                    obj.orderitemoperation_set.create(
                        oi_status=obj.oi_status,
                        last_oi_status=obj.last_oi_status,
                        assigned_to=obj.assigned_to)
            except Exception as e:
                logging.getLogger('error_log').error((str(e)))
                print(str(e))

    out_str = '%s profile removed from priority out of %s priority items' % (
        priority_applicant_removal_count, priority_applicant_orderitems.count())

    logging.getLogger('info_log').info("{}".format(out_str))
