from django import template
from communities.models import CommunitySubscription

register = template.Library()


@register.simple_tag
def get_community_subscription(user, community):
    return community.get_user_subscription(user)
