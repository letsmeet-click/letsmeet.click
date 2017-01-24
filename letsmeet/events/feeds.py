from django_ical.views import ICalFeed
from django.contrib.syndication.views import Feed
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from .models import Event


class LatestEventsFeed(Feed):
    description = "letsmeet.click events feed"

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

    def item_pubdate(self, item):
        return item.created


class ICalCommunityEventsFeed(ICalFeed):
    description = "letsmeet.click community events feed"
    product_id = '-//letsmeet.click//Event//DE'
    timezone = 'UTC'

    def title(self, obj):
        return "{} calendar".format(obj.name)

    def file_name(self, obj):
        return "feed_{}.ics".format(obj.slug)

    def get_object(self, request, community_slug):
        from communities.models import Community
        try:
            return Community.objects.get(slug=community_slug)
        except Community.DoesNotExist:
            return []

    def items(self, obj):
        return Event.objects.filter(community=obj).order_by('-created')

    def item_title(self, item):
        return item.name

    def item_description(self, item):
        return "{}\n\n{}".format(item.description, item.get_absolute_url())

    def item_pubdate(self, item):
        return item.created

    def item_start_datetime(self, item):
        return item.begin

    def item_end_datetime(self, item):
        return item.end

    def item_link(self, item):
        return item.get_absolute_url()


class ICalUserEventsFeed(ICalCommunityEventsFeed):

    def title(self, item):
        return "your letsmeet.click calendar"

    def file_name(self, item):
        return "feed_user.ics"

    def get_object(self, request):
        return request.user

    def items(self, obj):
        if hasattr(obj, 'userprofile'):
            return obj.userprofile.get_upcoming_yes_events().order_by('-created')
        return []


class ICalPersonalUserEventsFeed(ICalCommunityEventsFeed):

    def title(self, item):
        return "your personal letsmeet.click calendar"

    def file_name(self, item):
        return "feed_user.ics"

    def get_object(self, request, uuid):
        return get_object_or_404(get_user_model(), userprofile__personal_ical_uuid=uuid)

    def items(self, obj):
        if hasattr(obj, 'userprofile'):
            return obj.userprofile.get_upcoming_yes_events().order_by('-created')
        return []