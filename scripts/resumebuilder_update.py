# python imports

import os
import django
import sys
from datetime import date, datetime, timedelta


import traceback

os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "careerplus.config.settings_staging")

ROOT_FOLDER = os.path.realpath(os.path.dirname(__file__))
ROOT_FOLDER = ROOT_FOLDER[:ROOT_FOLDER.rindex('/')]

if ROOT_FOLDER not in sys.path:
    sys.path.insert(1, ROOT_FOLDER + '/')

#  setup django
django.setup()

from resumebuilder.models import Candidate
from django.utils import timezone
from users.tasks import user_register
from order.models import OrderItem


def get_resume_builder_items():
    return OrderItem.objects.filter(
        order__status__in=[1, 3], product__type_flow__in=[17]).select_related('order')


def update_candidate_profile():
    order_items = get_resume_builder_items()
    import ipdb
    ipdb.set_trace()
    for oi in order_items:
        candidate_id = oi.order.candidate_id
        candidate = Candidate.objects.filter(candidate_id=candidate_id).first()
        if candidate:
            candidate.active_subscription = True
            try:
                candidate.save()
            except Exception as e:
                print(e)

    return


if __name__ == '__main__':
    update_candidate_profile()
