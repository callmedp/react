# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-10-05 10:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0038_merge_20171005_1603'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='oi_draft',
            field=models.FileField(blank=True, max_length=255, null=True, upload_to='oi_draft/'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='oi_resume',
            field=models.FileField(blank=True, default='', max_length=255, null=True, upload_to='oi_resume/'),
        ),
    ]
