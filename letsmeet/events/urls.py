from django.conf.urls import url
from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import GenericSitemap

from .views import (
    EventCommentCreateView,
    EventUpdateView,
    EventDetailView,
    EventRSVPView,
)
from . import feeds
from communities.models import Community
from .models import Event

community_dict = {
    'queryset': Community.objects.exclude(is_deleted=True),
    'date_field': 'modified',
}

event_dict = {
    'queryset': Event.objects.all(),
    'date_field': 'modified',
}

urlpatterns = [
    # feeds
    url(r'^ical/(?P<uuid>.+)/$', feeds.ICalUserEventsFeed(), name='personal_events_ical_feed_legacy'),  # support legacy
    url(r'^feed/ical/$', feeds.ICalUserEventsFeed(), name='all_events_ical_feed'),
    url(r'^feed/json/$', feeds.JsonUserEventsFeed(), name='all_events_json_feed'),
    url(r'^feed/(?P<uuid>.+)/ical/$', feeds.ICalUserEventsFeed(), name='personal_events_ical_feed'),
    url(r'^feed/(?P<uuid>.+)/json/$', feeds.JsonUserEventsFeed(), name='personal_events_json_feed'),
    url(r'^c/(?P<community_slug>[\w-]+)/rss/$', feeds.LatestEventsFeed(), name='events_feed'),
    url(r'^c/(?P<community_slug>[\w-]+)/ical/$', feeds.ICalCommunityEventsFeed(), name='community_events_ical_feed'),
    url(r'^c/(?P<community_slug>[\w-]+)/json/$', feeds.JsonCommunityEventsFeed(), name='community_events_json_feed'),
    # views
    url(r'^c/(?P<community_slug>[\w-]+)/(?P<slug>[\w-]+)/$', EventDetailView.as_view(), name='event_detail'),
    url(r'^c/(?P<community_slug>[\w-]+)/(?P<slug>[\w-]+)/edit/$', EventUpdateView.as_view(), name='event_update'),
    url(r'^c/(?P<community_slug>[\w-]+)/(?P<slug>[\w-]+)/write-comment/$', EventCommentCreateView.as_view(), name='eventcomment_create'),
    url(r'^c/(?P<community_slug>[\w-]+)/(?P<slug>[\w-]+)/rsvp/(?P<answer>(yes|no|reset))/$', EventRSVPView.as_view(), name='event_rsvp'),
    url(r'^sitemap\.xml$', sitemap,
        {'sitemaps': {
            'communities': GenericSitemap(community_dict, priority=0.7),
            'events': GenericSitemap(event_dict, priority=0.6)}},
        name='django.contrib.sitemaps.views.sitemap')
]
