import logging

from celery.decorators import task

from django.contrib.auth import get_user_model
from django.conf import settings
from django.db import transaction

from order.models import Order

User = get_user_model()


@task(name="mock_welcomecall_assignment")
def mock_welcomecall_assignment(user=None):
    flag = False
    if user:
        try:
            user = User.objects.get(
                pk=user,
                groups__name__in=settings.WELCOMECALL_GROUP_LIST,
                is_active=True)
        except Exception as e:
            logging.getLogger('error_log').error("%s - %s" % ("No writer Found", str(e)))

        try:
            orders = Order.objects.filter(
                status=1, welcome_call_done=False,
                wc_cat=0, assigned_to=user)
            if not orders.exists():
                with transaction.atomic():
                    orders = Order.objects.select_for_update().filter(
                        status=1, welcome_call_done=False,
                        wc_cat=0, assigned_to=None)
                    if orders.exists():
                        order = orders[0]
                        order.assigned_to = user
                        order.save()
                        order.welcomecalloperation_set.create(
                            wc_cat=order.wc_cat,
                            wc_sub_cat=order.wc_cat,
                            wc_status=1,
                            assigned_to=order.assigned_to
                        )
                        flag = True
        except Exception as e:
            logging.getLogger('error_log').error("%s - %s" % ("mock welcomecall assigned", str(e)))
    return flag