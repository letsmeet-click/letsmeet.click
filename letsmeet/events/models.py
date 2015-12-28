import rules
from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django_extensions.db.models import TimeStampedModel


class Event(TimeStampedModel):
    community = models.ForeignKey('communities.Community', related_name='events')
    name = models.CharField(max_length=64, unique=True)
    slug = models.SlugField(max_length=64, unique=True)
    begin = models.DateTimeField(default=timezone.now)
    end = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    def rsvp_yes(self):
        return self.rsvps.filter(coming=True)

    def rsvp_no(self):
        return self.rsvps.filter(coming=False)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('event_detail', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('event_update', kwargs={'slug': self.slug})

    def get_rsvp_yes_url(self):
        return reverse('event_rsvp', kwargs={'slug': self.slug, 'answer': 'yes'})

    def get_rsvp_no_url(self):
        return reverse('event_rsvp', kwargs={'slug': self.slug, 'answer': 'no'})

    def get_rsvp_reset_url(self):
        return reverse('event_rsvp', kwargs={'slug': self.slug, 'answer': 'reset'})

    class Meta:
        ordering = ['name']


@rules.predicate
def can_edit_event(user, event):
    if not user or not event:
        return False

    return user.has_perm('community.can_edit', event.community)

rules.add_perm('event.can_edit', can_edit_event)


@rules.predicate
def can_rsvp_event(user, event):
    if not user or not event:
        return False

    return user in event.community.subscribers.all()

rules.add_perm('event.can_rsvp', can_rsvp_event)


class EventRSVP(TimeStampedModel):
    event = models.ForeignKey('Event', related_name='rsvps')
    user = models.ForeignKey('auth.User', related_name='rsvps')
    coming = models.BooleanField()

    class Meta:
        ordering = ('-coming', 'user')
        unique_together = (
            ('event', 'user'),
        )
