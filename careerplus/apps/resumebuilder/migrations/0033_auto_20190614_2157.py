# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2019-06-14 16:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resumebuilder', '0032_auto_20190613_2054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='extracurricular',
            field=models.TextField(blank=True, null=True, verbose_name='Extra Curricular'),
        ),
    ]
