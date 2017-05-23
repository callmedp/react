from django.contrib import admin

from .models import Cart, LineItem, ShippingDetail


class CartAdmin(admin.ModelAdmin):
	list_display = ['id', 'owner_id', 'owner_email', 'session_id', 'status']


class LineitemAdmin(admin.ModelAdmin):
	list_display = ['id', 'cart', 'parent', 'type_item', 'product', 'quantity',
		'reference', 'price_excl_tax', 'price_incl_tax']

admin.site.register(Cart, CartAdmin)
admin.site.register(LineItem, LineitemAdmin)
admin.site.register(ShippingDetail)