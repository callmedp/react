# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2019-07-14 10:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0073_auto_20190712_1326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitemfeedback',
            name='category',
            field=models.SmallIntegerField(blank=True, choices=[(101, 'Rating'), (102, 'Referral'), (103, 'Shared Feedback'), (201, 'Unaware of the services'), (202, 'Login details not received'), (203, 'Draft not received'), (204, 'No relevancy'), (301, '100% job guarantee'), (302, 'Up-selling'), (303, 'Job&Interview guarantee'), (401, 'Call back scheduled'), (402, 'Not Responded')], null=True),
        ),
        migrations.AlterField(
            model_name='orderitemfeedback',
            name='resolution',
            field=models.SmallIntegerField(blank=True, choices=[(1, 'Shared the service details'), (2, 'Shared the login details'), (3, 'Shared the drafts'), (4, 'Swapping of the services'), (5, 'Complimentary service'), (6, 'Educate about the services')], null=True),
        ),
    ]
