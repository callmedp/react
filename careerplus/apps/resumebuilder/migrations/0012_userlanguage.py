# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2019-03-06 06:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('resumebuilder', '0011_user_extra_info'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserLanguage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Language Name')),
                ('proficiency', models.IntegerField(default=3, verbose_name='Proficiency')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resumebuilder.User', verbose_name='User')),
            ],
        ),
    ]
