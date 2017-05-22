# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-22 05:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(editable=False)),
                ('modified', models.DateTimeField(blank=True, null=True)),
                ('number', models.CharField(db_index=True, max_length=128, unique=True, verbose_name='Order number')),
                ('site', models.PositiveSmallIntegerField(choices=[(0, 'Shinelearning'), (1, 'Cpcrm')], default=0)),
                ('candidate_id', models.CharField(max_length=255, null=True, verbose_name='Customer ID')),
                ('email', models.CharField(max_length=255, null=True, verbose_name='Customer Email')),
                ('first_name', models.CharField(max_length=255, null=True, verbose_name='First Name')),
                ('last_name', models.CharField(max_length=255, null=True, verbose_name='Last Name')),
                ('country_code', models.CharField(max_length=15, null=True, verbose_name='Country Code')),
                ('mobile', models.CharField(max_length=15, null=True)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('pincode', models.CharField(blank=True, max_length=15, null=True)),
                ('state', models.CharField(blank=True, max_length=255, null=True)),
                ('country', models.CharField(max_length=200, null=True)),
                ('total_incl_tax', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Order total (inc. tax)')),
                ('total_excl_tax', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Order total (excl. tax)')),
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'Unpaid'), (1, 'Paid'), (2, 'InProcess'), (3, 'Closed'), (4, 'Archive')], default=0)),
                ('date_placed', models.DateTimeField(db_index=True)),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
                'ordering': ['-date_placed'],
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('partner_name', models.CharField(blank=True, max_length=128, verbose_name='Partner name')),
                ('title', models.CharField(max_length=255, verbose_name='Product title')),
                ('upc', models.CharField(blank=True, max_length=128, null=True, verbose_name='UPC')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='Quantity')),
                ('oi_price_incl_tax', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Price (inc. tax)')),
                ('oi_price_excl_tax', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Price (excl. tax)')),
                ('oi_price_before_discounts_incl_tax', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Price before discounts (inc. tax)')),
                ('oi_price_before_discounts_excl_tax', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Price before discounts (excl. tax)')),
                ('unit_price_incl_tax', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, verbose_name='Unit Price (inc. tax)')),
                ('unit_price_excl_tax', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, verbose_name='Unit Price (excl. tax)')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orderitems', to='order.Order', verbose_name='Order')),
            ],
            options={
                'verbose_name': 'Order Item',
                'verbose_name_plural': 'Order Items',
                'ordering': ['pk'],
            },
        ),
    ]
