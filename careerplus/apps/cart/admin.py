from django.contrib import admin
from .models import Cart, LineItem, Subscription


class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'owner_id', 'owner_email', 'session_id', 'status',
        'date_frozen', 'date_closed']
    list_filter = ('status', )

    search_fields = ('id', 'owner_id', 'owner_email', 'email', 'session_id')
    filter_horizontal = ()


class LineitemAdmin(admin.ModelAdmin):
    list_display = ['id', 'cart', 'parent', 'type_item', 'product', 'quantity',
        'reference', 'price_excl_tax', 'price_incl_tax',
        'no_process', 'parent_deleted']
    search_fields = ('id', 'reference', 'cart__owner_email', 'cart__owner_id')
    raw_id_fields = ('cart', 'parent', 'product')


admin.site.register(Cart, CartAdmin)
admin.site.register(LineItem, LineitemAdmin)
admin.site.register(Subscription)
