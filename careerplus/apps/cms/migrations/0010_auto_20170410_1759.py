# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-10 12:29
from __future__ import unicode_literals

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0009_auto_20170410_1732'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='doc',
            field=models.FileField(max_length=200, storage=django.core.files.storage.FileSystemStorage(location='download/'), upload_to='', verbose_name='Document'),
        ),
    ]
