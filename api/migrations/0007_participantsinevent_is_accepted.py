# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-28 14:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_remove_event_distance'),
    ]

    operations = [
        migrations.AddField(
            model_name='participantsinevent',
            name='is_accepted',
            field=models.BooleanField(default=False),
        ),
    ]
