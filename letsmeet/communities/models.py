import rules

from django.db import models
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django_extensions.db.models import TimeStampedModel


class Community(TimeStampedModel):
    name = models.CharField(max_length=64, unique=True)
    slug = models.SlugField(max_length=64, unique=True)
    subscribers = models.ManyToManyField('auth.User', through='CommunitySubscription', related_name='communities')
    cname = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('community_detail', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('community_update', kwargs={'slug': self.slug})

    def get_subscribe_url(self):
        return reverse('community_subscribe', kwargs={'slug': self.slug})

    def get_unsubscribe_url(self):
        return reverse('community_unsubscribe', kwargs={'slug': self.slug})

    def get_event_create_url(self):
        return reverse('community_event_create', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Communities'


@rules.predicate
def can_edit_community(user, community):
    if not user or not community:
        return False

    try:
        return community.community_subscriptions.get(user=user).role == CommunitySubscription.ROLE_OWNER
    except CommunitySubscription.DoesNotExist:
        return False

rules.add_perm('community.can_edit', can_edit_community)


@rules.predicate
def can_create_community_event(user, community):
    if not user or not community:
        return False

    try:
        return community.community_subscriptions.get(user=user).role == CommunitySubscription.ROLE_OWNER
    except CommunitySubscription.DoesNotExist:
        return False

rules.add_perm('community.can_create_event', can_create_community_event)


@rules.predicate
def can_unsubscribe(user, community_subscription):
    if not user or not community_subscription:
        return False

    return not (community_subscription.role == CommunitySubscription.ROLE_OWNER and
                CommunitySubscription.objects.filter(
                    community=community_subscription.community, role=CommunitySubscription.ROLE_OWNER).count() == 1)

rules.add_rule('can_unsubscribe', can_unsubscribe)


class CommunitySubscription(TimeStampedModel):
    ROLE_OWNER = 'owner'
    ROLE_ADMIN = 'admin'
    ROLE_SUBSCRIBER = 'subscriber'
    ROLE_CHOICES = (
        (ROLE_OWNER, 'Owner'),
        (ROLE_ADMIN, 'Administrator'),
        (ROLE_SUBSCRIBER, 'Subscriber'),
    )

    community = models.ForeignKey(Community, related_name='community_subscriptions')
    user = models.ForeignKey('auth.User', related_name='community_subscriptions')
    role = models.CharField(max_length=64, choices=ROLE_CHOICES, default=ROLE_SUBSCRIBER)

    class Meta:
        ordering = ['user']
        unique_together = (
            ('community', 'user'),
        )
