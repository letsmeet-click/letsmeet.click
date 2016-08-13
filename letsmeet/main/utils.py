import json

from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


def send_notification(recipients, subject, template, context):
    recipients = recipients.exclude(email='')
    addresses = recipients.values_list('email', flat=True)
    if addresses:
        text = render_to_string(template, context)
        mail = EmailMessage(
            subject=settings.EMAIL_SUBJECT_PREFIX + ' ' + subject,
            body=text,
            to=addresses,
        )
        recipient_variables = {}
        for recipient in recipients:
            recipient_variables[recipient.email] = {
                'id': recipient.id
            }

        mail.extra_headers['recipient_variables'] = json.dumps(recipient_variables)
        mail.send()
