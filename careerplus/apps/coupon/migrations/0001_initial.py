# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-07 12:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Name')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Campaign',
                'verbose_name_plural': 'Campaigns',
            },
        ),
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField(help_text='Arbitrary coupon value', verbose_name='Value')),
                ('code', models.CharField(blank=True, help_text='Leaving this field empty will generate a random code.', max_length=30, unique=True, verbose_name='Code')),
                ('type', models.CharField(choices=[('monetary', 'Money based coupon'), ('percentage', 'Percentage discount'), ('virtual_currency', 'Virtual currency')], max_length=20, verbose_name='Type')),
                ('user_limit', models.PositiveIntegerField(default=1, verbose_name='User limit')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('valid_until', models.DateTimeField(blank=True, help_text='Leave empty for coupons that never expire', null=True, verbose_name='Valid until')),
            ],
            options={
                'ordering': ['created_at'],
                'verbose_name': 'Coupon',
                'verbose_name_plural': 'Coupons',
            },
        ),
        migrations.CreateModel(
            name='CouponUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('redeemed_at', models.DateTimeField(blank=True, null=True, verbose_name='Redeemed at')),
                ('coupon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to='coupon.Coupon')),
            ],
        ),
    ]
