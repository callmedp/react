# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2019-10-11 06:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0065_merge_20190927_1721'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='short_description',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='productscreen',
            name='short_description',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
