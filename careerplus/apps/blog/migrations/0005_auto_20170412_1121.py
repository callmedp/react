# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-12 05:51
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0004_auto_20170412_1100'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['-priority']},
        ),
        migrations.AddField(
            model_name='blog',
            name='user',
            field=models.ForeignKey(blank=True, help_text='for user or writer', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='blog',
            name='writer_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
