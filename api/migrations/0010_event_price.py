# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-31 13:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_auto_20160528_1826'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='price',
            field=models.FloatField(blank=True, default=2.0),
            preserve_default=False,
        ),
    ]
