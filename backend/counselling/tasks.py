from celery import shared_task
import logging

from counselling.models import CounsellingSession
import datetime
import pytz

logger = logging.getLogger()


@shared_task(bind=True, retry_kwargs={"max_retries": 3, "default_retry_delay": 0})
def update_session_chat(
    self,
    session_id,
):

    try:
        # Update session
        session = CounsellingSession.objects.select_related("chat").get(id=session_id)
        chat = session.chat

        # Check if need to update
        now = datetime.datetime.now(pytz.utc)

        if (
            now >= (session.from_datetime - datetime.timedelta(seconds=10))
            and now < session.to_datetime
        ):
            chat.is_active = True
        else:
            chat.is_active = False

        chat.save()
    except CounsellingSession.DoesNotExist as e:
        logger.error(
            f"Session {session_id} not found. No retry. Error: {e}", exc_info=True
        )
        return 0
    except Exception as e:
        logger.exception(
            f"Unexpected error updating chat for session {session_id}. Retrying... Error: {e}"
        )
        raise self.retry(exc=e)

    logger.debug(f"Session's ({session.id}) chat is updated with {chat.__dict__}")
    return 1
