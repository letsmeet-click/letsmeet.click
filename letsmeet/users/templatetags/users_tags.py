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

    return static(getattr(up.avatar, size).url)
