from rest_framework import serializers

from chat.models import Chat

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = [
            "id",
            "user_a", "user_b",
            "type", "is_active"
        ]