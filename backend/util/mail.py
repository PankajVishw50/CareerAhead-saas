from django.core.mail import send_mail as django_send_mail
from django.conf import settings

def mail(
        subject: str, 
        message: str,
        recipient_list: list,
        fail_silently=False,
        html_message=None,
        ignore_debug=False,
):
    if settings.DEBUG:
        recipient_list = []
        if settings.EMAIL_DEBUG_REDIRECT:
            recipient_list = settings.EMAIL_DEBUG_RECEIVERS


    mail_result = django_send_mail(
        subject=subject,
        message=message,
        recipient_list=recipient_list,
        fail_silently=fail_silently,
        html_message=html_message,
        from_email=None
    )

    if settings.EMAIL_LOG:
        prefix = (
            'Successfully sent mail to'
            if mail_result 
            or (settings.DEBUG and not settings.EMAIL_DEBUG_REDIRECT)
            else "Failed to send mail to"
        )
        print(f"{prefix} {recipient_list}")
        
    return mail_result

