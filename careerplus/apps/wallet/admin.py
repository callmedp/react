from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import Wallet, RewardPoint, ECash, WalletTransaction, ECashTransaction, PointTransaction


class RewardPointInline(admin.TabularInline):
    model = RewardPoint
    readonly_fields = ['modified']
    extra = 0

class ECashInline(admin.TabularInline):
    model = ECash
    readonly_fields = ['modified']
    extra = 0

class ECashTxnInline(admin.TabularInline):
    model = ECashTransaction
    readonly_fields = ['modified']
    fk_name = 'transaction'
    raw_id_fields = ['ecash', 'transaction']
    extra = 0

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
    inlines = [PointTxnInline, ECashTxnInline]
    

class WalletAdmin(admin.ModelAdmin):
    list_display = [
        'created', 'owner', 'owner_email', ]
    readonly_fields = ['modified', 'owner', 'owner_email']
    search_fields = ('owner', 'owner_email')
    inlines = (RewardPointInline, ECashInline,)
    
    
# Register your models here.
admin.site.register(Wallet, WalletAdmin)
admin.site.register(WalletTransaction, WalletTransactionAdmin)
