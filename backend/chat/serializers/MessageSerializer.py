from rest_framework import serializers

from chat.models import Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = [
            "id",
            "chat",
            "sender",
            "msg",
            "seen",
            "created_at",
            "modified_at",
        ]
        level = 1
