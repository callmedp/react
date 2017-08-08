from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from seo.models import AbstractAutoDate
from geolocation.models import Country
from linkedin.models import Draft

from .choices import STATUS_CHOICES, SITE_CHOICES,\
    PAYMENT_MODE, OI_OPS_STATUS, COUNSELLING_FORM_STATUS,\
    OI_USER_STATUS
from .functions import get_upload_path_order_invoice


class Order(AbstractAutoDate):
    number = models.CharField(
        _("Order number"), max_length=128, db_index=True, unique=True)

    site = models.PositiveSmallIntegerField(default=0, choices=SITE_CHOICES)

    cart = models.ForeignKey(
        'cart.Cart', verbose_name=_("Cart"),
        null=True, blank=True, on_delete=models.SET_NULL)

    # customer information
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
    midout_sent_on = models.DateTimeField(null=True, blank=True)

    # cash or Faild trasnsaction manual paid by..
    paid_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        related_name='order_paid_by',
        null=True, blank=True)

    # invoce order
    invoice = models.FileField(
        upload_to=get_upload_path_order_invoice, max_length=255,
        blank=True, null=True)

    class Meta:
        app_label = 'order'
        ordering = ['-date_placed']
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")
        permissions = (
            # order queue permission
            ("can_show_order_queue", "Can Show Order Queue"),
            ("can_show_all_order", "Can View All Orders"),
            ("can_show_paid_order", "Can View Only Paid Orders"),

            # welcome call permission
            ("can_show_welcome_queue", "Can Show Welcome Queue"),

            # order deatil permissions
            ("can_view_order_detail", "Can View Order Deatil"),

            # order Action permissions
            ("can_mark_order_as_paid", "Can Mark Order As Paid"),

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


class OrderItem(AbstractAutoDate):
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
    is_addon = models.BooleanField(default=False)

    #counselling form status
    counselling_form_status = models.PositiveSmallIntegerField(
        default=0, choices=COUNSELLING_FORM_STATUS)
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
    tat_date = models.DateTimeField(null=True, blank=True)

    oio_linkedin = models.OneToOneField(Draft, null=True, blank=True)

    waiting_for_input = models.BooleanField(default=False)

    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        related_name='oi_assigned',
        null=True, blank=True)

    assigned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        related_name='oi_assigned_by',
        null=True, blank=True)

    closed_on = models.DateTimeField(null=True, blank=True)
    draft_added_on = models.DateTimeField(null=True, blank=True)
    approved_on = models.DateTimeField(null=True, blank=True)  # draft approved on

    user_feedback = models.BooleanField(default=False)

    class Meta:
        app_label = 'order'
        # Enforce sorting in order of creation.
        ordering = ['pk']
        verbose_name = _("Order Item")
        verbose_name_plural = _("Order Items")
        permissions = (
            # midout queue permission
            ("can_show_midout_queue", "Can Show Midout Queue"),
            ("can_upload_candidate_resume", "Can Upload Candidate resume"),

            # inbox permission
            ("can_show_inbox_queue", "Can Show Writer Inbox Queue"),
            ("can_view_extra_field_inbox", "Can View Extra Fields Of Writer Inbox"),
            ("writer_inbox_assigner", "Writer Inbox Assigner"),
            ("writer_inbox_assignee", "Writer Inbox Assignee"),

            # oirder item detail permission
            ("can_view_order_item_detail", "Can View Order Item Detail"),

            # for linkedin flow
            ("writer_assignment_linkedin_action", "Can Assign to Other linkedin writer"),
            ("can_assigned_to_linkedin_writer", "Can Assigned To This linkedin Writer"),
            ("can_show_linkedinrejectedbyadmin_queue", "Can View Linkedin Rejected By Admin Queue"),
            ("can_show_linkedinrejectedbycandidate_queue", "Can View LinkedinRejected By Candidate Queue"),
            ("can_show_linkedin_approval_queue", "Can View Linkedin Approval Queue"),
            ("can_show_linkedin_inbox_queue", "Can View Linkedin Inbox Queue"),
            ("can_show_linkedin_writer_draft", "Can View Linkedin Writer Draft"),

            # Approval Queue
            ("can_show_approval_queue", "Can View Approval Queue"),
            ("can_view_all_approval_list", "Can View All Approval List"),
            ("can_view_only_assigned_approval_list", "Can View Only Assigned Approval List"),
            ("can_approve_or_reject_draft", "Can Approve Or Reject Draft"),

            # Appoved Queue
            ("can_show_approved_queue", "Can View Approved Queue"),
            ("can_view_all_approved_list", "Can View All Approved List"),
            ("can_view_only_assigned_approved_list", "Can View Only Assigned Approved List"),

            # Rejected By Admin Queue
            ("can_show_rejectedbyadmin_queue", "Can View Rejected By Admin Queue"),
            ("can_view_all_rejectedbyadmin_list", "Can View All Rejected by Admin List"),
            ("can_view_only_assigned_rejectedbyadmin_list", "Can View Only Assigned Rejected By Admin List"),

            # Rejected By Candidate Queue
            ("can_show_rejectedbycandidate_queue", "Can View Rejected By Candidate Queue"),
            ("can_view_all_rejectedbycandidate_list", "Can View All Rejected By Candidate List"),
            ("can_view_only_assigned_rejectedbycandidate_list", "Can View Only Assigned Rejected By Candidate List"),

            # Allocated Queue
            ("can_show_allocated_queue", "Can Show Allocated Queue"),
            ("can_view_all_allocated_list", "Can View All Allocated List"),
            ("can_view_only_assigned_allocated_list", "Can View Only Assigned Allocated List"),

            # Booster Queue
            ("can_show_booster_queue", "Can Show Booster Queue"),

            # Domestic Profile Update Queue Permissions
            ("can_show_domestic_profile_update_queue", "Can Show Domestic Profile Update Queue"),
            ("domestic_profile_update_assigner", "Domestic Profile Update Assigner"),
            ("domestic_profile_update_assignee", "Domestic Profile Update Assignee"),

            # Domestic Profile Approval Queue Permissions
            ("can_show_domestic_profile_approval_queue", "Can Show Domestic Profile Approval Queue"),

            # International Profile Update Queue Permissions
            ("can_show_international_profile_update_queue", "Can Show International Profile Update Queue"),
            ("international_profile_update_assigner", "International Profile Update Assigner"),
            ("international_profile_update_assignee", "International Profile Update Assignee"),

            # International Profile Approval Queue Permissions
            ("can_show_international_profile_approval_queue", "Can Show International Profile Approval Queue"),

            # Closed Permission
            ("can_show_closed_oi_queue", "Can Show Closed Orderitem Queue"),
            ("can_view_all_closed_oi_list", "Can View All Closed Orderitem List"),
            ("can_view_only_assigned_closed_oi_list", "Can View Only Assigned Closed Orderitem List"),

            # partner inbox permission
            ("can_show_partner_inbox_queue", "Can Show Partner Inbox Queue"),
            ("show_test_status_fields", "Show Test Status Field For Studymate"),

            # Hold queue permissions
            ("can_show_hold_orderitem_queue", "Can Show Hold Orderitem Queue"),

            # Varification report queue
            ("can_show_varification_report_queue", "Can Show Varification Report Queue"),

            # Action Permission
            ("oi_action_permission", "OrderItem Action Permission"),
            ("oi_export_as_csv_permission", "Order Item Export As CSV Permission"),
        )

    def __str__(self):
        if self.product:
            title = self.product.title
        else:
            title = _('<missing product>')
        return _("Product '%(name)s', quantity '%(qty)s'") % {
            'name': title, 'qty': self.quantity}

    @property
    def get_oi_status(self):
        dict_status = dict(OI_OPS_STATUS)
        return dict_status.get(self.oi_status)

    @property
    def get_user_oi_status(self):
        dict_status = dict(OI_USER_STATUS)
        return dict_status.get(self.oi_status)

    def get_oi_communications(self):
        communications = self.message_set.all().select_related('added_by')
        return list(communications)

    def get_oi_operations(self):
        operations = self.orderitemoperation_set.all().select_related(
            'added_by', 'assigned_to')
        return list(operations)

    def get_oi_drafts(self):
        max_limit_draft = settings.DRAFT_MAX_LIMIT
        drafts = self.orderitemoperation_set.filter(
            draft_counter__range=[1, max_limit_draft])
        return list(drafts)

    def get_draft_level(self):
        if self.draft_counter == settings.DRAFT_MAX_LIMIT:
            return 'Final Draft'
        elif self.draft_counter:
            return 'Draft %s' % (self.draft_counter)
        return ''

    def get_roundone_status(self):
        if self.oi_status == 142:
            pass
        elif self.oi_status not in [141, 142, 143]:
            pass
        dict_status = dict(OI_USER_STATUS)
        return dict_status.get(self.oi_status)

    def get_test_obj(self):
        return self


