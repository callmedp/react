# Python Core Imports
import time
from datetime import date
import logging
import requests

# Django Core Imports
from django.conf import settings
from django.utils import timezone

# Inter App Import
from order.models import OrderItem


def update_bgv_process():
    command = "update_bgv_process"

    try:
        orderitems = OrderItem.objects.select_related('order', 'product') \
            .filter(oi_status__in=[165])

        for oi in orderitems:
            if oi.product.type_flow == 20:

                report_value = oi.message_set.filter(is_internal=True).first().message
                verification_url = settings.HIRESURE_REPORT_URL.format(report_id=report_value)
                response = requests.get(verification_url)
                rresponse = response.json()
                if response.status_code == 200:
                    report_status = rresponse[0]['bgv_report']['report']

                    if report_status == 'IN_PROGRESS':
                        pass

                    elif report_status == 'COMPLETED':
                        order = oi.order
                        last_oi_status = oi.oi_status
                        oi.oi_status = 166
                        oi.last_oi_status = last_oi_status
                        oi.closed_on = timezone.now()
                        oi.save()
                        order.status = 3
                        order.save()
                        oi.orderitemoperation_set.create(
                            oi_status=oi.oi_status,
                            last_oi_status=last_oi_status
                        )
                        oi.message_set.create(message=response.json(), candidate_id=oi.order.candidate_id,
                                              is_internal=True)
                else:
                    logging.getLogger('error_log').error(
                        'Failed BGV report status_code => {} of URL =>'.format(str(response.status_code),
                                                                               verification_url))

        logging.getLogger('info_log').info(
            'Completed BGV report of date -> {} and Found Total Item -> {}'.format(str(date.today()),
                                                                                   str(orderitems.count())))
        print('Completed BGV report of date -> {} and Found Total Item -> {}'.format(str(date.today()),
                                                                                     str(orderitems.count())))

    except Exception as e:
        logging.getLogger('error_log').error('Failed to run BGV process, error => {}'.format(str(e)))


if __name__ == '__main__':
    update_bgv_process()
