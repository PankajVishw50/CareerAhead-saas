from django.db import models

from util.models.base_models import UUIDPrimaryFieldModel, TimeMonitorModel

class About(UUIDPrimaryFieldModel, TimeMonitorModel):

    MAX_LENGTH = 1024 * 10

    counsellor = models.OneToOneField(
        to="counselling.Counsellor",
        on_delete=models.CASCADE,
    )

    introduction = models.TextField(
        max_length=MAX_LENGTH,
    )

    qualification = models.TextField(
        max_length=MAX_LENGTH,
    )

    
    speciality = models.TextField(
        max_length=MAX_LENGTH,
    )


    methodology = models.TextField(
        max_length=MAX_LENGTH,
    )

    def __str__(self):
        return self.counsellor.user.email