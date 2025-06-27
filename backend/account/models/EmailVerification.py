from django.db import models
from django.conf import settings
from util.models.base_models import UUIDPrimaryFieldModel, TimeMonitorModel
from uuid import uuid4
from util import get_email_expiration_time
import datetime
from account.tasks import send_mail
import pytz
import logging

logger = logging.getLogger(__name__)


class EmailVerificationManager(models.Manager):
    def create_emailverification(self, user, **kwargs):
        sm = kwargs.pop("send_mail", True)

        emailverification = self.create(user=user, *kwargs)

        if sm:
            send_mail.delay(
                subject="Email Verification",
                message=f"This is you email otp: {emailverification.code}",
                html_message=f"This is your email otp: <b>{emailverification.code}</b>",
                recipient_list=[user.email],
            )
            logger.info(f"Mail Sent to {user.email}")
        return emailverification


class EmailVerification(UUIDPrimaryFieldModel, TimeMonitorModel):

    user = models.OneToOneField(
        to="account.User",
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

    objects = EmailVerificationManager()

    def get_verification_link(self):
        return None

    def verify(self, code=None, time=None, force=False):
        time = time or datetime.datetime.now(pytz.utc)

        if (self.code.hex == code and time < self.expiration_time) or force:
            self.verified = True
            self.verification_time = (
                time if time > self.expiration_time else datetime.datetime.now(pytz.utc)
            )
            return True

        return False

    def __str__(self):
        return f"{self.user.email}"
