from django.db import models

from util.models.base_models import UUIDPrimaryFieldModel, TimeMonitorModel
from util.models.shortcuts import User

class ChatManager(models.Manager):
    def create_chat(self, user_a, user_b, *args, **kwargs):
        kwargs.setdefault('type', 'counselling')

        chat = self.model(
            user_a=user_a,
            user_b=user_b,
            *args,
            **kwargs
        )
        chat.save()
        return chat

class Chat(UUIDPrimaryFieldModel, TimeMonitorModel):

    user_a = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='chat_initiator'
    )

    user_b = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="chat_receiver"
    )

    type = models.CharField(
        max_length=16,
    )

    is_active = models.BooleanField(
        default=True,
    )

    obects = ChatManager()

