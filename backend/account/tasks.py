from celery import shared_task
from util.mail import mail

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
        return mail(
            subject,
            message,
            recipient_list,
            fail_silently,
            html_message,
            ignore_debug,
        )   