# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-10 14:54
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20160510_1653'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='date_end',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 10, 14, 54, 1, 8000, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='event',
            name='date_start',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 10, 14, 54, 1, 8000, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='event',
            name='date_updated',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 10, 14, 54, 1, 9000, tzinfo=utc)),
        ),
    ]