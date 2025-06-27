from django.db import models

from util.models.base_models import UUIDPrimaryFieldModel, TimeMonitorModel
from util.models.shortcuts import User


class ChatManager(models.Manager):
    def create_chat(self, user_a, user_b, *args, **kwargs):
        kwargs.setdefault("type", "counselling")

        chat = self.model(user_a=user_a, user_b=user_b, *args, **kwargs)
        chat.save()
        return chat

    def all_valids(self, **kwargs):
        return self.filter(is_active=True, **kwargs)

    def get_valid(self, **kwargs):
        return self.all_valids().get(**kwargs)

    def all_invalids(self, **kwargs):
        return self.filter(is_active=False, **kwargs)

    def get_invalid(self, **kwargs):
        return self.all_invalids().get(**kwargs)


class Chat(UUIDPrimaryFieldModel, TimeMonitorModel):
    class Meta:
        ordering = ["-created_at"]

    user_a = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="chat_initiator"
    )

    user_b = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="chat_receiver"
    )

    type = models.CharField(
        max_length=16,
    )

    is_active = models.BooleanField(
        default=True,
    )

    objects = ChatManager()

    # @property
    # def session_from_datetime(self):
    #     return self.session.from_datetime

    def user_owns_chat(self, user):
        if user == self.user_a or user == self.user_b:
            return True
        return False

    def new_message(self, sender, message):
        from chat.models import Message

        if not self.user_owns_chat(sender):
            raise ValueError(
                "sender do not have priviledge to send message in this chat"
            )

        return Message.objects.create(
            chat=self,
            msg=message,
            sender=sender,
        )
