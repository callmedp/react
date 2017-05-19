# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-18 12:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(editable=False)),
                ('modified', models.DateTimeField(blank=True, null=True)),
                ('owner_id', models.CharField(max_length=255, null=True, verbose_name='Owner ID')),
                ('owner_email', models.CharField(max_length=255, null=True, verbose_name='Owner Email')),
                ('session_id', models.CharField(blank=True, max_length=255, null=True)),
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'Open - currently active but no owner'), (1, 'Merged - merged in other cart'), (2, 'Saved - currently active but with owner'), (3, 'Express - currently active'), (4, 'Frozen - the cart cannot be modified'), (5, 'Closed - order has been made'), (6, 'Archive - cart need to be archived')], default=0, verbose_name='Status')),
                ('is_submitted', models.BooleanField(default=False)),
                ('date_merged', models.DateTimeField(blank=True, null=True, verbose_name='Date merged')),
                ('date_submitted', models.DateTimeField(blank=True, null=True, verbose_name='Date submitted')),
                ('date_frozen', models.DateTimeField(blank=True, null=True, verbose_name='Date frozen')),
                ('date_closed', models.DateTimeField(blank=True, null=True, verbose_name='Date closed')),
            ],
            options={
                'verbose_name': 'Cart',
                'verbose_name_plural': 'Carts',
            },
        ),
        migrations.CreateModel(
            name='LineItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(editable=False)),
                ('modified', models.DateTimeField(blank=True, null=True)),
                ('type_item', models.PositiveSmallIntegerField(default=0)),
                ('reference', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='Quantity')),
                ('price_excl_tax', models.DecimalField(decimal_places=2, max_digits=12, null=True, verbose_name='Price excl. Tax')),
                ('price_incl_tax', models.DecimalField(decimal_places=2, max_digits=12, null=True, verbose_name='Price incl. Tax')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lineitems', to='cart.Cart', verbose_name='Cart')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cart.LineItem')),
            ],
            options={
                'ordering': ['modified', 'pk'],
                'verbose_name': 'Cart Line Item',
                'verbose_name_plural': 'Cart Line Items',
            },
        ),
        migrations.CreateModel(
            name='ShippingDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('candidate_id', models.CharField(max_length=255, unique=True, verbose_name='Candidate Id')),
                ('first_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='First Name')),
                ('last_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Last Name')),
                ('email', models.EmailField(max_length=255, null=True)),
                ('mobile', models.CharField(max_length=15, null=True)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('pincode', models.CharField(blank=True, max_length=15, null=True)),
                ('city', models.CharField(blank=True, max_length=255, null=True)),
                ('state', models.CharField(blank=True, max_length=255, null=True)),
                ('landmark', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
    ]
