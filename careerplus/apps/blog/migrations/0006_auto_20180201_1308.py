# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-02-01 07:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20171122_0009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='visibility',
            field=models.PositiveIntegerField(choices=[(1, 'ShineLearning'), (2, 'TalentEconomy')], default=1, help_text='sites where blog published.', verbose_name='Site Visibilty'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='summary',
            field=models.TextField(blank=True, default='', verbose_name='Summarys Article'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='visibility',
            field=models.PositiveIntegerField(choices=[(1, 'ShineLearning'), (2, 'TalentEconomy')], default=1, help_text='sites where blog published.', verbose_name='Site Visibilty'),
        ),
        migrations.AlterField(
            model_name='category',
            name='visibility',
            field=models.PositiveIntegerField(choices=[(1, 'ShineLearning'), (2, 'TalentEconomy')], default=1, help_text='sites where blog published.', verbose_name='Site Visibilty'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='visibility',
            field=models.PositiveIntegerField(choices=[(1, 'ShineLearning'), (2, 'TalentEconomy')], default=1, help_text='sites where blog published.', verbose_name='Site Visibilty'),
        ),
    ]
