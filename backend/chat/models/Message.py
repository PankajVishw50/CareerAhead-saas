from django.db import models

from util.models.base_models import UUIDPrimaryFieldModel, TimeMonitorModel
from util.models.shortcuts import User
from chat.models.Chat import Chat

class Message(UUIDPrimaryFieldModel, TimeMonitorModel):

    chat = models.ForeignKey(
        Chat,
        on_delete=models.CASCADE,
        related_name="messages",
    )

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    msg = models.TextField(
    )

    seen = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return self.msg[:10]

    @property
    def receiver(self):
        return self.chat.user_a if self.chat.user_a != self.sender else self.chat.user_b

    def get_alternate_user(self, user):
        if user not in [self.sender, self.receiver]:
            return False

        return self.sender if self.receiver == user else self.receiver