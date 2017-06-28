# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-06-28 18:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0003_location_homepage'),
        ('events', '0010_event_max_attendees'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='eventrsvp',
            options={'ordering': ('-coming', 'user__username')},
        ),
        migrations.AddField(
            model_name='event',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='events', to='locations.Location'),
        ),
        migrations.AlterField(
            model_name='event',
            name='max_attendees',
            field=models.PositiveIntegerField(blank=True, help_text='Optional maximum number of attendees for this event. Leave blank for no limit.', null=True),
        ),
    ]
