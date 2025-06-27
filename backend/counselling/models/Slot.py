from django.db import models
import datetime
from django.conf import settings

from util.models.base_models import UUIDPrimaryFieldModel, TimeMonitorModel
from counselling.models.Counsellor import Counsellor


class SlotManager(models.Manager):

    def all_valids(self, *args, **kwargs):
        return self.filter(is_deleted=False, *args, **kwargs)

    def all_actives(self, *args, **kwargs):
        return self.get_valids().filter(is_active=True, *args, **kwargs)

    def all_inactives(self, *args, **kwargs):
        return self.get_valids().filter(is_active=False, *args, **kwargs)

    def get_valid(self, *args, **kwargs):
        return self.all_valids().get(*args, **kwargs)

    def get_active(self, *args, **kwargs):
        return self.all_actives().get(*args, **kwargs)

    def get_inactive(self, *args, **kwargs):
        return self.all_inactives().get(*args, **kwargs)


class Slot(UUIDPrimaryFieldModel, TimeMonitorModel):
    ALL_DAYS = 0b1111111

    class Meta:
        ordering = ["-modified_at"]

    counsellor = models.ForeignKey(
        Counsellor,
        related_name="slots",
        related_query_name="slots",
        on_delete=models.CASCADE,
    )

    from_time = models.TimeField()

    duration = models.DurationField()

    days = models.PositiveSmallIntegerField(
        default=ALL_DAYS,
        db_default=ALL_DAYS,
    )

    fee = models.PositiveIntegerField(
        default=0,
        db_default=0,
    )

    timezone = models.CharField(
        max_length=32,
    )

    is_active = models.BooleanField(default=True, db_default=True)

    is_deleted = models.BooleanField(
        default=False,
        db_default=False,
    )

    objects = SlotManager()

    @property
    def to_time(self):
        if not isinstance(self.from_time, datetime.time) or not isinstance(
            self.duration, datetime.timedelta
        ):
            return NotImplementedError

        _dt = datetime.datetime.combine(datetime.datetime.today(), self.from_time)
        return (_dt + self.duration).time()

    def __str__(self):
        return f"{self.counsellor.user.email}: {self.from_time} - {self.to_time}"

    def work_day(self, day: int) -> bool:
        return (self.days & (2**day)) == (2**day)

    def deactivate(self):
        if self.is_active == False:
            return True

        self.is_active = False
        self.save()
        return True

    def activate(self):
        if self.is_active == True:
            return True

        self.is_active = True
        self.save()
        return True

    def delete(self):
        if self.is_deleted == True:
            return True

        self.is_deleted = True
        self.save()
        return True
