# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-09-26 15:45
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0003_rewardpoint_cw_id'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='wallet',
            options={'ordering': ['-created'], 'verbose_name': 'Wallet', 'verbose_name_plural': 'Wallets'},
        ),
        migrations.AlterModelOptions(
            name='wallettransaction',
            options={'ordering': ('-created',), 'verbose_name': 'Wallet Transaction', 'verbose_name_plural': 'Wallet Transactions'},
        ),
    ]
