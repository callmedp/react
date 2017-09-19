from django.contrib import admin

from .models import Order, OrderItem, OrderItemOperation, Message,\
    RefundRequest, RefundItem, RefundOperation, CouponOrder,\
    EmailOrderItemOperation, SmsOrderItemOperation

from wallet.models import WalletTransaction
from payment.models import PaymentTxn


class CouponOrderInline(admin.TabularInline):
    model = CouponOrder
    extra = 0


class WalletOrderInline(admin.TabularInline):
    model = WalletTransaction
    extra = 0


class TxnOrderInline(admin.TabularInline):
    model = PaymentTxn
    extra = 0
    

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'number', 'site', 'candidate_id', 'email',
        'status', 'date_placed']
    list_filter = ('status', )
    search_fields = ('number', 'id', 'candidate_id', 'email')
    inlines = [CouponOrderInline, WalletOrderInline, TxnOrderInline]


class OrderItemOperationInline(admin.TabularInline):
    model = OrderItemOperation
    readonly_fields = ('oi_resume', 'oi_draft', 'draft_counter', 'oi_status',
        'last_oi_status', 'assigned_to', 'added_by')
    ordering = ('-created',)


class OrderItemOperationAdmin(admin.ModelAdmin):
    list_display = ['created']
    ordering = ('-created',)

    extra = 0


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'parent', 'product', 'title', 'is_addon',
        'is_combo', 'no_process', 'is_variation', 'oi_status', 'draft_counter']
    inlines = [OrderItemOperationInline, ]

    list_filter = ('oi_status', 'partner')
    search_fields = ('order__number', 'id',
        'order__candidate_id', 'order__email', 'partner__name')


class RefundItemInline(admin.TabularInline):
    model = RefundItem
    readonly_fields = ('oi', 'type_refund', 'amount')

    extra = 0


class RefundOperationInline(admin.TabularInline):
    model = RefundOperation
    readonly_fields = ('status', 'last_status', 'message', 'document', 'added_by')
    ordering = ['created', ]

    extra = 0


class RefundRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'status', 'last_status',
        'refund_mode', 'currency', 'refund_amount',
        'txn_no', 'added_by']

    list_filter = ('status', 'last_status', 'refund_mode')
    search_fields = ('order__number', 'id',
        'order__candidate_id', 'order__email', 'txn_no')
    inlines = [RefundItemInline, RefundOperationInline]


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(OrderItemOperation, OrderItemOperationAdmin)
# admin.site.register(Message)
admin.site.register(RefundRequest, RefundRequestAdmin)
admin.site.register(EmailOrderItemOperation)
admin.site.register(SmsOrderItemOperation)