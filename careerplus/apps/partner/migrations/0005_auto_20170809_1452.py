# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-08-09 09:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partner', '0004_vendor_cp_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor',
            name='website',
            field=models.CharField(blank=True, help_text='Website', max_length=255, verbose_name='Website.'),
        ),
    ]
