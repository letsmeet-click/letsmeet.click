# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-07 21:44
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0008_auto_20151229_0323'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ['begin', 'name']},
        ),
    ]
