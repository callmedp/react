# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-10-03 06:03
from __future__ import unicode_literals

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import meta.models
import shop.functions


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0026_merge_20180821_1732'),
    ]

    operations = [
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('url', models.CharField(blank=True, max_length=255, verbose_name='Url')),
                ('title', models.CharField(blank=True, max_length=255, verbose_name='Title')),
                ('meta_desc', models.TextField(blank=True, default='', verbose_name='Meta Description')),
                ('meta_keywords', models.TextField(blank=True, default='', verbose_name='Keywords')),
                ('heading', models.CharField(blank=True, max_length=255, verbose_name='H1')),
                ('image_alt', models.CharField(blank=True, max_length=255, verbose_name='Image Alt')),
                ('name', models.CharField(help_text='Faculty Name decides slug', max_length=200, verbose_name='Name')),
                ('slug', models.CharField(help_text='Unique slug', max_length=200, unique=True, verbose_name='Slug')),
                ('image', models.ImageField(blank=True, null=True, upload_to=shop.functions.get_upload_path_faculty, verbose_name='Image')),
                ('designation', models.CharField(max_length=200, verbose_name='Designation')),
                ('description', models.TextField(blank=True, default='', verbose_name='Description')),
                ('short_desc', models.TextField(blank=True, default='', verbose_name='Short Description')),
                ('faculty_speak', models.TextField(blank=True, default='', verbose_name='Faculty Speak')),
                ('active', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, meta.models.ModelMeta),
        ),
        migrations.CreateModel(
            name='FacultyProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('active', models.BooleanField(default=False)),
                ('display_order', models.PositiveIntegerField(default=1)),
                ('faculty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='facultyproducts', to='shop.Faculty', verbose_name='Faculty')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SubHeaderCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('heading', models.CharField(max_length=100)),
                ('description', ckeditor.fields.RichTextField(blank=True, default='', verbose_name='Description')),
                ('active', models.BooleanField(default=False)),
                ('display_order', models.PositiveIntegerField(default=1)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UniversityCourseDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('batch_launch_date', models.DateField(default=django.utils.timezone.now, help_text='This university course launch date')),
                ('apply_last_date', models.DateField(default=django.utils.timezone.now, help_text='Last date to apply for this univeristy course')),
                ('sample_certificate', models.FileField(blank=True, max_length=255, null=True, upload_to=shop.functions.get_upload_path_for_sample_certicate)),
                ('benefits', models.CharField(default='', max_length=1024)),
                ('application_process', models.CharField(default='', max_length=1024)),
                ('assesment', ckeditor.fields.RichTextField(default='', help_text='Description of Assesment and Evaluation', verbose_name='assesment')),
            ],
        ),
        migrations.CreateModel(
            name='UniversityCourseDetailScreen',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('batch_launch_date', models.DateField(default=django.utils.timezone.now, help_text='This university course launch date')),
                ('apply_last_date', models.DateField(default=django.utils.timezone.now, help_text='Last date to apply for this univeristy course')),
                ('sample_certificate', models.FileField(blank=True, max_length=255, null=True, upload_to=shop.functions.get_upload_path_for_sample_certicate)),
                ('benefits', models.CharField(default='', max_length=1024)),
                ('application_process', models.CharField(default='', max_length=1024)),
                ('assesment', ckeditor.fields.RichTextField(default='', help_text='Description of Assesment and Evaluation', verbose_name='assesment')),
            ],
        ),
        migrations.CreateModel(
            name='UniversityCoursePayment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('installment_fee', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='INR Program Fee')),
                ('last_date_of_payment', models.DateField(verbose_name='Last date of payemnt')),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='UniversityCoursePaymentScreen',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('installment_fee', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='INR Program Fee')),
                ('last_date_of_payment', models.DateField(verbose_name='Last date of payment')),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.AddField(
            model_name='category',
            name='is_university',
            field=models.BooleanField(default=False, verbose_name='Show as a University Page'),
        ),
        migrations.AlterField(
            model_name='product',
            name='type_flow',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Default'), (1, 'Resume Writing India'), (2, 'Courses'), (3, 'Resume Critique'), (4, 'International Profile Update'), (5, 'Featured Profile'), (6, 'IDfy Assessment'), (7, 'Resume Booster'), (8, 'Linkedin'), (9, 'Round One'), (10, 'StudyMate'), (11, 'TSSC'), (12, 'Country Specific Resume'), (13, 'Executive Bio,Portfolio,Visual Resume,Cover Letter,Second Regular Resume'), (14, 'University Courses')], default=0, verbose_name='Flow'),
        ),
        migrations.AlterField(
            model_name='productscreen',
            name='type_flow',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Default'), (1, 'Resume Writing India'), (2, 'Courses'), (3, 'Resume Critique'), (4, 'International Profile Update'), (5, 'Featured Profile'), (6, 'IDfy Assessment'), (7, 'Resume Booster'), (8, 'Linkedin'), (9, 'Round One'), (10, 'StudyMate'), (11, 'TSSC'), (12, 'Country Specific Resume'), (13, 'Executive Bio,Portfolio,Visual Resume,Cover Letter,Second Regular Resume'), (14, 'University Courses')], default=0, verbose_name='Flow'),
        ),
        migrations.AddField(
            model_name='universitycoursepaymentscreen',
            name='productscreen',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='screen_university_course_payment', to='shop.ProductScreen'),
        ),
        migrations.AddField(
            model_name='universitycoursepayment',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='university_course_payment', to='shop.Product'),
        ),
        migrations.AddField(
            model_name='universitycoursedetailscreen',
            name='productscreen',
            field=models.OneToOneField(help_text='Product related to these details', on_delete=django.db.models.deletion.CASCADE, related_name='screen_university_course_detail', to='shop.ProductScreen'),
        ),
        migrations.AddField(
            model_name='universitycoursedetail',
            name='product',
            field=models.OneToOneField(help_text='Product related to these details', on_delete=django.db.models.deletion.CASCADE, related_name='university_course_detail', to='shop.Product'),
        ),
        migrations.AddField(
            model_name='subheadercategory',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subheaders', to='shop.Category', verbose_name='University'),
        ),
        migrations.AddField(
            model_name='facultyproduct',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='facultyproducts', to='shop.Product', verbose_name='Product'),
        ),
        migrations.AddField(
            model_name='faculty',
            name='institute',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.Category'),
        ),
        migrations.AddField(
            model_name='faculty',
            name='products',
            field=models.ManyToManyField(blank=True, through='shop.FacultyProduct', to='shop.Product', verbose_name='Faculty Products'),
        ),
    ]
