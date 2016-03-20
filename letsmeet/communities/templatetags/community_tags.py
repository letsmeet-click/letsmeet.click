from django import template

register = template.Library()


@register.simple_tag
def get_community_subscription(user, community):
    return community.get_user_subscription(user)
