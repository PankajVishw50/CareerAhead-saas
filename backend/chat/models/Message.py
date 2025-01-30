from django.db import models

from util.models.base_models import UUIDPrimaryFieldModel, TimeMonitorModel
from util.models.shortcuts import User
from chat.models.Chat import Chat

class Message(UUIDPrimaryFieldModel, TimeMonitorModel):

    chat = models.ForeignKey(
        Chat,
        on_delete=models.CASCADE
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