# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2019-03-07 12:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0038_subcategory_product_mapped'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subcategory',
            old_name='product_mapped',
            new_name='products_mapped',
        ),
    ]
