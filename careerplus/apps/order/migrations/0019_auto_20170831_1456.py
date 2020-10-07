# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-08-31 09:26
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0018_order_tax_config'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='cart',
        ),
        migrations.RemoveField(
            model_name='order',
            name='instrument_issue_date',
        ),
        migrations.RemoveField(
            model_name='order',
            name='instrument_issuer',
        ),
        migrations.RemoveField(
            model_name='order',
            name='instrument_number',
        ),
        migrations.RemoveField(
            model_name='order',
            name='payment_date',
        ),
        migrations.RemoveField(
            model_name='order',
            name='payment_mode',
        ),
        migrations.RemoveField(
            model_name='order',
            name='txn',
        ),
    ]
