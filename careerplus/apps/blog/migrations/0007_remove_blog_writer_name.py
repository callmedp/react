# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-14 18:24
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20170414_1606'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='writer_name',
        ),
    ]
