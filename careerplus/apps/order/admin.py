from django.contrib import admin

from .models import Order, OrderItem, OrderItemOperation, Message, CouponOrder
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


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'partner',
        'partner_name', 'parent', 'product', 'title', 'upc',
        'is_combo', 'no_process', 'is_variation', 'oi_status']
    inlines = [OrderItemOperationInline, ]

    list_filter = ('oi_status', 'partner')
    search_fields = ('order__number', 'id',
        'order__candidate_id', 'order__email', 'partner__name')


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(OrderItemOperation, OrderItemOperationAdmin)
admin.site.register(Message)