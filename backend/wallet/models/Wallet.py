from util.models.base_models import UUIDPrimaryFieldModel, TimeMonitorModel
from django.db import models
from django.apps import apps

from util.models.shortcuts import User

class WalletManager(models.Manager):

    def create_wallet_object(
            self, user, 
            **kwargs
    ):        
        kwargs.setdefault('is_active', False)

        wallet = self.model(
            user=user,
            **kwargs
        )

        wallet.save()
        return wallet

    
    def create_wallet(self, user):
        from wallet.razorpay import razorpay
        
        wallet = self.create_wallet_object(user)

        # TODO: It should be done using 
        # background worker so this operation 
        # can be faster and user can get
        # response faster
        if (contact_id := razorpay.create_contact(user)):
            wallet.contact_id = contact_id 
            wallet.is_active = True
        else:
            wallet.is_active = False

        wallet.save()
        return wallet

        

class Wallet(UUIDPrimaryFieldModel, TimeMonitorModel):

    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
    )

    contact_id = models.CharField(
        max_length=30,
        blank=True,
        null=True,
    )

    balance = models.IntegerField(
        default=0,
        db_default=0,
    )

    _is_active = models.BooleanField(
        default=False,
    )

    objects = WalletManager()

    def __str__(self):
        return f"{self.user.email}: {self.balance}"
    
    def have_balance(self, amount):
        if self.balance >= amount:
            return True
    
    @property
    def is_active(self):
        return self._is_active 
    
    @is_active.setter
    def is_active(self, value):
        if not isinstance(value, bool):
            raise ValueError('Value must be a boolean')

        if value is True and not self.contact_id:
            raise ValueError('Contact ID is must be set before activating wallet')

        self._is_active = value
        self.save()
        return self._is_active

    def withdraw(self, amount):
        if not self.have_balance(amount) or not self.is_active:
            return False

        Withdrawal = apps.get_model('wallet.Withdrawal')
        withdrawal = Withdrawal.objects.create_withdrawal(self, amount)

        if withdrawal:
            self.balance -= amount
        self.save()
        return withdrawal