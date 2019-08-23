# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2019-08-21 10:29
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('order', '0079_auto_20190821_1559'),
        ('console', '0002_auto_20170707_1804'),
    ]

    operations = [
        migrations.CreateModel(
            name='CandidateAgentInteraction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_on', models.DateTimeField(auto_now=True, null=True)),
                ('queue_name', models.PositiveSmallIntegerField(choices=[(0, 'Default'), (1, 'Order List'), (2, 'Midout List'), (3, 'Inbox'), (4, 'Replaced Order'), (5, 'Approval'), (6, 'Approved'), (7, 'Rejected by Admin'), (8, 'Rejected by Candidate'), (9, 'Booster'), (10, 'Whatsapp Jobs'), (11, 'Certification/Assessment'), (12, 'Domestic Profile Update'), (13, 'Domestic Profile Approval'), (14, 'Domestic Profile Initiated'), (15, 'International Profile Update'), (16, 'International Profile Approval'), (17, 'Allocated'), (18, 'Closed Orderitems'), (19, 'Partner Inbox'), (20, 'Hold Items'), (21, 'Verification Reports'), (22, 'Order Detail'), (23, 'Linkedin Inbox '), (24, 'Linkedin Rejected by Candidate'), (25, 'Linkedin Rejected by Admin'), (26, 'Linkedin Approval')], default=0)),
                ('recording_url', models.TextField(blank=True, null=True, verbose_name='Call Recording')),
                ('candidate_id', models.CharField(blank=True, max_length=255, null=True, verbose_name='Customer ID')),
                ('called_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='called_by', to=settings.AUTH_USER_MODEL)),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='order.OrderItem')),
            ],
        ),
    ]
