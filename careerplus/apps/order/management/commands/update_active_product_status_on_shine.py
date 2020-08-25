from django.core.management.base import BaseCommand
from order.models import OrderItem
from django.utils import timezone

class Command(BaseCommand):

    def handle(self, *args, **options):
        remove_inactive_products_from_scp()


def remove_inactive_products_from_scp():
    from emailers.utils import BadgingMixin
    """ removing the product whose end time is less than current time"""

    order_items = OrderItem.objects.filter(active_on_shine=1)

    for oi in order_items:
        if (oi.end_date and (oi.end_date > timezone.now())):
            try:
                active_services_details = BadgingMixin().get_active_services_or_courses_or_assessments(
                    candidate_id=oi.order.candidate_id, curr_order_item=oi, active=False)
                if active_services_details:
                    BadgingMixin().update_badging_data(
                        candidate_id=oi.order.candidate_id, data=active_services_details)
            except Exception as exc:
                logging.getLogger('error_log').error(
                    'could not update touch point data')

            try:
                oi.active_on_shine = 0
                oi.save()
            except Exception as e:
                logging.getLogger('error_log').error(
                    'could not able to update order Item {} whle inactivating products from shine', oi.id)
