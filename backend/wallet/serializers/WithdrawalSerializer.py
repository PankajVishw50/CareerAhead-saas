from rest_framework import serializers

from wallet.models import Withdrawal

class WithdrawalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Withdrawal
        fields = [
            'wallet', 'amount', 'state'
        ]
