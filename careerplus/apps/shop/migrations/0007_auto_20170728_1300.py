# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-28 07:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_chapter_screenchapter'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chapter',
            options={'ordering': ['ordering'], 'permissions': (('console_add_chapter', 'Can Add Product Chapter From Console'), ('console_change_chapter', 'Can Change Product Chapter From Console'), ('console_moderate_chapter', 'Can Moderate Product Chapter From Console')), 'verbose_name': 'Chapter', 'verbose_name_plural': 'Chapters'},
        ),
        migrations.AlterModelOptions(
            name='screenchapter',
            options={'ordering': ['ordering'], 'verbose_name': 'Screen Chapter', 'verbose_name_plural': 'Screen Chapters'},
        ),
        migrations.AddField(
            model_name='screenchapter',
            name='chapter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orig_ch', to='shop.Chapter'),
        ),
    ]
