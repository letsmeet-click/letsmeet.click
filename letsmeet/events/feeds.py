from django.contrib.syndication.views import Feed
from .models import Event


class LatestEventsFeed(Feed):
    description = "FIXME"

    def get_object(self, request, community_slug):
        from communities.models import Community
        return Community.objects.get(slug=community_slug)

    def title(self, obj):
        return "Events of {}".format(obj.name)

    def link(self, obj):
        return obj.get_absolute_url()

    def items(self, obj):
        return Event.objects.filter(community=obj).order_by('-created')

    def item_title(self, item):
        return item.name

    def item_description(self, item):
        return item.description
