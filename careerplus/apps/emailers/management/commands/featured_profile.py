import logging
import datetime

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings
from django.db.models import Q

from order.utils import FeatureProfileUtil


class Command(BaseCommand):
    def handle(self, *args, **options):
        util = FeatureProfileUtil()
        util.start_all_feature()
        util.close_all_feature()
