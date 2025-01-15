from django.db import models
import datetime 

from util.models.base_models import UUIDPrimaryFieldModel, TimeMonitorModel
from counselling.models.Counsellor import Counsellor

class Slot(UUIDPrimaryFieldModel, TimeMonitorModel):
    ALL_DAYS = 0b1111111

    class Meta:
        ordering = ['-modified_at']

    counsellor = models.ForeignKey(
        Counsellor,
        related_name="slots",
        related_query_name="slots",
        on_delete=models.CASCADE,
    )

    from_time = models.TimeField(
    )

    duration = models.DurationField(
    )

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

    is_active = models.BooleanField(
        default=True,
        db_default=True
    )

    is_deleted = models.BooleanField(
        default=False,
        db_default=False,
    )

    @property
    def to_time(self):
        _dt = datetime.datetime.combine(datetime.datetime.today(), self.from_time)
        return (_dt + self.duration).time()
    

    def __str__(self):
        return f"{self.counsellor.user.email}: {self.from_time} - {self.to_time}"
