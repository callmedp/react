# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-07 12:34
from __future__ import unicode_literals

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Draft',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('candidate_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Name')),
                ('headline', models.CharField(blank=True, max_length=120, null=True, verbose_name='Headline')),
                ('summary', ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Summary')),
                ('profile_photo', models.CharField(blank=True, max_length=2000, null=True, verbose_name='Profile Photograph')),
                ('recommendation', models.CharField(blank=True, max_length=2000, null=True, verbose_name='Recommendations')),
                ('follow_company', models.CharField(blank=True, max_length=2000, null=True, verbose_name='Follow Companies')),
                ('join_group', models.CharField(blank=True, max_length=2000, null=True, verbose_name='Join Groups')),
                ('public_url', models.CharField(blank=True, max_length=2000, null=True, verbose_name='Public Urls')),
                ('key_skills', models.CharField(blank=True, help_text='comma separated(,) separated skills, e.g. java, python, ...', max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='School Name')),
                ('level', models.PositiveSmallIntegerField(choices=[('NA', '---------'), (0, 'School'), (1, 'College')], default=1)),
                ('degree', models.CharField(blank=True, max_length=100, null=True, verbose_name='Degree')),
                ('edu_desc', ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Education Description')),
                ('field', models.CharField(blank=True, max_length=100, null=True, verbose_name='Field Of Study')),
                ('study_from', models.DateField(blank=True, help_text='Date Format MM/DD/YYYY', null=True, verbose_name='From')),
                ('study_to', models.DateField(blank=True, help_text='Date Format MM/DD/YYYY', null=True, verbose_name='To')),
                ('edu_current', models.BooleanField(default=False)),
                ('draft', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_education', to='linkedin.Draft')),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('org_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Company Name')),
                ('title', models.CharField(blank=True, max_length=100, null=True, verbose_name='Title')),
                ('org_desc', ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Organization Description')),
                ('work_from', models.DateField(blank=True, help_text='Date Format MM/DD/YYYY', null=True, verbose_name='From')),
                ('work_to', models.DateField(blank=True, help_text='Date Format MM/DD/YYYY', null=True, verbose_name='To')),
                ('org_current', models.BooleanField(default=False)),
                ('draft', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_organization', to='linkedin.Draft')),
            ],
        ),
    ]
