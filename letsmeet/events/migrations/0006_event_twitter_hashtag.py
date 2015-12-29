# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-29 03:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_eventcomment'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='twitter_hashtag',
            field=models.CharField(blank=True, help_text='Twitter hashtag of this event (without leading #)', max_length=140, null=True),
        ),
    ]
