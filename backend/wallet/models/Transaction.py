from util.models.base_models import UUIDPrimaryFieldModel, TimeMonitorModel
from django.db import models

from wallet.models import Wallet

class TransactionManager(models.Manager):

    def create_transaction(self, sender, receiver, amount):

        if not sender.wallet.debit(amount):
            raise ValueError("failed to debit money from sender's wallet")
        
        if not receiver.wallet.credit(amount):
            sender.wallet.credit(amount)
            raise ValueError("failed to credit money to receiver's wallet")
        
        transaction = self.model(
            sender=sender.wallet,
            receiver=receiver.wallet,
            amount=amount
        )   
        transaction.save()
        return transaction     

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

    objects = TransactionManager()

    def __str__(self):
        return f"{self.sender.user.email} -> {self.receiver.user.email}: {self.amount}"    
    