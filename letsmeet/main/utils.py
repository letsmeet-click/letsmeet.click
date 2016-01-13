import json
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


def send_notification(recipients, subject, template, context):
    addresses = recipients.values_list('email', flat=True)
    if addresses:
        text = render_to_string(template, context)
        mail = EmailMessage(
            subject='[letsmeet.click] ' + subject,
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
