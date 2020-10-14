from __future__ import absolute_import
# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from shinecpcrm.config.celery import app as celery_app  # noqa

from ajax.views import *
from order.models import *


import csv

fieldnames = ['Candidate_id', 'Email', 'Products', 'LTV']

from core.library.gcloud.custom_cloud_storage import *

upload = GCPPrivateMediaStorage().open('adhoc/ltv_data3.csv', 'wb')

csvwriter = csv.DictWriter(
     upload, delimiter=',',
     fieldnames=fieldnames)

csvwriter.writerow(dict((fn, fn) for fn in fieldnames))

orders = Order.objects.filter(payment_date__gt=datetime.datetime(2017,11,1))


for i, order in enumerate(orders):
    try:
        candidate_id = order.candidate_id
        selected, ltv = get_ltv(candidate_id)
        if selected:
            candidate_orders = Order.objects.filter(status__gt=0, candidate_id=candidate_id)
            products = []
            for order_c in candidate_orders:
                products.append(order_c.orderitems.all().values_list('product__heading'))
            row = {'Candidate_id': candidate_id, 'Email': order.email}
            row.update({'Products': products, 'LTV': ltv})
            csvwriter.writerow(row)
            print(i, order.id, candidate_id, "LTV")
        else:
            print(i, order.id, candidate_id, "no LTV")
            csvwriter.writerow({'Candidate_id': candidate_id, 'Email': order.email, 'Products': None, 'LTV': ltv})
    except Exception as e:
        print(order.id, str(e))
        csvwriter.writerow({'Candidate_id': candidate_id, 'Email': order.email, 'Products': None, 'LTV': "Exception"})
upload.close()
