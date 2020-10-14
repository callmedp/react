from django.contrib import admin

from .models import PaymentTxn


class PaymentTxnAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'txn', 'status', 'payment_mode',
        'payment_date', 'currency', 'instrument_number', 'instrument_issuer',
        'instrument_issue_date', 'created']
    list_filter = ('status', 'payment_mode', 'currency')
    search_fields = ('id', 'txn', 'instrument_number')
    raw_id_fields = ('order', 'cart')

admin.site.register(PaymentTxn, PaymentTxnAdmin)