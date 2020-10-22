from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import Wallet, RewardPoint, ECash, WalletTransaction, ECashTransaction, PointTransaction


class RewardPointInline(admin.TabularInline):
    model = RewardPoint
    readonly_fields = ['modified']
    extra = 0

# class ECashInline(admin.TabularInline):
#     model = ECash
#     readonly_fields = ['modified']
#     extra = 0

# class ECashTxnInline(admin.TabularInline):
#     model = ECashTransaction
#     readonly_fields = ['modified']
#     fk_name = 'transaction'
#     raw_id_fields = ['ecash', 'transaction']
#     extra = 0

class PointTxnInline(admin.TabularInline):
    model = PointTransaction
    readonly_fields = ['modified']
    fk_name = 'transaction'
    raw_id_fields = ['point', 'transaction']
    extra = 0



class WalletTransactionAdmin(admin.ModelAdmin):
    model = WalletTransaction
    raw_id_fields = ('wallet', 'order', 'cart',)
    readonly_fields = ['modified']
    inlines = [PointTxnInline]
    
class WalletTransactionInline(admin.StackedInline):
    model = WalletTransaction
    raw_id_fields = ('order', 'cart',)
    readonly_fields = ['modified']
    fk_name = 'wallet'
    extra = 0

class WalletAdmin(admin.ModelAdmin):
    list_display = [
        'pk','owner', 'owner_email', 'current_balance']
    readonly_fields = ['owner', 'owner_email', 'current_balance']
    search_fields = ('owner', 'owner_email')
    inlines = (RewardPointInline, WalletTransactionInline)
    
    def current_balance(self, obj):
        return obj.get_current_amount()
    current_balance.short_description = _("Balance")

# Register your models here.
admin.site.register(Wallet, WalletAdmin)
admin.site.register(WalletTransaction, WalletTransactionAdmin)
