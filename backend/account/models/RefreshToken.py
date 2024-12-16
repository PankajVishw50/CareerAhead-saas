from django.db import models
from util.models.base_models import UUIDPrimaryFieldModel, TimeMonitorModel
from account.auth import Token

class RefreshToken(UUIDPrimaryFieldModel, TimeMonitorModel):

    user = models.ForeignKey(
        to='User',
        on_delete=models.CASCADE,
        related_name='tokens'
    )

    code = models.CharField(
        max_length=255,
        default=Token.generate_refresh_token,
        unique=True,
    )

    expiration_on = models.DateTimeField(
        default=Token.generate_refresh_expiry_time,
    )

