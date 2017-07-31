from django.core.management.base import BaseCommand
from django.utils import timezone

from order.models import OrderItem, Order
from emailers.email import SendMail
from emailers.sms import SendSMS
from users.tasks import user_register
from core.api_mixin import FeatureProfileUpdate


class Command(BaseCommand):
    def handle(self, *args, **options):
        featured_updated()
        print ("updated fetaured profiles closed")


def featured_updated():
    ''' featured profile cron for closing updated orderitem '''

    featured_orderitems = OrderItem.objects.filter(
        order__status__in=[1, 3], product__type_flow=5, oi_status=24)
    featured_orderitems = featured_orderitems.select_related('order')

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
                    "is_email_verified": 1,
                    "is_cell_phone_verified": 1
                })
                flag = FeatureProfileUpdate().update_feature_profile(
                    candidate_id=candidate_id, data=data)
                if flag:
                    # Send mail and sms with subject line as Your Profile updated
                    try:
                        mail_type = "FEATURED_UPDATE_MAIL"
                        to_emails = [obj.order.email]
                        data = {}
                        data.update({
                            "info": 'your profile updated',
                            "subject": 'your profile updated',
                            "name": obj.order.first_name + ' ' + obj.order.last_name,
                            "mobile": obj.order.mobile,
                        })
                        SendMail().send(to_emails, mail_type, data)
                        SendSMS().send(sms_type=mail_type, data=data)
                    except Exception as e:
                        print (str(e))

                    last_oi_status = obj.oi_status
                    obj.oi_status = 4
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

            except Exception as e:
                print (str(e))