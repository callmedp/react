# Create your models here.

from django.db import models
from django.conf import settings

from console.operations.functions import get_upload_path_order_item_operation
from order.models import Order, OrderItem
from django.utils.translation import ugettext_lazy as _

from console.operations.choices import OPERATION_TYPE,QUEUE_NAME


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


class CandidateAgentInteraction(models.Model):
    """
    Any exotel call operation thai are performed to any candidate
    """
    added_on = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified_on = models.DateTimeField(auto_now=True, null=True, blank=True)
    called_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,
                                    related_name='called_by')
    order = models.ForeignKey(Order, blank=True, null=True)

    queue_name = models.PositiveSmallIntegerField(
        choices=QUEUE_NAME, default=0)
    recording_url = models.TextField(_('Call Recording'), blank=True, null=True)
    candidate_id = models.CharField(null=True, blank=True, max_length=255, verbose_name=_("Customer ID"))
    connected = models.BooleanField(default=False, verbose_name=_("Is Call Connected"))
