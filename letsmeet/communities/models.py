import rules

from django.db import models
from django.core.urlresolvers import reverse
from django.core.validators import RegexValidator
from django.template.defaultfilters import slugify
from django_extensions.db.models import TimeStampedModel


class Community(TimeStampedModel):
    name = models.CharField(max_length=64, unique=True)
    slug = models.SlugField(max_length=64, unique=True)
    subscribers = models.ManyToManyField('auth.User', through='CommunitySubscription', related_name='communities')
    cname = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="CNAME",
        validators=[RegexValidator(r'[a-zA-Z0-9-\.]+')],
    )

    twitter = models.CharField(max_length=128, blank=True, null=True,
                               help_text="Twitter username (without leading @)",
                               validators=[RegexValidator(r'[a-zA-Z0-9_]+')],)
    github = models.CharField(max_length=128, blank=True, null=True,
                              help_text="GitHub username or organisation name")
    homepage = models.URLField(max_length=128, blank=True, null=True,
                               help_text="URL of homepage (including http://)")
    irc_channel = models.CharField(
        max_length=128, blank=True, null=True, verbose_name="IRC channel",
        help_text='IRC channel name',
    )
    irc_network = models.CharField(
        max_length=128, blank=True, null=True,
        help_text='Network the IRC channel is located on (e.g. "Freenode")',
        verbose_name='IRC network',
    )
    slack = models.CharField(max_length=128, blank=True, null=True,
                             help_text="Slack organisation name")

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
        user = community.community_subscriptions.get(user=user)
        if user:
            return user.role == CommunitySubscription.ROLE_OWNER
    except CommunitySubscription.DoesNotExist:
        pass
    return False

rules.add_perm('community.can_create_event', can_create_community_event)


@rules.predicate
def is_last_owner(user, community_subscription):
    if not user or not community_subscription:
        return False

    return not (community_subscription.role == CommunitySubscription.ROLE_OWNER and
                CommunitySubscription.objects.filter(
                    community=community_subscription.community, role=CommunitySubscription.ROLE_OWNER).count() == 1)

rules.add_rule('is_last_owner', is_last_owner)
rules.add_rule('can_unsubscribe', ~is_last_owner)


@rules.predicate
def can_set_owner(user, community):
    if not user or not community:
        return False

    print('can_set_owner')
    try:
        return community.community_subscriptions.get(user=user).role == CommunitySubscription.ROLE_OWNER
    except CommunitySubscription.DoesNotExist:
        return False

rules.add_perm('community.can_set_owner', can_set_owner)


@rules.predicate
def can_set_admin(user, community):
    if not user or not community:
        return False

    try:
        return community.community_subscriptions.get(user=user).role in [
            CommunitySubscription.ROLE_OWNER, CommunitySubscription.ROLE_ADMIN]
    except CommunitySubscription.DoesNotExist:
        return False

rules.add_perm('community.can_set_admin', can_set_admin)
rules.add_perm('community.can_set_subscriber', can_set_admin)
