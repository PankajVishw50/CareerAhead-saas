from rest_framework import serializers

from counselling.models import Slot

class SlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slot
        fields = [
            "id", "counsellor",
            "from_time", "to_time",
            "duration",
            "days", "fee",
            "timezone", "is_active",
        ]
        read_only_fields = [
            "is_active", "to_time", "timezone", "counsellor"
        ]

    def validate_duration(self, value):
        return value * 60

class AvailableSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slot
        fields = [
            "id",
            "from_time", "to_time",
            "duration", "days",
            "fee", "timezone",
            "from_datetime", "to_datetime",
            "is_active",
        ]
        read_only_fields = [
            "id",
            "from_datetime", "to_datetime", "to_time",
            "is_active",
        ]

    from_datetime = serializers.DateTimeField()
    to_datetime = serializers.DateTimeField()
