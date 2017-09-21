from decimal import Decimal
from django.utils import timezone
from django.db import models
from django.utils.translation import ugettext_lazy as _
from cart.models import Cart
from order.models import Order
from seo.models import AbstractAutoDate

STATUS_REWARD = (
    (0, "Default"),
    (1, "Active- Can be used"),
    (2, "Exhausted - In Transaction"),
    (3, "Expired- Expired"),
    (4, "InActive- Can't be Used"),
    (5, "Archive - Points need to be archived"),
)

STATUS_CASH = (
    (0, "Default"),
    (1, "Active - Can be used"),
    (2, "Exhausted - In Transaction"),
    (3, "InActive - Can't be used"),
    (4, "Archive - Points need to be archived"),
)

TXN_TYPE = (
    (0, "Default"),
    (1, "Added"),
    (2, "Redeemed"),
    (3, "Refund"),
    (4, "Expired"),
    (5, "Reverted"),
)


class Wallet(AbstractAutoDate):
    owner = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=_("Owner ID"))
    owner_email = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Owner Email"))

    class Meta:
        verbose_name = _('Wallet')
        verbose_name_plural = _('Wallets')
        ordering = ("-modified", "-created")

    def __str__(self):
        return self.owner

    def get_current_amount(self):
        points = self.point.filter(status=1)
        total = Decimal(0)
        for pts in points:
            if pts.expiry >= timezone.now():
                total += pts.current
        return total

        
class RewardPoint(AbstractAutoDate):
    wallet = models.ForeignKey(
        Wallet,
        verbose_name=_('wallet'),
        related_name='point',
        on_delete=models.CASCADE)
    original = models.DecimalField(
        _('Original'), decimal_places=2, max_digits=12,
        null=True)
    current = models.DecimalField(
        _('Current'), decimal_places=2, max_digits=12,
        null=True)
    expiry = models.DateTimeField(
        _("Expiry"), null=True, blank=True)
    last_used = models.DateTimeField(
        _("Last Used"), null=True, blank=True)
    status = models.PositiveSmallIntegerField(
        _("Status"),
        default=0, choices=STATUS_REWARD)
    txn = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Transaction"))
    cw_id = models.IntegerField(
        _('CP Credits'),
        blank=True,
        null=True,
        editable=False)
    

    class Meta:
        verbose_name = _('Reward Point')
        verbose_name_plural = _('Reward Points')
        ordering = ("-modified", "-created")

    def __str__(self):
        return self.wallet.owner + ' - ' + str(self.pk)


class ECash(AbstractAutoDate):
    wallet = models.ForeignKey(
        Wallet,
        verbose_name=_('wallet'),
        related_name='ecash',
        on_delete=models.CASCADE)
    original = models.DecimalField(
        _('Original'), decimal_places=2, max_digits=12,
        null=True)
    current = models.DecimalField(
        _('Current'), decimal_places=2, max_digits=12,
        null=True)
    last_used = models.DateTimeField(
        _("Last Used"), null=True, blank=True)
    status = models.PositiveSmallIntegerField(
        _("Status"),
        default=0, choices=STATUS_CASH)
    txn = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Transaction"))

    class Meta:
        verbose_name = _('E-Cash')
        verbose_name_plural = _('E-Cashs')
        ordering = ("-modified", "-created")

    def __str__(self):
        return self.wallet.owner + ' - ' + str(self.pk)


class WalletTransaction(AbstractAutoDate):
    wallet = models.ForeignKey(
        Wallet,
        verbose_name=_('wallet'),
        related_name='wallettxn',
        on_delete=models.CASCADE)
    txn_type = models.PositiveSmallIntegerField(
        _("Type"),
        default=0, choices=TXN_TYPE)
    status = models.PositiveSmallIntegerField(
        _("status"),
        default=0, choices=(
            (0, "Working"),
            (1, "Success"),
            (2, "Failure")))
    notes = models.TextField(
        verbose_name=_('Description'), blank=True, default='')
    order = models.ForeignKey(
        Order,
        verbose_name=_('Order'),
        null=True,
        related_name='wallettxn',
        on_delete=models.SET_NULL)
    cart = models.ForeignKey(
        Cart,
        verbose_name=_('Cart'),
        null=True,
        related_name='wallettxn',
        on_delete=models.SET_NULL)
    txn = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Transaction"))
    point_txn = models.ManyToManyField(
        RewardPoint,
        verbose_name=_('Point'),
        through='PointTransaction',
        through_fields=('transaction', 'point'),
        blank=True)
    ecash_txn = models.ManyToManyField(
        ECash,
        verbose_name=_('ECash'),
        through='ECashTransaction',
        through_fields=('transaction', 'ecash'),
        blank=True)
    point_value = models.DecimalField(
        _('Point Value'), decimal_places=2, max_digits=12,
        null=True)
    ecash_value = models.DecimalField(
        _('Cash Value'), decimal_places=2, max_digits=12,
        null=True)

    current_value = models.DecimalField(
        _('Current Value'), decimal_places=2, max_digits=12,
        null=True)

    class Meta:
        verbose_name = _('Wallet Transaction')
        verbose_name_plural = _('Wallet Transactions')
        ordering = ("-modified", "-created")

    def __str__(self):
        return self.wallet.owner + ' - ' + str(self.pk)

    def added_point_expiry(self):
        pointtxns = self.usedpoint.all()
        if pointtxns.exists():
            return pointtxns[0].point.expiry.date()
        return ''

    def get_txn_type(self):
        txn_type_dict = dict(TXN_TYPE)
        return txn_type_dict.get(self.txn_type)
   

class PointTransaction(AbstractAutoDate):
    point = models.ForeignKey(
        RewardPoint,
        related_name='wallettxn',
        on_delete=models.CASCADE)
    transaction = models.ForeignKey(
        WalletTransaction,
        related_name='usedpoint',
        on_delete=models.CASCADE)
    point_value = models.DecimalField(
        _('Point Value'), decimal_places=2, max_digits=12,
        null=True)
    txn_type = models.PositiveSmallIntegerField(
        _("Type"),
        default=0, choices=TXN_TYPE)
    
    def __str__(self):
        return _("%(pt)s to '%(txn)s'") % {
            'pt': self.point,
            'txn': self.transaction}
    
    class Meta:
        unique_together = ('point', 'transaction')
        verbose_name = _('Point Transaction')
        verbose_name_plural = _('Point Transactions')


class ECashTransaction(AbstractAutoDate):
    ecash = models.ForeignKey(
        ECash,
        related_name='wallettxn',
        on_delete=models.CASCADE)
    transaction = models.ForeignKey(
        WalletTransaction,
        related_name='usedcash',
        on_delete=models.CASCADE)
    ecash_value = models.DecimalField(
        _('ECash Value'), decimal_places=2, max_digits=12,
        null=True)
    txn_type = models.PositiveSmallIntegerField(
        _("Type"),
        default=0, choices=TXN_TYPE)
    
    def __str__(self):
        return _("%(cash)s to '%(txn)s'") % {
            'cash': self.ecash,
            'txn': self.transaction}
    
    class Meta:
        unique_together = ('ecash', 'transaction')
        verbose_name = _('ECash Transaction')
        verbose_name_plural = _('ECash Transactions')
