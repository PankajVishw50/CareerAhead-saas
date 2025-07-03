from channels.generic.websocket import WebsocketConsumer
from django.db import transaction
from django.db.models import F
from rest_framework.response import Response
import json
from django.core.exceptions import ValidationError
from asgiref.sync import async_to_sync
import logging

from chat.serializers import NotificationEventSerializer, MessageSerializer
from chat.models import Chat, Message
from util.helpers import convert_uuid, serializer_uuid_dict

logger = logging.getLogger(__name__)


def invalid_type_response(payload):
    return send_response("error", payload)


def send_response(type, payload):
    return {"type": type, "payload": payload}


def load_serialized_event(type=None):
    def decorator(func):
        def wrapper(self, event=None, text_data=None):
            # import ipdb;ipdb.set_trace()
            event_data = (
                event.get("text") if event and isinstance(event, dict) else text_data
            )

            result, data = self._get_notification_serializer(event_data)
            if not result or (type is not None and data["type"] != type):
                message = data
                # Don't send exceptions to client
                if isinstance(data, Exception):
                    message = "Invalid event"
                self.send(text_data=json.dumps(invalid_type_response(message)))
                return
            self.event_data = data
            return func(self, event or text_data)

        return wrapper

    return decorator


class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope["user"]

        # Join group
        async_to_sync(
            self.channel_layer.group_add,
        )(
            self.user.id.hex,
            self.channel_name,
        )

        with transaction.atomic():
            # Updating active devices
            # Using `F` to prevent race condition
            self.user.active_devices = F("active_devices") + 1
            self.user.save()

            self.accept()
            self.send(f"HI, {self.scope['user'].email}")

        logger.info(f"Websocket accepted")

    def disconnect(self, close_code):
        # Leave Group
        async_to_sync(self.channel_layer.group_discard)(
            self.user.id.hex,
            self.channel_name,
        )
        # Updating active devices
        # Using `F` to prevent race condition
        self.user.active_devices = F("active_devices") - 1
        self.user.save()

    def _get_notification_serializer(self, text_data):
        try:
            json_data = json.loads(text_data)
            data_s = NotificationEventSerializer(data=json_data)
            if not data_s.is_valid():
                return (False, data_s.errors)
            data = data_s.data

        except json.JSONDecodeError as e:
            return (False, e)

        return (True, data)

    @load_serialized_event(None)
    def receive(self, text_data):
        result, data = self._get_notification_serializer(text_data)
        if not result:
            self.send(text_data=json.dumps(invalid_type_response(data)))
            return

        match data.get("type"):
            case "message.new":
                async_to_sync(self.channel_layer.send)(
                    self.channel_name, {"type": "message.new", "text": text_data}
                )
            case "message.seen":
                async_to_sync(self.channel_layer.send)(
                    self.channel_name,
                    {
                        "type": "message.seen",
                        "text": text_data,
                    },
                )

    def send_client(self, event):
        self.send(text_data=event["text"])

    @load_serialized_event("message.new")
    def message_new(self, event):
        # Check if provided_chat id is valid
        try:
            chat = Chat.objects.get(id=self.event_data["payload"]["chat_id"])
        except json.JSONDecodeError:
            self.send(text_data=json.dumps(invalid_type_response("Invalid json")))
            return
        except Chat.DoesNotExist:
            self.send(
                text_data=json.dumps(invalid_type_response("Chat does not exist"))
            )
            return
        except ValidationError:
            self.send(text_data=json.dumps(invalid_type_response("Invalid chat id")))
            return

        # Check if user is part of the chat
        if not chat.user_owns_chat(self.user):
            self.send(
                text_data=json.dumps(
                    invalid_type_response("You are not part of this chat")
                )
            )
            return

        # validate if chat is active
        if not chat.is_active:
            self.send(
                text_data=json.dumps(
                    invalid_type_response("Chat is not active: %s" % chat.id)
                )
            )
            return

        # Save message
        try:
            message = chat.new_message(self.user, self.event_data["payload"]["message"])
        except Exception as e:
            logger.exception(
                f"Failed to fetch chat by provided id with exception {e}", exc_info=e
            )
            self.send(
                text_data=json.dumps(invalid_type_response("Failed to send message"))
            )
            return

        # Send message to the chat users
        message_s = MessageSerializer(instance=message)
        response_data = serializer_uuid_dict(
            send_response("new_message", message_s.data)
        )
        self._broadcast_chat(chat, response_data)

    def _broadcast_chat(self, chat, text_data):
        for user in [chat.user_a, chat.user_b]:
            if not user.is_online:
                continue

            async_to_sync(self.channel_layer.group_send)(
                user.id.hex,
                {
                    "type": "send.client",
                    "text": json.dumps(
                        {
                            "type": "message.new",
                            "text": text_data,
                        }
                    ),
                },
            )

    @load_serialized_event("message.seen")
    def message_seen(self, event):
        try:
            chat = Chat.objects.get(id=self.event_data["payload"]["chat_id"])

            # validate if user owns this
            if not chat.user_owns_chat(self.user):
                return self.send(
                    text_data=json.dumps(invalid_type_response("Forbidden"))
                )

            message = chat.messages.get(id=self.event_data["payload"]["id"])
            # check if it's valid message
            # Found out it's not practical to cancel this request
            # if message.sender == self.user:
            #     return self.send(
            #         text_data=json.dumps(
            #             invalid_type_response(
            #                 "Cannot perform the action for specified id"
            #             )
            #         )
            #     )

            # Fetch all prior message to provided message which are not seen
            messages = chat.messages.filter(
                created_at__lte=message.created_at,
                seen=False,
                sender=message.get_alternate_user(self.user),
            )
        except Chat.DoesNotExist:
            return self.send(
                text_data=json.dumps(invalid_type_response("Chat not found"))
            )
        except Message.DoesNotExist:
            return self.send(
                text_data=json.dumps(invalid_type_response("Message not found"))
            )

        # Update Messages
        messages.update(seen=True)

        # Send Message to other user
        message_sender = (
            message.sender if message.sender != self.user else message.receiver
        )
        if message_sender.is_online:
            async_to_sync(self.channel_layer.group_send)(
                message_sender.id.hex,
                {
                    "type": "send.client",
                    "text": json.dumps(
                        send_response(
                            "message.seen",
                            {
                                "chat_id": str(message.chat_id),
                                "id": str(message.id),
                            },
                        )
                    ),
                },
            )
