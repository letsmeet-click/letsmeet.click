import rules

from django.core.urlresolvers import reverse
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
from django.utils import timezone
from django_extensions.db.models import TimeStampedModel


class CommunityManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class Community(TimeStampedModel):
    name = models.CharField(max_length=64, unique=True)
    slug = models.SlugField(max_length=64, unique=True)
    description = models.TextField(null=True, blank=True)
    subscribers = models.ManyToManyField('auth.User', through='CommunitySubscription', related_name='communities')
    cname = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="CNAME",
        validators=[RegexValidator(r'[a-zA-Z0-9-\.\ ]+')],
        help_text="use your own domain to redirect to this community."
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

    is_deleted = models.BooleanField(default=False)

    objects = CommunityManager()
    default = models.Manager()   # the default manager

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def subscribe_user(self, user):
        subscription, created = CommunitySubscription.objects.get_or_create(
            user=user, community=self,
        )
        if created:
            recipients = User.objects.filter(pk__in=self.community_subscriptions.filter(
                role__in=[CommunitySubscription.ROLE_ADMIN, CommunitySubscription.ROLE_OWNER],
                user__userprofile__notify_on_new_subscription=True,
            ).values_list('user__pk', flat=True))
            # send notification mail to all subscribers
            if recipients:
                from main.utils import send_notification
                send_notification(
                    recipients=recipients,
                    subject='New subscription to community {}'.format(self.name),
                    template='communities/mails/new_subscription.txt',
                    context={'subscription': subscription},
                )

        return subscription

    def get_user_subscription(self, user):
        """returns the CommunitySubscription object of the user. None if user is not subscribed"""
        return self.community_subscriptions.filter(user=user).first()

    def get_next_event(self):
        if not hasattr(self, '_next_event'):
            self._next_event = self.events.filter(begin__gte=timezone.now()).order_by('begin').first()

        return self._next_event

    def get_ical_url(self):
        return reverse('community_events_ical_feed', kwargs={'community_slug': self.slug})

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
        ordering = ['slug']
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
        ordering = ['role', 'user']
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
        community_subscription = community.community_subscriptions.get(user=user)
        if community_subscription:
            return community_subscription.role == CommunitySubscription.ROLE_OWNER
    except CommunitySubscription.DoesNotExist:
        pass  # yes, quantifiedcode, this is intentional
    return False

rules.add_perm('community.can_create_event', can_create_community_event)


@rules.predicate
def is_last_owner(user, community_subscription):
    if not user or not community_subscription:
        return False

    return community_subscription.role == CommunitySubscription.ROLE_OWNER and \
        CommunitySubscription.objects.filter(
            community=community_subscription.community, role=CommunitySubscription.ROLE_OWNER).count() == 1

rules.add_rule('is_last_owner', is_last_owner)
rules.add_rule('can_unsubscribe', ~is_last_owner)


@rules.predicate
def can_set_owner(user, community):
    if not user or not community:
        return False

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
