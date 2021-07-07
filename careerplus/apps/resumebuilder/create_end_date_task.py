# from order.models import OrderItem
# from resumebuilder.models import Candidate
# import datetime
# from django.utils import timezone

# orderitems = OrderItem.objects.filter(order__status__in=[1, 3], product__type_flow__in=[17], oi_status__in=[0], product__sub_type_flow__in=[1701]).select_related('order')

# for oi in orderitems:
#     if oi.start_date is not None and oi.end_date is None:
#         oi.end_date = oi.start_date + datetime.timedelta(days=oi.product.day_duration)
#         oi.save()
#         #print(oi.start_date, oi.end_date, oi.product, oi.product.day_duration)
        
#         candidate = Candidate.objects.filter(candidate_id=oi.order.candidate_id).first()
#         if candidate:
#             #print(oi.start_date, oi.end_date, timezone.now(), oi.product.day_duration, candidate.active_subscription)
#             if oi.end_date < timezone.now():
#                 candidate.active_subscription = False
#                 #print(oi.start_date, oi.end_date, oi.product, oi.product.day_duration, candidate.active_subscription)
#                 candidate.save()


