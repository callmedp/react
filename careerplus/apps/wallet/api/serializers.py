from rest_framework import serializers
from wallet.models import Wallet,WalletTransaction

#



class WalletHistoryTxnSerializer(serializers.ModelSerializer):
    wal_total = serializers.SerializerMethodField()


    class Meta:
        model = Wallet
        fields = ['wal_total' ]

    #
    def get_wal_total(self,obj):
        return obj.get_current_amount()
    # #
    # def get_txns(self,obj):
    #     txns = obj.wallettxn.filter(txn_type__in=[1, 2, 3, 4, 5], point_value__gt=0).order_by('-created')
    #     return txns




class WalletTransactionSerializer(serializers.ModelSerializer):
    added_point_expiry = serializers.SerializerMethodField()
    wallet = WalletHistoryTxnSerializer(read_only=True)
    # wal_total = serializers.SerializerMethodField()

    class Meta:
        model = WalletTransaction
        exclude = ('cart','ecash_txn','added_by','point_txn')

    # def get_added_point_expiry(self,obj):
    #     return obj.added_point_expiry()
    #
    # def get_wal_total(self,obj):
    #     return obj.wallet.get_current_amount()
