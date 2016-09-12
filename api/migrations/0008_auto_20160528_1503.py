# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-28 15:03
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0007_participantsinevent_is_accepted'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='participantsinevent',
            name='user',
        ),
        migrations.AddField(
            model_name='participantsinevent',
            name='user_joined',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='participatingUser', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='participantsinevent',
            name='date_joined',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='participantsinevent',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participatingEvent', to='api.Event'),
        ),
    ]
