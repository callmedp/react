# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-10-23 06:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crmapi', '0004_userquries_path'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userquries',
            name='lead_source',
            field=models.SmallIntegerField(choices=[(0, 'Default'), (1, 'Skill Page'), (2, 'Detail Page'), (3, 'Contact Us Page'), (6, 'Marketing')], default=0),
        ),
    ]