from django.db import models
from django.conf import settings
from util.models.base_models import UUIDPrimaryFieldModel, TimeMonitorModel
from uuid import uuid4
from util import get_email_expiration_time
import datetime
import pytz 

class EmailVerification(UUIDPrimaryFieldModel, TimeMonitorModel):

    user = models.OneToOneField(
        to='account.User', 
        on_delete=models.CASCADE,
    )

    code = models.UUIDField(
        default=uuid4,
    )

    verified = models.BooleanField(
        db_default=False,
    )

    expiration_time = models.DateTimeField(
        default=get_email_expiration_time,
    )

    verification_time = models.DateTimeField(
        null=True,
        blank=True,
    )

    def get_verification_link(self):
        return None  


    def verify(self, code=None, time=None, force=False):
        time = time or datetime.datetime.now(pytz.utc)

        if (
            (self.code.hex == code and time < self.expiration_time)
            or force
        ):
            self.verified = True 
            self.verification_time = time if time > self.expiration_time else datetime.datetime.now(pytz.utc)
            return True 
        
        return False 

    def __str__(self):
        return f"{self.user.email}"

    