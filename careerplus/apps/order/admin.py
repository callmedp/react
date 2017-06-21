from django.contrib import admin

from .models import Order, OrderItem, OrderItemOperation


class OrderAdmin(admin.ModelAdmin):
	list_display = ['id', 'number', 'site', 'cart', 'candidate_id', 'email',
		'status', 'date_placed']


class OrderItemOperationInline(admin.TabularInline):
	model = OrderItemOperation
	readonly_fields = ('oi_resume', 'oi_draft', 'draft_counter', 'oi_status', 'last_oi_status', 'assigned_to', 'added_by')
	ordering = ('-created',)


class OrderItemOperationAdmin(admin.ModelAdmin):
	list_display = ['created']
	ordering = ('-created',)


class OrderItemAdmin(admin.ModelAdmin):
	list_display = ['id', 'order', 'partner', 'partner_name', 'parent', 'product', 'title', 'upc', 'is_combo', 'no_process', 'is_variation']
	inlines = [OrderItemOperationInline, ]


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(OrderItemOperation, OrderItemOperationAdmin)