from django.contrib.gis.db import models
from django.template.defaultfilters import slugify
from django_extensions.db.models import TimeStampedModel


class Location(TimeStampedModel):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True,
                             help_text='Are there special requirements for organizers at this location?')
    geo_location = models.PointField(srid=4326, blank=True, null=True)
    city = models.CharField(max_length=1000, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    class Meta:
        ordering = ['slug']
