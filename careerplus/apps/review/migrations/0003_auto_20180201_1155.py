# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-02-01 06:25
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0002_auto_20170718_1236'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='review',
            options={'ordering': ['-created'], 'permissions': (('can_change_review_queue', 'Can Change Review Queue'),)},
        ),
    ]
