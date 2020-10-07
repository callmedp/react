#inter app imports 
from wallet.models import (Wallet, RewardPoint, WalletTransaction)


#third party imports 
from rest_framework import serializers


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = '__all__'


class RewardPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = RewardPoint
        fields = '__all__'


class WalletTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WalletTransaction
        fields = '__all__'
