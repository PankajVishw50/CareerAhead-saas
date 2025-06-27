from django.dispatch import receiver
from django.db.models.signals import post_save
from counselling.models import CounsellingSession
from counselling.tasks import update_session_chat
import logging
import datetime

from util.decorators import disable_for_loaddata

logger = logging.getLogger()


@receiver(post_save, sender=CounsellingSession)
@disable_for_loaddata
def create_background_worker_for_session_chat_update(sender, **kwargs):
    # import ipdb;ipdb.set_trace()
    instance = kwargs.get("instance")

    logger.info(f"Signal received to CounsellingSession: id-{instance.id}")
    logger.debug(f"Signal for CounsellinSession: {instance.__dict__}")

    # Schedule to Enable chat
    update_session_chat.apply_async((instance.id,), eta=instance.from_datetime)

    # Schedule to Disable chat
    update_session_chat.apply_async(
        (instance.id,), eta=instance.to_datetime + datetime.timedelta(seconds=1)
    )
