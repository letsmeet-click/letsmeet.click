import rules
from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django_extensions.db.models import TimeStampedModel


class EventManager(models.Manager):
    def upcoming(self):
        return self.get_queryset().filter(end__gte=timezone.now())

    def past(self):
        return self.get_queryset().filter(end__lt=timezone.now())


class Event(TimeStampedModel):
    community = models.ForeignKey('communities.Community', related_name='events')
    name = models.CharField(max_length=64)
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField(max_length=64, help_text="Note: changing the slug will change the URL of the event")
    begin = models.DateTimeField(default=timezone.now)
    end = models.DateTimeField(default=timezone.now)
    twitter_hashtag = models.CharField(
        max_length=140, null=True, blank=True, help_text='Twitter hashtag of this event (without leading #)')
    objects = EventManager()

    def __str__(self):
        return self.name

    def is_upcoming(self):
        return self.end >= timezone.now()

    def is_past(self):
        return self.end < timezone.now()

    def rsvp_yes(self):
        return self.rsvps.filter(coming=True)

    def rsvp_no(self):
        return self.rsvps.filter(coming=False)

    def save(self, *args, **kwargs):
        if not self.id:
            slug = "{}-{}".format(slugify(self.name), str(self.begin.date()))
            if Event.objects.filter(slug=slug, community=self.community):
                # use datetime, because date was not unique
                slug = "{}-{}".format(slugify(self.name), slugify(self.begin))
            self.slug = slug

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('event_detail', kwargs={'slug': self.slug,
                                               'community_slug': self.community.slug})

    def get_update_url(self):
        return reverse('event_update', kwargs={'slug': self.slug,
                                               'community_slug': self.community.slug})

    def get_comment_create_url(self):
        return reverse('eventcomment_create', kwargs={
            'slug': self.slug, 'community_slug': self.community.slug})

    def get_rsvp_yes_url(self):
        return reverse('event_rsvp', kwargs={'slug': self.slug,
                                             'community_slug': self.community.slug,
                                             'answer': 'yes'})

    def get_rsvp_no_url(self):
        return reverse('event_rsvp', kwargs={'slug': self.slug,
                                             'community_slug': self.community.slug,
                                             'answer': 'no'})

    def get_rsvp_reset_url(self):
        return reverse('event_rsvp', kwargs={'slug': self.slug,
                                             'community_slug': self.community.slug,
                                             'answer': 'reset'})

    class Meta:
        ordering = ['begin', 'name']
        unique_together = ('community', 'slug')


@rules.predicate
def can_edit_event(user, event):
    if not user or not event:
        return False

    return user.has_perm('community.can_edit', event.community)

rules.add_perm('event.can_edit', can_edit_event)


@rules.predicate
def is_subscriber(user, event):
    if not user or not event:
        return False

    return user in event.community.subscribers.all()

rules.add_perm('event.can_rsvp', is_subscriber)
rules.add_perm('event.can_create_comment', is_subscriber)


class EventRSVP(TimeStampedModel):
    event = models.ForeignKey('Event', related_name='rsvps')
    user = models.ForeignKey('auth.User', related_name='rsvps')
    coming = models.BooleanField()

    class Meta:
        ordering = ('-coming', 'user')
        unique_together = (
            ('event', 'user'),
        )


class EventComment(TimeStampedModel):
    event = models.ForeignKey('Event', related_name='comments')
    user = models.ForeignKey('auth.User', related_name='comments')
    text = models.TextField()
