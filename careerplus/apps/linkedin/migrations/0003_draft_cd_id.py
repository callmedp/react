# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-09-19 06:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('linkedin', '0002_auto_20170801_1221'),
    ]

    operations = [
        migrations.AddField(
            model_name='draft',
            name='cd_id',
            field=models.IntegerField(blank=True, editable=False, null=True, verbose_name='CP Draft'),
        ),
    ]
