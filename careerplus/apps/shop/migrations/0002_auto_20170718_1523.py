# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-18 09:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='country_name',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='profile_website',
            field=models.CharField(blank=True, help_text='comma separated(,) profile url, e.g. www.test1.com, www.test2.com', max_length=500, null=True),
        ),
    ]
