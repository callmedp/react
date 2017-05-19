# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-18 12:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('order', '0001_initial'),
        ('partner', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='partner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_items', to='partner.Vendor', verbose_name='Partner'),
        ),
    ]
