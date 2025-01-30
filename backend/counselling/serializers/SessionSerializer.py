from rest_framework import serializers

from counselling.models import Session

class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = [
            "id", "user", "counsellor",
            "transaction", "slot", "chat",
            "from_datetime", "to_datetime",
        ]