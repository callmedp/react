# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2019-03-13 10:44
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0041_subcategory_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subcategory',
            name='name',
        ),
    ]
