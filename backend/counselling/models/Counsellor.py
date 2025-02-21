from django.db import models
import pytz

from util.models.base_models import TimeMonitorModel, UUIDPrimaryFieldModel
from util.models.shortcuts import User

class CounsellorManager(models.Manager):

    # Method to create counsellor
    def create_counsellor(self, user, about: dict, **kwargs):
        from counselling.models import About

        counsellor = self.model(
            user=user,
            **kwargs,
        )
        counsellor.save()

        about = About.objects.create(
            counsellor=counsellor,
            **about,
        )

        counsellor.save()
        return counsellor
    

class Counsellor(UUIDPrimaryFieldModel, TimeMonitorModel):
    class Meta:
        ordering = ['-modified_at']

    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
    )

    timezone = models.CharField(
        max_length=32,
        default=pytz.utc.zone,
    )

    objects = CounsellorManager()

    @property
    def tz(self):
        return pytz.timezone(self.timezone)

    def __str__(self):
        return self.user.email

    def create_slot(self, fee, from_time, duration, **kwargs):
        from counselling.models import Slot

        return Slot.objects.create(
            counsellor=self,
            from_time=from_time,
            duration=duration,
            timezone=self.timezone,
            is_active=True,
            is_deleted=False,
            fee=fee,
            **kwargs,
        )