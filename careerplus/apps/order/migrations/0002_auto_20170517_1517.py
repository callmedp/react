# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-17 09:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='customer_id',
            new_name='candidate_id',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='cutomer_email',
            new_name='email',
        ),
        migrations.AddField(
            model_name='order',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='country',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='country_code',
            field=models.CharField(max_length=15, null=True, verbose_name='Country Code'),
        ),
        migrations.AddField(
            model_name='order',
            name='first_name',
            field=models.CharField(max_length=255, null=True, verbose_name='First Name'),
        ),
        migrations.AddField(
            model_name='order',
            name='last_name',
            field=models.CharField(max_length=255, null=True, verbose_name='Last Name'),
        ),
        migrations.AddField(
            model_name='order',
            name='mobile',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='pincode',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='state',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='site',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Shinelearning'), (1, 'Cpcrm')], default=0),
        ),
    ]
