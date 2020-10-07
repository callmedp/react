# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-07-12 07:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0059_auto_20180704_1750'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='alt_email',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Alternate Email'),
        ),
        migrations.AddField(
            model_name='order',
            name='alt_mobile',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='Alternate Mobile'),
        ),
    ]
