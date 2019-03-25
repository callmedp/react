# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2019-02-04 14:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ExternalLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.CharField(max_length=200, verbose_name='Link')),
            ],
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(max_length=100, verbose_name='Skill Name')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(max_length=100, verbose_name='User Name')),
                ('email', models.CharField(max_length=100, unique=True, verbose_name='User Email')),
                ('mobile', models.CharField(max_length=15, verbose_name='User Contact Number')),
                ('date_of_birth', models.DateField(verbose_name='DOB')),
                ('location', models.CharField(max_length=100, verbose_name='User Location')),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Others')], max_length=1, verbose_name='Gender')),
                ('extra_info', models.TextField(verbose_name='Extra Information')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserCertification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_of_certification', models.CharField(max_length=250, verbose_name='Certification Name')),
                ('year_of_certification', models.DateField(verbose_name='Year of Certification')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resumebuilder.User', verbose_name='User')),
            ],
        ),
        migrations.CreateModel(
            name='UserEducation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('specialization', models.CharField(max_length=200, verbose_name='Specialization')),
                ('institution_name', models.CharField(max_length=250, verbose_name='Institution Name')),
                ('course_type', models.CharField(choices=[('FT', 'Full Time'), ('PT', 'Part Time'), ('CR', 'Correspondence')], max_length=2, verbose_name='Institution Name')),
                ('percentage_cgpa', models.CharField(max_length=250, verbose_name='Percentage Or CGPA')),
                ('start_date', models.DateField(verbose_name='Start Date')),
                ('end_date', models.DateField(blank=True, verbose_name='End Date')),
                ('is_pursuing', models.BooleanField(verbose_name='Still Pursuing')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resumebuilder.User', verbose_name='User')),
            ],
        ),
        migrations.CreateModel(
            name='UserExperience',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_profile', models.CharField(max_length=100, verbose_name='Job Profile')),
                ('company_name', models.CharField(max_length=200, verbose_name='Company Name')),
                ('start_date', models.DateField(verbose_name='Start Date')),
                ('end_date', models.DateField(blank=True, verbose_name='End Date')),
                ('is_working', models.BooleanField(verbose_name='Present')),
                ('job_location', models.CharField(max_length=100, verbose_name='Job Location')),
                ('work_description', models.TextField(verbose_name='Job Description')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resumebuilder.User', verbose_name='User')),
            ],
        ),
        migrations.CreateModel(
            name='UserProject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(max_length=150, verbose_name='Project Name')),
                ('start_date', models.DateField(verbose_name='Start Date')),
                ('end_date', models.DateField(blank=True, verbose_name='End Date')),
                ('skills', models.ManyToManyField(to='resumebuilder.Skill', verbose_name='List of Skills')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resumebuilder.User', verbose_name='User')),
            ],
        ),
        migrations.CreateModel(
            name='UserReference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference_designation', models.CharField(max_length=150, verbose_name='Reference Designation')),
                ('about_user', models.TextField(verbose_name='About User')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resumebuilder.User', verbose_name='User')),
            ],
        ),
        migrations.AddField(
            model_name='skill',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resumebuilder.User', verbose_name='User'),
        ),
        migrations.AddField(
            model_name='externallink',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resumebuilder.User', verbose_name='User'),
        ),
    ]
