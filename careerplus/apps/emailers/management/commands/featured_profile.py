import logging
import datetime

from django.core.management.base import BaseCommand
from django.utils import timezone

from order.models import OrderItem, Order
from emailers.tasks import send_email_task
from emailers.sms import SendSMS
from users.tasks import user_register
from core.api_mixin import FeatureProfileUpdate
from shop.choices import S_ATTR_DICT


class Command(BaseCommand):
    def handle(self, *args, **options):
        featured_updated()
        unfeature()


def featured_updated():
    ''' featured profile cron for feature updation on shine.com'''

    featured_orderitems = OrderItem.objects.filter(
        order__status__in=[1, 3], product__type_flow=5, oi_status=30)
    featured_orderitems = featured_orderitems.select_related('order')

    featured_count = 0

    for obj in featured_orderitems:
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
                flag = FeatureProfileUpdate().update_feature_profile(
                    candidate_id=candidate_id, data=data)
                if flag:
                    featured_count += 1
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
                        mail_type = "FEATURED_PROFILE_UPDATED"
                        email_sets = list(
                            obj.emailorderitemoperation_set.all().values_list(
                                'email_oi_status', flat=True).distinct())
                        to_emails = [obj.order.email]
                        data = {}
                        data.update({
                            "subject": 'Your Featured Profile Is Updated',
                            "username": obj.order.first_name,
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

    out_str = out_str = '%s profile featured out of %s' % (
        featured_count, featured_orderitems.count())

    logging.getLogger('info_log').info("{}".format(out_str))


def unfeature():
    ''' featured profile cron for closing updated orderitem '''

    featured_orderitems = OrderItem.objects.filter(
        order__status__in=[1, 3], product__type_flow=5, oi_status=28)
    featured_orderitems = featured_orderitems.select_related('order')

    unfeature_count = 0

    for obj in featured_orderitems:
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
                flag = FeatureProfileUpdate().update_feature_profile(
                    candidate_id=candidate_id, data=data)
                if flag:
                    unfeature_count += 1
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

    out_str = '%s profile expired out of %s featured items' % (
        unfeature_count, featured_orderitems.count())

    logging.getLogger('info_log').info("{}".format(out_str))
