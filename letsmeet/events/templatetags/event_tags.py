from django import template
from events.models import EventRSVP

register = template.Library()


@register.simple_tag
def get_community_event_rsvp(user, event):
    if not event or not user:
        return None

    # use filter + first to return None if there is no subscription
    return EventRSVP.objects.filter(user=user, event=event).first()
