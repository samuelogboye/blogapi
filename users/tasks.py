from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_registration_email(subject, message, recipient_list):
    """
    Celery task to send registration email.
    """
    send_mail(
        subject,
        message,
        'your_email@example.com',  # From email
        recipient_list,  # To email
        fail_silently=False,
    )
