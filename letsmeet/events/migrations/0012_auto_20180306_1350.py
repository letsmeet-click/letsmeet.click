# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-06 12:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0011_auto_20170628_2027'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='publish',
            field=models.BooleanField(default=True, help_text='Should this event be published elsewhere?'),
        ),
        migrations.AlterField(
            model_name='event',
            name='begin',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.TextField(blank=True, help_text='You can write markdown here!', null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='end',
            field=models.DateTimeField(),
        ),
    ]