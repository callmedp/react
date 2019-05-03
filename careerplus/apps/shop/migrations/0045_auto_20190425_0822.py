# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2019-04-25 02:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('partner', '0013_auto_20190425_0822'),
        ('shop', '0044_auto_20190411_1731'),
    ]

    operations = [
        migrations.AddField(
            model_name='shineprofiledata',
            name='vendor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vendor', to='partner.Vendor', verbose_name='Vendor'),
        ),
        migrations.AlterField(
            model_name='product',
            name='sub_type_flow',
            field=models.IntegerField(choices=[(501, 'Featured Profile'), (502, 'Jobs on the Move'), (503, 'Priority Applicant'), (1601, 'Free Test'), (1602, 'Paid Test')], default=-1),
        ),
        migrations.AlterField(
            model_name='product',
            name='type_flow',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Default'), (1, 'Resume Writing India'), (2, 'Courses'), (3, 'Resume Critique'), (4, 'International Profile Update'), (5, 'Featured Profile'), (6, 'IDfy Assessment'), (7, 'Resume Booster'), (8, 'Linkedin'), (9, 'Round One'), (10, 'StudyMate'), (11, 'TSSC'), (12, 'Country Specific Resume'), (13, 'Executive Bio,Portfolio,Visual Resume,Cover Letter,Second Regular Resume'), (14, 'University Courses'), (15, 'Resume Booster International'), (16, 'Assessment and Certifications')], default=0, verbose_name='Flow'),
        ),
        migrations.AlterField(
            model_name='productscreen',
            name='sub_type_flow',
            field=models.IntegerField(choices=[(501, 'Featured Profile'), (502, 'Jobs on the Move'), (503, 'Priority Applicant'), (1601, 'Free Test'), (1602, 'Paid Test')], default=-1),
        ),
        migrations.AlterField(
            model_name='productscreen',
            name='type_flow',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Default'), (1, 'Resume Writing India'), (2, 'Courses'), (3, 'Resume Critique'), (4, 'International Profile Update'), (5, 'Featured Profile'), (6, 'IDfy Assessment'), (7, 'Resume Booster'), (8, 'Linkedin'), (9, 'Round One'), (10, 'StudyMate'), (11, 'TSSC'), (12, 'Country Specific Resume'), (13, 'Executive Bio,Portfolio,Visual Resume,Cover Letter,Second Regular Resume'), (14, 'University Courses'), (15, 'Resume Booster International'), (16, 'Assessment and Certifications')], default=0, verbose_name='Flow'),
        ),
        migrations.AlterField(
            model_name='shineprofiledata',
            name='sub_type_flow',
            field=models.IntegerField(choices=[(501, 'Featured Profile'), (502, 'Jobs on the Move'), (503, 'Priority Applicant'), (1601, 'Free Test'), (1602, 'Paid Test')]),
        ),
        migrations.AlterField(
            model_name='shineprofiledata',
            name='type_flow',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Default'), (1, 'Resume Writing India'), (2, 'Courses'), (3, 'Resume Critique'), (4, 'International Profile Update'), (5, 'Featured Profile'), (6, 'IDfy Assessment'), (7, 'Resume Booster'), (8, 'Linkedin'), (9, 'Round One'), (10, 'StudyMate'), (11, 'TSSC'), (12, 'Country Specific Resume'), (13, 'Executive Bio,Portfolio,Visual Resume,Cover Letter,Second Regular Resume'), (14, 'University Courses'), (15, 'Resume Booster International'), (16, 'Assessment and Certifications')], verbose_name='Flow'),
        ),
        migrations.AlterUniqueTogether(
            name='shineprofiledata',
            unique_together=set([('type_flow', 'sub_type_flow', 'vendor')]),
        ),
    ]
