from django.contrib import admin

from .models import Cart, LineItem


class CartAdmin(admin.ModelAdmin):
	list_display = ['id', 'owner_id', 'owner_email', 'session_id', 'status']


class LineitemAdmin(admin.ModelAdmin):
	list_display = ['id', 'cart', 'parent', 'type_item', 'product', 'quantity', 'price_excl_tax', 'price_incl_tax']

admin.site.register(Cart, CartAdmin)
admin.site.register(LineItem, LineitemAdmin)