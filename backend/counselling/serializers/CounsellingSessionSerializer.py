from rest_framework import serializers

from counselling.models import CounsellingSession


class CounsellingSessionSerializer(serializers.ModelSerializer):
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
        ]
