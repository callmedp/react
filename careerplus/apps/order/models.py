from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from seo.models import AbstractAutoDate
from .choices import STATUS_CHOICES, SITE_CHOICES,\
    PAYMENT_MODE, OI_OPS_STATUS


class Order(AbstractAutoDate):
    number = models.CharField(
        _("Order number"), max_length=128, db_index=True, unique=True)

    site = models.PositiveSmallIntegerField(default=0, choices=SITE_CHOICES)

    cart = models.ForeignKey(
        'cart.Cart', verbose_name=_("Cart"),
        null=True, blank=True, on_delete=models.SET_NULL)

    # custome information
    candidate_id = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        verbose_name=_("Customer ID"))

    txn = models.CharField(max_length=255, null=True, blank=True)

    # pay by cheque/Draft
    instrument_number = models.CharField(max_length=255, null=True, blank=True)
    instrument_issuer = models.CharField(max_length=255, null=True, blank=True)
    instrument_issue_date = models.CharField(
        max_length=255, null=True, blank=True)

    status = models.PositiveSmallIntegerField(default=0, choices=STATUS_CHOICES)

    payment_mode = models.IntegerField(choices=PAYMENT_MODE, default=0)
    payment_date = models.DateTimeField(null=True, blank=True)
    currency = models.CharField(
        _("Currency"), max_length=12, null=True, blank=True)

    total_incl_tax = models.DecimalField(
        _("Order total (inc. tax)"), decimal_places=2, max_digits=12, default=0)
    total_excl_tax = models.DecimalField(
        _("Order total (excl. tax)"), decimal_places=2, max_digits=12, default=0)

    date_placed = models.DateTimeField(db_index=True)
    closed_on = models.DateTimeField(null=True, blank=True)

    # shipping Address
    email = models.CharField(
        null=True,
        max_length=255,
        verbose_name=_("Customer Email"))

    first_name = models.CharField(
        max_length=255, null=True, blank=True, verbose_name=_("First Name"))

    last_name = models.CharField(
        max_length=255, null=True, blank=True, verbose_name=_("Last Name"))

    country_code = models.CharField(
        max_length=15, null=True, blank=True, verbose_name=_("Country Code"))

    mobile = models.CharField(max_length=15, null=True, blank=True,)

    address = models.CharField(max_length=255, null=True, blank=True)

    pincode = models.CharField(max_length=15, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)

    country = models.CharField(max_length=200, null=True, blank=True)

    # welcome call done or not
    welcome_call_done = models.BooleanField(default=False)

    class Meta:
        app_label = 'order'
        ordering = ['-date_placed']
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")
        permissions = (
            ("can_show_order_queue", "Can Show Order Queue"),
            ("can_show_welcome_queue", "Can Show Welcome Queue"),
            ("can_show_midout_queue", "Can Show Midout Queue"),
            ("can_show_all_order", "Can View All Orders"),
            ("can_show_paid_order", "Can View Paid Orders"),
        )

    def __str__(self):
        return u"#%s" % (self.number,)

    @property
    def get_status(self):
        statusD = dict(STATUS_CHOICES)
        return statusD.get(self.status)

    @property
    def get_payment_mode(self):
        payD = dict(PAYMENT_MODE)
        return payD.get(self.payment_mode)


