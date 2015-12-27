from django.db import models
from django_extensions.db.models import TimeStampedModel


class Community(TimeStampedModel):
    name = models.CharField(max_length=64)
    slug = models.SlugField(max_length=64)
    subscribers = models.ManyToManyField('auth.User', through='CommunitySubscription')

    def __str__(self):
        return self.name


class CommunitySubscription(TimeStampedModel):
    ROLE_CHOICES = (
        ('owner', 'Owner'),
        ('admin', 'Administrator'),
        ('subscriber', 'Subscriber'),
    )

    community = models.ForeignKey(Community)
    user = models.ForeignKey('auth.User')
    role = models.CharField(max_length=64, choices=ROLE_CHOICES)
