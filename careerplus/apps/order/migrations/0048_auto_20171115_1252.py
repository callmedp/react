# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-11-15 07:22
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0047_auto_20171107_1912'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['-date_placed'], 'permissions': (('can_show_order_queue', 'Can Show Order Queue'), ('can_show_all_order', 'Can View All Orders'), ('can_show_paid_order', 'Can View Only Paid Orders'), ('can_show_welcome_queue', 'Can Show Welcome Queue'), ('can_view_order_detail', 'Can View Order Deatil'), ('can_mark_order_as_paid', 'Can Mark Order As Paid'), ('can_search_order_from_console', 'Can Search Order From Console')), 'verbose_name': 'Order', 'verbose_name_plural': 'Orders'},
        ),
    ]
