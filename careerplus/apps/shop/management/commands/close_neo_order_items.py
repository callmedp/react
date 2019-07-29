import json
import logging
import time

from django.conf import settings
from django.utils import timezone

from django.core.management.base import BaseCommand
from shop.api.v1.tasks import update_practice_test_info
from core.api_mixin import NeoApiMixin
from order.models import OrderItem
from shop.models import PracticeTestInfo
class Command(BaseCommand):
    """
        Custom command to Update Crm Products.
    """
    help = 'Update Products CRM'

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def handle(self, *args, **options):
        emails = list(PracticeTestInfo.objects.filter(is_boarded=False).values_list('email', flat=True))
        order_item = OrderItem.objects.filter(
            product__vendor__slug='neo',
            order__status__in=[1, 3],
            order__email__in=emails
        )
        neo_closing_count = 0
        for oi in order_item:
            email = oi.order.email
            test_info = PracticeTestInfo.objects.filter(email=email).exclude(order_item=None).first()
            if test_info:
                status = NeoApiMixin().get_student_status_on_neo(email=test_info.email)
                if status == 'onboard':
                    test_info.is_boarded = True
                    if not test_info.test_data:
                        json_rep = NeoApiMixin().get_pt_result(email=email)
                        if json_rep:
                            setattr(test_info, 'test_data', str(json_rep))
                    test_info.save()
                    last_oi_status = oi.oi_status
                    oi.oi_status = 4
                    oi.closed_on = timezone.now()
                    oi.orderitemoperation_set.create(
                        oi_status=33,
                        last_oi_status=last_oi_status,
                        assigned_to=oi.assigned_to
                    )
                    oi.orderitemoperation_set.create(
                        oi_status=4,
                        last_oi_status=33,
                        assigned_to=oi.assigned_to
                    )
                    neo_closing_count += 1

        logging.getLogger('info_log').error(
            "{} orders of neo has been closed".format(str(neo_closing_count))
        )
