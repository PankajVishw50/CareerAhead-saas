from util.models.base_models import UUIDPrimaryFieldModel, TimeMonitorModel
from django.db import models

from wallet.models import Wallet

class Transaction(UUIDPrimaryFieldModel, TimeMonitorModel):

    sender = models.ForeignKey(
        Wallet,
        on_delete=models.CASCADE,
        related_name="sent_transaction"
    )

    receiver = models.ForeignKey(
        Wallet,
        on_delete=models.CASCADE,
        related_name="received_transaction"
    )

    amount = models.PositiveIntegerField(
    )

    refunded = models.BooleanField(
        default=False
    )

    def __str__(self):
        return f"{self.sender.user.email} -> {self.receiver.user.email}: {self.amount}"
    