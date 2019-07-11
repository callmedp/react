import logging
import datetime

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings
from django.db.models import Q

from order.models import OrderItem, Order
from emailers.tasks import send_email_task
from emailers.sms import SendSMS
from emailers.utils import get_featured_profile_data_for_candidate
from users.tasks import user_register
from core.api_mixin import FeatureProfileUpdate
from shop.choices import S_ATTR_DICT, A_ATTR_DICT


class Command(BaseCommand):
    def handle(self, *args, **options):
        featured_updated()
        unfeature()


def featured_updated():
    ''' featured profile cron for feature updation on shine.com'''

    featured_orderitems = OrderItem.objects.filter(
        order__status__in=[1, 3], product__type_flow__in=[5], oi_status=30,
        product__sub_type_flow__in=[501, 503])
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
                data = get_featured_profile_data_for_candidate(
                    candidate_id=candidate_id, curr_order_item=obj, feature=True)
                flag = FeatureProfileUpdate().update_feature_profile(
                    candidate_id=candidate_id, data=data)
                if flag:
                    logging.getLogger('info_log').info(
                        'Feature:- Data sent to shine for order item %s is %s' % (str(obj.id), str(data))
                    )
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
                        if obj.product.sub_type_flow == 501:
                            mail_type = "FEATURED_PROFILE_UPDATED"
                        elif obj.product.sub_type_flow == 503:
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

    out_str = out_str = '%s profile featured out of %s' % (
        featured_count, featured_orderitems.count())

    logging.getLogger('info_log').info("{}".format(out_str))


def unfeature():
    ''' featured profile cron for closing updated orderitem '''

    featured_orderitems = OrderItem.objects.filter(
        order__status__in=[1, 3], product__type_flow__in=[5], oi_status=28, product__sub_type_flow__in=[501, 503])
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
        if obj.product.sub_type_flow == 502:
            featured_ops = obj.orderitemoperation_set.filter(oi_status=5)
        else:
            featured_ops = obj.orderitemoperation_set.filter(oi_status=28)

        try:
            activation_date = featured_ops[0].created
        except Exception as e:
            logging.getLogger('error_log').error("unable to create activation date%s" % (str(e)))
            continue
        duration_dict = {
            'service': getattr(obj.product.attr, S_ATTR_DICT.get('FD'), 180),
            'assessment': getattr(obj.product.attr, A_ATTR_DICT.get('AD'), 365)
        }

        duration_days = duration_dict.get(obj.product.product_class.name)

        delta_time = activation_date + datetime.timedelta(days=duration_days)

        if candidate_id and delta_time < timezone.now():
            try:
                data = {}
                data = get_featured_profile_data_for_candidate(
                    candidate_id=candidate_id, curr_order_item=obj, feature=False)
                flag = FeatureProfileUpdate().update_feature_profile(
                    candidate_id=candidate_id, data=data)
                if flag:
                    logging.getLogger('info_log').info(
                        'Unfeature:- Data sent to shine for order item %s is %s' % (str(obj.id), str(data))
                    )
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
