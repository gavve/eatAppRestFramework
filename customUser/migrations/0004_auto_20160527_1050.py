# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-27 10:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customUser', '0003_auto_20160527_1046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='profile_picture',
            field=models.ImageField(null=True, upload_to='profilepictures/'),
        ),
    ]
