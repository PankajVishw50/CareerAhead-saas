from django.db import models 
from django.conf import settings

from util.models.base_models import UUIDPrimaryFieldModel, TimeMonitorModel

class WithdrawalManager(models.Manager):
    def validate_amount(self, amount):
        if (
            amount < settings.MINIMUM_WITHDRAWL
            or amount > settings.MAXIMUM_WITHDRAWL
        ):
            return False
        return True
        
    def create_withdrawal(self, wallet, amount):

        # Validate amount and enough balance
        if (
            not self.validate_amount(amount)
            or not wallet.have_balance(amount)
        ):
            return False

        withdrawal = self.model(
            wallet=wallet,
            amount=amount,
        )
        withdrawal.save()
        return withdrawal


class Withdrawal(UUIDPrimaryFieldModel, TimeMonitorModel):
    
    class StateChoices(models.TextChoices):
        pending = 'Pending'
        done = 'Done'
        failed = 'Failed'

    wallet = models.ForeignKey(
        'Wallet',
        on_delete=models.CASCADE,
    )

    payout_id = models.CharField(
        max_length=30,
    )

    amount = models.PositiveIntegerField(
    )

    state = models.CharField(
        max_length=16,
        choices=StateChoices,
        default=StateChoices.pending,
    )

    objects = WithdrawalManager()

    def __str__(self):
        return f"{self.wallet.user.email}: {self.amount}"

    def withdrawal_failed(self):

        # Check if it's not already in failed state
        if self.state == self.StateChoices.failed:
            return True
        self.state = self.StateChoices.failed
        self.save()

        # Add Money to wallet
        self.wallet.balance += self.amount
        self.wallet.save()
        return True
    
    def withdrawal_done(self):
        # Check if it's not already 
        # in done state
        if self.state == self.StateChoices.done:
            return True
        
        # Remove money from wallet
        # if it was in failed state
        if self.state == self.StateChoices.failed:
            if self.wallet.balance < self.amount:
                return False
            self.wallet.balance -= self.amount
            self.wallet.save()

        self.state = self.StateChoices.done
        self.save() 
        return True       
