# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-03 21:33
from __future__ import unicode_literals

from django.db import migrations
import stdimage.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=stdimage.models.StdImageField(help_text='Image should be square. Otherwise it will be cropped.', upload_to='avatars'),
        ),
    ]
