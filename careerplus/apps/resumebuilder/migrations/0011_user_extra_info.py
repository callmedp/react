# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2019-03-04 08:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resumebuilder', '0010_auto_20190304_1418'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='extra_info',
            field=models.TextField(blank=True, null=True, verbose_name='Extra Information'),
        ),
    ]
