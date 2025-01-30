from django.db import models, transaction

from util.models.base_models import UUIDPrimaryFieldModel, TimeMonitorModel
from util.models.shortcuts import User
from counselling.models.Counsellor import Counsellor
from counselling.models.Slot import Slot
from wallet.models.Transaction import Transaction
from chat.models import Chat

class SessionManager(models.Manager):

    def create_session(self, user, counsellor, slot, from_datetime):
        from util.models.shortcuts import User
        from counselling.models import Counsellor, Slot

        with transaction.atomic():

            trans = Transaction.create_transaction(
                user,
                counsellor,
                slot.fee
            )

            chat = Chat.objects.create_chat(
                user,
                counsellor,
            )

            session = self.model(
                user=user,
                counsellor=counsellor,
                transaction=transaction,
                chat=chat,
                from_datetime=from_datetime,
                to_datetime=from_datetime+slot.duration,
            )
            session.save()
        return session




class Session(UUIDPrimaryFieldModel, TimeMonitorModel):

    user = models.ForeignKey(
        User, on_delete=models.CASCADE
    )

    counsellor = models.ForeignKey(
        Counsellor,
        on_delete=models.CASCADE,
        related_name="sessions",
    )

    transaction = models.ForeignKey(
        Transaction,
        on_delete=models.CASCADE
    )

    slot = models.ForeignKey(
        Slot,
        on_delete=models.CASCADE
    )
    
    chat  = models.ForeignKey(
        Chat,
        on_delete=models.CASCADE
    )

    from_datetime = models.DateTimeField(
    )

    to_datetime = models.DateTimeField(
    )

    objects = SessionManager()

    def __str__(self):
        return f"{self.user} - {self.counsellor}: {self.from_datetime}"

    
