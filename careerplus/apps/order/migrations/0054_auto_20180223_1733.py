# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-02-23 12:03
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0053_auto_20180223_1326'),
    ]

    operations = [
        migrations.AddField(
            model_name='welcomecalloperation',
            name='order',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='order.Order'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='welcomecalloperation',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='wop_created_by', to=settings.AUTH_USER_MODEL, verbose_name='Created By'),
        ),
    ]
