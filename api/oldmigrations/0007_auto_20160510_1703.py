# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-10 15:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20160510_1701'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participantsinevent',
            name='date_joined',
            field=models.DateTimeField(blank=True),
        ),
    ]
