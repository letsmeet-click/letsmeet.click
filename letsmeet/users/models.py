import rules
from django.core.urlresolvers import reverse
from django.db import models
from django_extensions.db.models import TimeStampedModel
from stdimage.models import StdImageField

from communities.models import CommunitySubscription
from events.models import Event, EventRSVP


class UserProfile(TimeStampedModel):
    user = models.OneToOneField('auth.User', unique=True)
    avatar = StdImageField(
        upload_to='avatars',
        variations={
            'thumbnail': (400, 400, True),
            'mini': (200, 200, True),
            'tiny': (100, 100, True),
            'micro': (40, 40, True),
        },
        help_text='Image should be square. Otherwise it will be cropped.'
    )
    notify_on_new_event = models.BooleanField(default=True)
    notify_on_new_subscription = models.BooleanField(default=True)
    notify_on_new_rsvp_for_organizer = models.BooleanField(default=True)
    notify_on_new_rsvp_for_attending = models.BooleanField(default=True)
    notify_on_new_comment = models.BooleanField(default=True)

    def get_next_event(self):
        return self.get_upcoming_events().order_by('begin').first()

    def get_upcoming_events(self):
        return Event.objects.upcoming()

    def get_next_yes_event(self):
        return self.get_upcoming_yes_events().order_by('begin').first()

    def get_upcoming_yes_events(self):
        return Event.objects.upcoming().filter(
            pk__in=EventRSVP.objects.filter(user=self.user, coming=True).values_list('event__pk', flat=True))

    def get_communitysubscriptions(self):
        return CommunitySubscription.objects.exclude(community__is_deleted=True).filter(user=self.user)

    @staticmethod
    def get_absolute_url():
        return reverse('profile')

    def __str__(self):
        return 'Profile of {}'.format(self.user.username)


@rules.predicate
def can_delete_user_social_auth(user, user_social_auth):
    return user_social_auth.allowed_to_disconnect(user, user_social_auth.provider)

rules.add_rule('can_delete_user_social_auth', can_delete_user_social_auth)
