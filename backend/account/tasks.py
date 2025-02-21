from celery import shared_task
from util.mail import mail
import logging

logger = logging.getLogger(__name__)

@shared_task(bind=True, autoretry_for=(Exception,), retry_kwargs={"max_retries": 3, "countdown":5})
def send_mail(
    self,
    subject: str,
    message: str,
    recipient_list: list,
    fail_silently: bool = False,
    html_message: str = None,
    ignore_debug: bool = False,
):
    try:
        output = mail(
            subject,
            message,
            recipient_list,
            fail_silently,
            html_message,
            ignore_debug,
        )

        if output is not 1:
            logger.warning(f"Failed to sent mail to {recipient_list} with output being {output}")
    except Exception as e:
        logger.exception(f"Attempting to send mail to {recipient_list} with exception {e}", exc_info=True)
        raise Exception()


    return output


@shared_task
def add(a, b):
    return a + b