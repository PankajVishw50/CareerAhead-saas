from django.db import models

from util.models.base_models import UUIDPrimaryFieldModel, TimeMonitorModel
from util.models.shortcuts import User
from wallet.models import Wallet
from util.helpers import generate_random_string

class RechargeManager(models.Manager):
    def create_recharge(self, user, wallet, amount, currency, order_id):
        recharge = self.create(
            user=user,
            wallet=wallet,
            amount=amount,
            currency=currency,
            order_id=order_id,
        )
        return recharge

class Recharge(UUIDPrimaryFieldModel, TimeMonitorModel):

    class Meta:
        ordering = ['-modified_at']

    class StatusChoices(models.TextChoices):
        created = 'Created'
        attempted = 'Attempted'
        paid = 'Paid'
        failed = 'failed'

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    wallet = models.ForeignKey(
        Wallet,
        on_delete=models.CASCADE,
    )

    amount = models.IntegerField(
    )
    
    currency = models.CharField(
        max_length=6,
    )

    payment_id = models.CharField(
        max_length=60,
        blank=True,
        null=True,
    )

    order_id = models.CharField(
        max_length=60,
        unique=True, 
    )

    status = models.CharField(
        max_length=16,
        choices=StatusChoices,
        default=StatusChoices.created,
        db_default=StatusChoices.created,
    )

    objects = RechargeManager()

    def __str__(self):
        return f"{self.user.email}: {self.amount}"

    def complete_payment(self, payment_id):
        if self.status == self.StatusChoices.paid:
            if self.payment_id == payment_id:
                return True 
            return False 
        
        self.status = self.StatusChoices.paid 
        self.payment_id = payment_id
        self.save()

        # Add money to wallet
        self.wallet.balance += self.amount 
        self.wallet.save()
        return True


    def verify_signature(self, payment_id, signature):
        from wallet.razorpay import razorpay
        if not razorpay.verify_signature(self.order_id, payment_id, signature):
            return False
        return self.complete_payment(payment_id)