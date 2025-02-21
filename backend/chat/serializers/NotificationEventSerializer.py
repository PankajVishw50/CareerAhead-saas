from rest_framework import serializers

class BaseNotificationEventSerializer(serializers.Serializer):
    type = serializers.ChoiceField(
        choices=["message.new", "message.seen"],
    )

class ChatNotificationSerializer(serializers.Serializer):
    chat_id = serializers.CharField(required=True)
    message = serializers.CharField(required=True)


class NotificationEventSerializer(BaseNotificationEventSerializer):
    payload = serializers.DictField(required=True)

    def validated(self, data):
        payload_data = data.get('payload', {})
        type_value = data.get('type')

        # Mapping of serializers
        serializer_mapping = {
            "chat": ChatNotificationSerializer,
        }

        if not serializer_mapping.get(type_value):
            raise serializers.ValidationError("Invalid type")

        payload_serializer = serializer_mapping[type_value]
        payload_serialized = payload_serializer(data=payload_data)

        if not payload_serialized.is_valid():
            raise serializers.validationError(payload_serialized.errors)
        
        data['payload'] = payload_serialized.data

        return data
        