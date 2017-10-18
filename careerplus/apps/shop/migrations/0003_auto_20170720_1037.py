# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-20 05:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('geolocation', '0002_country_profile_url'),
        ('shop', '0002_auto_20170718_1523'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='country_name',
        ),
        migrations.RemoveField(
            model_name='product',
            name='profile_website',
        ),
        migrations.AddField(
            model_name='product',
            name='profile_country',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='geolocation.Country'),
        ),
    ]
