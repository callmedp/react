# Python Core Imports
from django.conf import settings
from django.utils import timezone
from celery.result import AsyncResult
import logging
import json

# Inter App Import
from order.models import OrderItem


def update_celery_status():
    try:
        obj_sucess_count = 0
        orderitem_obj = OrderItem.objects.select_related('order', 'product'). \
            filter(product__type_flow__in=[17], product__sub_type_flow__in=[1701],
                   order__status__in=[1, 2], end_date__gte=timezone.now())

        for oi in orderitem_obj:
            task_obj = oi.message_set.filter(is_internal=True, candidate_id='celery_task')

            if task_obj.count() <= 0:
                # No task is pending, assume the task is completed
                pass
            else:
                task_json = json.loads(task_obj.first().message)
                task_id = task_json.get('task_id', None)
                task_status = task_json.get('status')

                if task_status == 'PENDING':
                    async_result = AsyncResult(task_id)
                    if async_result.status == 'PENDING':
                        pass
                    elif async_result.status == 'SUCCESS':
                        task_obj.first().delete()
                        obj_sucess_count += 1
                    else:
                        logging.getLogger('error_log').error('Task updating celery broke, reason -> {}'.
                                                             format(str(async_result.info)))
                        pass

        logging.getLogger('info_log').info(
            'Completed CELERY STATUS BUILDER, FOUND -> {} AND COMPLETED -> {}'.format(
                str(orderitem_obj.count()), str(obj_sucess_count)))

        print('Completed CELERY STATUS BUILDER, FOUND -> {} AND COMPLETED -> {}'.format(
            str(orderitem_obj.count()), str(obj_sucess_count)))

    except Exception as e:
        logging.getLogger('error_log').error('Failed to run Update Builder status, error => {}'.format(str(e)))


if __name__ == '__main__':
    update_celery_status()
