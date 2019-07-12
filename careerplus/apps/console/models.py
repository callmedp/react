# Create your models here.

from django.db import models
from django.conf import settings

from console.operations.functions import get_upload_path_order_item_operation
from order.models import Order, OrderItem

from console.operations.choices import OPERATION_TYPE


class OrderItemOperations(models.Model):
    """
    Any operation thats performed on a order item.
    """
    order_item = models.ForeignKey(OrderItem)
    operation_type = models.PositiveSmallIntegerField(
        choices=OPERATION_TYPE, default=0)
    assigned_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,
                                    related_name='assigned_to')

    added_on = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified_on = models.DateTimeField(auto_now=True, null=True, blank=True)

    operation_changed_from = models.PositiveSmallIntegerField(
        choices=OPERATION_TYPE, default=0)
    uploaded_document = models.FileField(upload_to=get_upload_path_order_item_operation)



