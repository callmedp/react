from django.contrib import admin

from .models import Order, OrderItem, OrderItemOperation, Message,\
    RefundRequest, RefundItem, RefundOperation, CouponOrder,\
    EmailOrderItemOperation, SmsOrderItemOperation,\
    InternationalProfileCredential, GazettedHoliday

from wallet.models import WalletTransaction
from payment.models import PaymentTxn

class CouponOrderInline(admin.TabularInline):
    model = CouponOrder
    extra = 0
    fields = ('coupon',)
    raw_id_fields = ('coupon',)


class WalletOrderInline(admin.TabularInline):
    model = WalletTransaction
    extra = 0
    fields = ('wallet', 'cart',)
    raw_id_fields = ('wallet', 'cart',)


class TxnOrderInline(admin.TabularInline):
    model = PaymentTxn
    fields = ('cart',)
    raw_id_fields = ('cart',)
    extra = 0


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    fields = ('parent', 'partner', 'product', 'delivery_service',
        'assigned_to', 'assigned_by',)
    raw_id_fields = ('parent', 'partner', 'product', 'delivery_service',
        'assigned_to', 'assigned_by',)
    extra = 0

class GazettedHolidaysAdmin(admin.ModelAdmin):
    list_display = ['holiday_date', 'holiday_type']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'number', 'site', 'candidate_id', 'email',
        'status', 'date_placed', 'payment_date']
    list_filter = ('status', 'site')
    raw_id_fields = ('country',)
    search_fields = ('number', 'id', 'candidate_id', 'email')
    inlines = [OrderItemInline, TxnOrderInline, CouponOrderInline, WalletOrderInline]


class OrderItemOperationInline(admin.TabularInline):
    model = OrderItemOperation
    fields = ('oi_resume', 'oi_draft', 'draft_counter', 'oi_status',
        'last_oi_status', 'assigned_to', 'added_by')
    readonly_fields = ('oi_resume', 'oi_draft', 'draft_counter', 'oi_status',
        'last_oi_status', 'assigned_to', 'added_by')
    raw_id_fields = ('oi',)
    ordering = ('-created',)
    extra = 0


class OrderItemOperationAdmin(admin.ModelAdmin):
    list_display = ['created']
    ordering = ('-created',)
    raw_id_fields = ('oi',)
    extra = 0


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'parent', 'product', 'title', 'is_addon',
        'is_combo', 'no_process', 'is_variation', 'oi_status', 'draft_counter']
    inlines = [OrderItemOperationInline, ]
    raw_id_fields = ('order', 'parent', 'product', 'partner', 'oio_linkedin')

    list_filter = ('oi_status', 'partner', 'product__type_flow')
    search_fields = ('order__number', 'id',
        'order__candidate_id', 'order__email', 'partner__name', 'product__name')


class RefundItemInline(admin.TabularInline):
    model = RefundItem
    readonly_fields = ('oi', 'type_refund', 'amount')

    extra = 0


class RefundOperationInline(admin.TabularInline):
    model = RefundOperation
    readonly_fields = ('status', 'last_status', 'message', 'document', 'added_by')
    ordering = ['created', ]

    extra = 0


class MessageAdmin(admin.ModelAdmin):
    model = Message
    raw_id_fields = ('oi', 'oio')


class RefundRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'status', 'last_status',
        'refund_mode', 'currency', 'refund_amount',
        'txn_no', 'added_by']

    list_filter = ('status', 'last_status', 'refund_mode')
    search_fields = ('order__number', 'id',
        'order__candidate_id', 'order__email', 'txn_no')
    inlines = [RefundItemInline, RefundOperationInline]


class InternationalProfileCredentialAdmin(admin.ModelAdmin):
    list_display = ['username', 'password', 'profile_status']
    extra = 0
    raw_id_fields = ('oi', 'country')


class EmailOrderItemOperationAdmin(admin.ModelAdmin):
    list_display = ['oi', 'email_oi_status', 'draft_counter', 'to_email', 'status']
    raw_id_fields = ('oi', )
    search_fields = ('oi__id', 'to_email')


class SmsOrderItemOperationAdmin(admin.ModelAdmin):
    list_display = ['oi', 'sms_oi_status', 'draft_counter', 'to_mobile', 'status']
    raw_id_fields = ('oi', )
    search_fields = ('oi__id', 'to_mobile')

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(OrderItemOperation, OrderItemOperationAdmin)
admin.site.register(RefundRequest, RefundRequestAdmin)
admin.site.register(EmailOrderItemOperation, EmailOrderItemOperationAdmin)
admin.site.register(SmsOrderItemOperation, SmsOrderItemOperationAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(
    InternationalProfileCredential,
    InternationalProfileCredentialAdmin
)
admin.site.register(GazettedHoliday ,GazettedHolidaysAdmin)
