from django.db import models
from django.conf import settings

from order.models import Order, OrderItem


class OrderItemOperations(models.Model):
	"""
    Any operation thats performed on a order item.
    """
    order_item = models.ForeignKey(OrderItem)
    operation_type = models.PositiveSmallIntegerField(
        choices=OPERATION_TYPE, default=0)
    rating = models.DecimalField(
        'Rating (Not greater than 5)', max_digits=2, decimal_places=1,
        null=True, blank=True)

    assigned_by = models.ForeignKey(User, null=True, blank=True)
    assigned_to = models.ForeignKey(User, null=True, blank=True,
                                    related_name='assigned_to')

    added_on = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified_on = models.DateTimeField(auto_now=True, null=True, blank=True)

    operation_changed_from = models.PositiveSmallIntegerField(
        choices=OPERATION_TYPE, default=0)