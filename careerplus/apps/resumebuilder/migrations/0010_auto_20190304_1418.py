# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2019-03-04 08:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resumebuilder', '0009_skill_proficiency'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='extra_info',
        ),
        migrations.AddField(
            model_name='user',
            name='extracurricular',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Extra Curricular'),
        ),
    ]
