# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2019-10-10 08:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0084_auto_20191009_1542'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ltvmonthlyrecord',
            old_name='candidate_id_ltv_mapping',
            new_name='candidate_ids',
        ),
        migrations.RemoveField(
            model_name='ltvmonthlyrecord',
            name='crm_order_count',
        ),
        migrations.RemoveField(
            model_name='ltvmonthlyrecord',
            name='crm_users',
        ),
        migrations.RemoveField(
            model_name='ltvmonthlyrecord',
            name='learning_order_count',
        ),
        migrations.RemoveField(
            model_name='ltvmonthlyrecord',
            name='learning_users',
        ),
        migrations.RemoveField(
            model_name='ltvmonthlyrecord',
            name='total_item_count',
        ),
        migrations.RemoveField(
            model_name='ltvmonthlyrecord',
            name='total_order_count',
        ),
        migrations.RemoveField(
            model_name='ltvmonthlyrecord',
            name='total_users',
        ),
        migrations.AddField(
            model_name='ltvmonthlyrecord',
            name='crm_order_ids',
            field=models.TextField(default=True, null=True),
        ),
        migrations.AddField(
            model_name='ltvmonthlyrecord',
            name='learning_order_ids',
            field=models.TextField(default=True, null=True),
        ),
    ]
