from django.db import models

from seo.models import AbstractAutoDate
from geolocation.models import CURRENCY_SYMBOL

from .choices import STATUS_CHOICES, PAYMENT_MODE


class PaymentTxn(AbstractAutoDate):
    txn = models.CharField(max_length=255, null=True, blank=True)
    order = models.ForeignKey(
        'order.Order', related_name='ordertxns',
        verbose_name="Order",on_delete=models.CASCADE)
    cart = models.ForeignKey(
        'cart.Cart', verbose_name="Cart",
        null=True, blank=True,
        related_name='carttxns', on_delete=models.SET_NULL)
    status = models.PositiveSmallIntegerField(
        default=0, choices=STATUS_CHOICES)

    payment_mode = models.IntegerField(
        choices=PAYMENT_MODE, default=0)

    payment_date = models.DateTimeField(null=True, blank=True)

    currency = models.PositiveIntegerField(
        "Currency", choices=CURRENCY_SYMBOL, default=0)

    txn_amount = models.DecimalField(
        "Txn Amount", decimal_places=2, max_digits=12, default=0)

    # razor_order_id =  models.CharField(max_length=255, null=True, blank=True)
    #
    # razor_payment_id= models.CharField(max_length=255, null=True, blank=True)
    # razorpay_signature =  models.CharField(max_length=255, null=True, blank=True)

    # pay by cheque/Draft
    instrument_number = models.CharField(max_length=255, null=True, blank=True)
    instrument_issuer = models.CharField(max_length=255, null=True, blank=True)
    instrument_issue_date = models.CharField(
        max_length=255, null=True, blank=True)

    txn_info = models.TextField(
        "Transaction info")

    class Meta:
        app_label = 'payment'
        ordering = ('created', )

    def get_payment_mode(self):
        payment_mode_dict = dict(PAYMENT_MODE)
        return payment_mode_dict.get(self.payment_mode)

    def get_payment_status(self):
        status_dict = dict(STATUS_CHOICES)
        return status_dict.get(self.status)