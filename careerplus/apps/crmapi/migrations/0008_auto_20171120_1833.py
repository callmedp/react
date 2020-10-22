# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-11-20 13:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crmapi', '0007_auto_20171117_1525'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userquries',
            name='lead_source',
            field=models.SmallIntegerField(choices=[(0, 'Default'), (1, 'Skill Page'), (2, 'Course Detail Page'), (8, 'Resume Detail Page'), (3, 'Contact Us Page'), (4, 'SEM'), (7, 'CMS Page')], default=0),
        ),
    ]