class OrderItem(models.Model):
    order = models.ForeignKey(
        'order.Order', related_name='orderitems', verbose_name=_("Order"))

    parent = models.ForeignKey('self', null=True, blank=True)

    partner = models.ForeignKey(
        'partner.Vendor', related_name='order_items', blank=True, null=True,
        on_delete=models.SET_NULL, verbose_name=_("Partner"))
    partner_name = models.CharField(
        _("Partner name"), max_length=128, blank=True)
    product = models.ForeignKey(
        'shop.Product', on_delete=models.SET_NULL, blank=True, null=True,
        verbose_name=_("Product"))
    title = models.CharField(
        _("Product title"), max_length=255)
    upc = models.CharField(_("UPC"), max_length=128, blank=True, null=True)
    quantity = models.PositiveIntegerField(
        _("Quantity"), default=1)

    oi_price_incl_tax = models.DecimalField(
        _("Price (inc. tax)"), decimal_places=2, max_digits=12, default=0)
    oi_price_excl_tax = models.DecimalField(
        _("Price (excl. tax)"), decimal_places=2, max_digits=12, default=0)

    # Price information before discounts are applied
    oi_price_before_discounts_incl_tax = models.DecimalField(
        _("Price before discounts (inc. tax)"),
        decimal_places=2, max_digits=12, default=0)
    oi_price_before_discounts_excl_tax = models.DecimalField(
        _("Price before discounts (excl. tax)"),
        decimal_places=2, max_digits=12, default=0)

    # Normal site price for item (without discounts)
    unit_price_incl_tax = models.DecimalField(
        _("Unit Price (inc. tax)"), decimal_places=2, max_digits=12,
        blank=True, null=True)
    unit_price_excl_tax = models.DecimalField(
        _("Unit Price (excl. tax)"), decimal_places=2, max_digits=12,
        blank=True, null=True)

    no_process = models.BooleanField(default=False)
    is_combo = models.BooleanField(default=False)
    is_variation = models.BooleanField(default=False)

    # operation fields
    oi_status = models.PositiveIntegerField(
        _("Operation Status"), default=0, choices=OI_OPS_STATUS)
    last_oi_status = models.PositiveIntegerField(
        _("Last Operation Status"), default=0, choices=OI_OPS_STATUS)
    oi_resume = models.FileField(
        max_length=255, upload_to='oi_resume/',
        null=True, blank=True, default='')
    oi_draft = models.FileField(
        max_length=255, upload_to='oi_draft/', null=True, blank=True)
    draft_counter = models.PositiveIntegerField(default=0)

    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        related_name='oi_assigned',
        null=True, blank=True)

    assigned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        related_name='oi_assigned_by',
        null=True, blank=True)

    closed_on = models.DateTimeField(null=True, blank=True)
    midout_sent_on = models.DateTimeField(null=True, blank=True)
    draft_added_on = models.DateTimeField(null=True, blank=True)

    added_on = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_on = models.DateTimeField(null=True, blank=True)

    class Meta:
        app_label = 'order'
        # Enforce sorting in order of creation.
        ordering = ['pk']
        verbose_name = _("Order Item")
        verbose_name_plural = _("Order Items")
        permissions = (
            ("can_show_midout_queue", "Can Show Midout Queue"),
            ("can_show_inbox_queue", "Can Show Inbox Queue"),
            ("can_show_assigned_inbox", "Can Show Only Assigned Inbox"),
            ("can_show_unassigned_inbox", "Can Show Only Not Assigned Inbox"),
            ("writer_assignment_action", "Can Assign to Other writer"),
            ("can_assigned_to_writer", "Can Assigned To This Writer"),
            ("can_view_order_item_detail", "Can View Order Item Detail"),
        )

    def __str__(self):
        if self.product:
            title = self.product.title
        else:
            title = _('<missing product>')
        return _("Product '%(name)s', quantity '%(qty)s'") % {
            'name': title, 'qty': self.quantity}


class OrderItemOperation(AbstractAutoDate):
    oi = models.ForeignKey(OrderItem)
    oi_resume = models.FileField(
        max_length=255, upload_to='oio_resume/', null=True, blank=True)

    oi_draft = models.FileField(
        max_length=255, upload_to='oio_draft/', null=True, blank=True)
    draft_counter = models.PositiveIntegerField(default=0)
    oi_status = models.PositiveIntegerField(
        _("Operation Status"), default=0, choices=OI_OPS_STATUS)
    last_oi_status = models.PositiveIntegerField(
        _("Last Operation Status"), default=0, choices=OI_OPS_STATUS)

    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        related_name='oio_assigned',
        null=True, blank=True)

    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        related_name='oio_added_by',
        null=True, blank=True)


class Message(models.Model):
    oi = models.ForeignKey(OrderItem)

    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        related_name='message_added_by',
        null=True, blank=True)

    candidate_id = models.CharField(max_length=255, null=True, blank=False)

    message = models.TextField()

    is_internal = models.BooleanField(default=False)

    added_on = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified_on = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        ordering = ['added_on']
