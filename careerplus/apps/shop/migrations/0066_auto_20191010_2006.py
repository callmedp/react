# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2019-10-10 14:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0065_merge_20190927_1721'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='sub_type_flow',
            field=models.IntegerField(choices=[(1601, 'Free Test'), (1602, 'Paid Test'), (200, 'Default'), (201, 'Certificate Product'), (501, 'Featured Profile'), (502, 'Jobs on the Move'), (503, 'Priority Applicant')], default=-1),
        ),
        migrations.AlterField(
            model_name='productscreen',
            name='sub_type_flow',
            field=models.IntegerField(choices=[(1601, 'Free Test'), (1602, 'Paid Test'), (200, 'Default'), (201, 'Certificate Product'), (501, 'Featured Profile'), (502, 'Jobs on the Move'), (503, 'Priority Applicant')], default=-1),
        ),
        migrations.AlterField(
            model_name='shineprofiledata',
            name='sub_type_flow',
            field=models.IntegerField(choices=[(1601, 'Free Test'), (1602, 'Paid Test'), (200, 'Default'), (201, 'Certificate Product'), (501, 'Featured Profile'), (502, 'Jobs on the Move'), (503, 'Priority Applicant')]),
        ),
    ]
