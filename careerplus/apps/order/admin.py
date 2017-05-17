from django.contrib import admin

from .models import Order, OrderItem


class OrderAdmin(admin.ModelAdmin):
	list_display = ['id', 'number', 'site', 'cart', 'candidate_id', 'email',
		'status', 'date_placed']


class OrderItemAdmin(admin.ModelAdmin):
	list_display = ['id', 'order', 'partner', 'partner_name', 'product', 'title', 'upc']


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)