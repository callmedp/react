# python imports
from decimal import Decimal

# django imports
from django.db.models import Sum
from django.core.cache import cache


def get_ltv(candidate_id):
    from order.models import Order,OrderItem,RefundRequest
    key = 'ltv_' + candidate_id
    ltv = cache.get(key)
    if ltv:
        return ltv
    ltv_pks = list(Order.objects.filter(candidate_id=candidate_id, status__in=[1, 2, 3]).values_list('pk', flat=True))
    ltv = Decimal(0)
    if ltv_pks:
        ltv_order_sum = Order.objects.filter(pk__in=ltv_pks).aggregate(ltv_price=Sum('total_incl_tax'))
        ltv = ltv_order_sum.get('ltv_price') if ltv_order_sum.get('ltv_price') else Decimal(0)
        rf_ois = list(OrderItem.objects.filter(order__in=ltv_pks, oi_status = 163).values_list('order', flat=True))
        rf_sum = RefundRequest.objects.filter(order__in=rf_ois).aggregate(rf_price=Sum('refund_amount'))
        if rf_sum.get('rf_price'):
            ltv = ltv - rf_sum.get('rf_price')
    cache.set(key, ltv, 2592000)
    return ltv