import logging
import datetime

from django.core.management.base import BaseCommand

from resumebuilder.utils import SubscriptionUtil


class Command(BaseCommand):
    def handle(self, *args, **options):
        util = SubscriptionUtil()
        util.assign_end_date()
        util.close_subscription()
