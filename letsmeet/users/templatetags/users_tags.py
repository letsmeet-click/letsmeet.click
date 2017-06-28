from django import template
from django.contrib.auth.models import User
from django.contrib.staticfiles.templatetags.staticfiles import static
from users.models import UserProfile

register = template.Library()


@register.filter
def avatar_url(user, size='thumbnail'):
    if not isinstance(user, User):
        return static('img/letsmeet_icon.png')

    up, created = UserProfile.objects.get_or_create(user=user)
    if not up.avatar:
        return static('img/letsmeet_icon.png')

    return getattr(up.avatar, size).url


@register.inclusion_tag('users/templatetags/notification_change_list_group_item.html')
def notification_change_list_group_item(notification_type, notification_state, text):
    return {
        'notification_type': notification_type,
        'notification_state': notification_state,
        'text': text,
    }


@register.filter
def backend_name(backend):
    name = backend
    name = name.replace('-oauth2', '')
    return name
