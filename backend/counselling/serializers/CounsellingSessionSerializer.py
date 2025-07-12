from rest_framework import serializers

from account.serializers.UserSerializer import UserProfileSerializer
from counselling.models import CounsellingSession
from counselling.serializers import CounsellorProfileMinmialSerializer


class CounsellingSessionSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()
    counsellor = CounsellorProfileMinmialSerializer()

    fee = serializers.DecimalField(source="slot.fee", max_digits=10, decimal_places=2)

    class Meta:
        model = CounsellingSession
        fields = [
            "id",
            "user",
            "counsellor",
            "transaction",
            "slot",
            "chat",
            "from_datetime",
            "to_datetime",
            "fee",
            "type",
        ]
