from rest_framework.serializers import ModelSerializer

from wallet.models import Recharge

class RechargeSerializer(ModelSerializer):
    class Meta:
        model = Recharge
        fields = [
            'id', 'user', 'wallet', 'amount', 
            'currency', 'payment_id', 'order_id', 
            'status'
        ]
