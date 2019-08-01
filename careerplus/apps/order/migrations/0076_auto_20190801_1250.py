# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2019-08-01 07:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0075_auto_20190801_1003'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitemfeedbackoperation',
            name='oi_type',
            field=models.SmallIntegerField(choices=[(1, 'Order Item Updated'), (2, 'Feedback Message Updated')], default=1),
        ),
        migrations.AlterField(
            model_name='orderitemfeedbackoperation',
            name='customer_feedback',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.CustomerFeedback'),
        ),
    ]