class OrderItemOperation(AbstractAutoDate):
    oi = models.ForeignKey(OrderItem)
    linkedin = models.ForeignKey(Draft, null=True, blank=True)
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

    class Meta:
        ordering = ['created']

    @property
    def get_oi_status(self):
        dict_status = dict(OI_OPS_STATUS)
        return dict_status.get(self.oi_status)

    @property
    def get_user_oi_status(self):
        dict_status = dict(OI_USER_STATUS)
        return dict_status.get(self.oi_status)


class Message(AbstractAutoDate):
    oi = models.ForeignKey(OrderItem)

    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        related_name='message_added_by',
        null=True, blank=True)

    candidate_id = models.CharField(max_length=255, null=True, blank=False)

    message = models.TextField()

    is_internal = models.BooleanField(default=False)

    class Meta:
        ordering = ['created']


class InternationalProfileCredential(AbstractAutoDate):
    oi = models.ForeignKey(OrderItem)
    country =  models.ForeignKey(Country)
    username = models.CharField(_('Username'), max_length=100)
    password = models.CharField(_('Password'), max_length=100)
    candidateid = models.CharField(_('CandidateId'), max_length=100)
    candidate_email = models.CharField(_('Candidate Email'), max_length=100)
    site_url = models.CharField(_('Site Url'), max_length=100, blank=True)
    profile_status = models.BooleanField(default=False)

    def __str__(self):
        return self.username

