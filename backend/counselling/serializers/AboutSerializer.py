from rest_framework import serializers

from counselling.models import About


class AboutSerializer(serializers.ModelSerializer):
    class Meta:
        model = About
        fields = [
            "id",
            "counsellor",
            "introduction",
            "qualification",
            "speciality",
            "methodology",
        ]
        read_only_fields = [
            "id",
            "counsellor",
        ]
