from django.core.management.base import BaseCommand

from emailers.cashbackmailers import get_eligible_orders,\
    get_eligible_orders_3lastdays, get_eligible_orders_lastdays


class Command(BaseCommand):
    def handle(self, *args, **options):
        get_eligible_orders()
        get_eligible_orders_3lastdays()
        get_eligible_orders_lastdays()
