# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2019-07-30 11:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0052_merge_20190730_1643'),
    ]

    operations = [
        migrations.AddField(
            model_name='productuserprofile',
            name='onboard',
            field=models.BooleanField(default=False),
        ),
    ]
