# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2019-04-16 08:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resumebuilder', '0026_candidatelanguage_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidateachievement',
            name='order',
            field=models.IntegerField(default=0, verbose_name='Order'),
        ),
        migrations.AddField(
            model_name='candidatecertification',
            name='order',
            field=models.IntegerField(default=0, verbose_name='Order'),
        ),
        migrations.AddField(
            model_name='candidateeducation',
            name='order',
            field=models.IntegerField(default=0, verbose_name='Order'),
        ),
        migrations.AddField(
            model_name='candidateexperience',
            name='order',
            field=models.IntegerField(default=0, verbose_name='Order'),
        ),
        migrations.AddField(
            model_name='candidateproject',
            name='order',
            field=models.IntegerField(default=0, verbose_name='Order'),
        ),
        migrations.AddField(
            model_name='candidatereference',
            name='order',
            field=models.IntegerField(default=0, verbose_name='Order'),
        ),
        migrations.AddField(
            model_name='candidatesociallink',
            name='order',
            field=models.IntegerField(default=0, verbose_name='Order'),
        ),
        migrations.AddField(
            model_name='skill',
            name='order',
            field=models.IntegerField(default=0, verbose_name='Order'),
        ),
    ]
