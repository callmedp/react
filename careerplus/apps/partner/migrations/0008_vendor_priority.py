# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-01-18 11:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partner', '0007_auto_20170809_1504'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor',
            name='priority',
            field=models.IntegerField(default=0),
        ),
    ]
