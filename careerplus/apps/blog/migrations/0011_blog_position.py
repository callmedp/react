# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2020-01-15 12:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_auto_20191011_1141'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='position',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
