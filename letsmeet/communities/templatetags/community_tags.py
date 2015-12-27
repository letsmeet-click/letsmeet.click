from django import template
from communities.models import CommunitySubscription

register = template.Library()


@register.simple_tag
def get_community_subscription(user, community):
    # use filter + first to return None if there is no subscription
    return CommunitySubscription.objects.filter(user=user, community=community).first()
