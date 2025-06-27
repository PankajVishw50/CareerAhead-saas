from django.db import models, transaction as db_transaction

from util.models.base_models import UUIDPrimaryFieldModel, TimeMonitorModel
from util.models.shortcuts import User
from counselling.models.Counsellor import Counsellor
from counselling.models.Slot import Slot
from wallet.models.Transaction import Transaction
from chat.models import Chat


class CounsellingSessionManager(models.Manager):

    def create_session(self, user, counsellor, slot, from_datetime, **kwargs):

        with db_transaction.atomic():

            transaction = Transaction.objects.create_transaction(
                user, counsellor.user, slot.fee
            )

            chat = Chat.objects.create_chat(user, counsellor.user, is_active=False)

            session = self.model(
                user=user,
                counsellor=counsellor,
                transaction=transaction,
                slot=slot,
                chat=chat,
                from_datetime=from_datetime,
                to_datetime=from_datetime + slot.duration,
                **kwargs,
            )
            session.save()
        return session


class CounsellingSession(UUIDPrimaryFieldModel, TimeMonitorModel):

    user = models.ForeignKey(User, related_name="sessions", on_delete=models.CASCADE)

    counsellor = models.ForeignKey(
        Counsellor,
        on_delete=models.CASCADE,
        related_name="sessions",
    )

    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)

    slot = models.ForeignKey(
        Slot,
        on_delete=models.CASCADE,
        related_name="sessions",
    )

    chat = models.OneToOneField(Chat, on_delete=models.CASCADE, related_name="session")

    from_datetime = models.DateTimeField()

    to_datetime = models.DateTimeField()

    objects = CounsellingSessionManager()

    def __str__(self):
        return f"{self.user} - {self.counsellor}: {self.from_datetime}"
