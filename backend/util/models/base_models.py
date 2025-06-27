from django.db import models
from uuid import uuid4


class UUIDPrimaryFieldModel(models.Model):
    class Meta:
        abstract = True

    id = models.UUIDField(primary_key=True, default=uuid4)


class TimeMonitorModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    modified_at = models.DateTimeField(
        auto_now=True,
    )
