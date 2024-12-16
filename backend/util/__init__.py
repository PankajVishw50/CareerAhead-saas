import datetime
import pytz 
from django.conf import settings


def get_email_expiration_time(now=None):
    now = now or datetime.datetime.now(pytz.utc)
    return datetime.datetime.now(pytz.utc) + datetime.timedelta(seconds=settings.EMAIL_VERIFICATION_CODE_EXPIRY)