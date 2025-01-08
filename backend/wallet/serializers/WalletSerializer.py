from rest_framework.serializers import ModelSerializer

from wallet.models import Wallet

class WalletSerializer(ModelSerializer):
    class Meta:
        model = Wallet
        fields = [
            'user', 'balance', 'is_active',
        ]
        read_only_fields = ['balance', 'is_active']
    