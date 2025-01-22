from celery import shared_task
# from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

@shared_task
def send_notification_via_email(subject, recipient_list, template, context=None):
    """
    Celery task to send login notification via email.
    """
    if context is None:
        context = {}

   # Render the HTML content (this must be a string)
    html_content = render_to_string(f'emails/{template}', context)

    # Create the email object
    email = EmailMessage(
        subject=subject,               # Email subject
        body=html_content,            # Email body (HTML content as string)
        from_email='your_email@example.com',  # Replace with your sender email
        to=recipient_list             # Recipient list
    )
    email.content_subtype = "html"  # Specify the email content type as HTML
    email.send()