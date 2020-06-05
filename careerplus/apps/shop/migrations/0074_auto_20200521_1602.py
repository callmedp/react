# Generated by Django 2.2.10 on 2020-05-21 10:32

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import shop.functions


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_blog_position'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shop', '0073_merge_20200521_1559'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubSection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('icon', models.ImageField(blank=True, null=True, upload_to=shop.functions.get_upload_path_product_subsection_icon, verbose_name='subsection icon')),
                ('heading', models.CharField(blank=True, default='', max_length=255, verbose_name='Sub Section heading')),
                ('description', ckeditor.fields.RichTextField(blank=True, default='', verbose_name='Sub Section Description')),
                ('active', models.BooleanField(default=False)),
                ('priority', models.PositiveSmallIntegerField(default=1)),
            ],
            options={
                'ordering': ['-priority'],
            },
        ),
        migrations.RemoveField(
            model_name='product',
            name='job_title',
        ),
        migrations.AddField(
            model_name='product',
            name='banner_text',
            field=models.CharField(default='', help_text='This text will be displayed on Banner Image', max_length=100, verbose_name='Banner Text'),
        ),
        migrations.AddField(
            model_name='product',
            name='sub_heading',
            field=models.CharField(default='', max_length=100, verbose_name='Sub heading will be displayed above heading'),
        ),
        migrations.AddField(
            model_name='product',
            name='visible_on_resume_shine',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='productscreen',
            name='banner_text',
            field=models.CharField(default='', help_text='This text will be displayed on Banner Image', max_length=100, verbose_name='Banner Text'),
        ),
        migrations.AddField(
            model_name='productscreen',
            name='sub_heading',
            field=models.CharField(default='', max_length=100, verbose_name='Sub heading will be displayed above heading'),
        ),
        # migrations.AddField(
        #     model_name='productuserprofile',
        #     name='due_date_extended_by',
        #     field=models.PositiveSmallIntegerField(default=0),
        # ),
        # migrations.AddField(
        #     model_name='productuserprofile',
        #     name='latest_education',
        #     field=models.PositiveSmallIntegerField(blank=True, choices=[('0', 'NA'), ('101', '10+2 or Below'), ('102', 'B.A'), ('103', 'B.Arch'), ('104', 'B.B.A / B.M.S'), ('105', 'B.C.A'), ('106', 'B.Com'), ('107', 'B.Ed'), ('108', 'B.Pharma'), ('109', 'B.Sc'), ('110', 'B.Tech/B.E'), ('111', 'BDS'), ('112', 'BHM'), ('113', 'BVSC'), ('114', 'C.A'), ('115', 'C.F.A'), ('116', 'C.S'), ('117', 'Diploma'), ('118', 'ICWA / CMA'), ('119', 'Integrated PG'), ('120', 'LL.M'), ('121', 'LLB'), ('122', 'M.A'), ('123', 'M.C.A'), ('124', 'M.Com'), ('125', 'M.Ed'), ('126', 'M.Pharma'), ('127', 'M.Sc'), ('128', 'M.Tech'), ('129', 'MBA/PGDM'), ('130', 'MBBS'), ('131', 'MD/MS'), ('132', 'MDS'), ('133', 'MMH'), ('134', 'MPHIL'), ('135', 'MVSC'), ('136', 'Other'), ('137', 'PG Diploma'), ('138', 'Ph.D/Doctorate'), ('139', 'BHMS'), ('140', 'BAMS'), ('141', 'B.P.Ed'), ('142', 'BPT'), ('143', 'BUMS'), ('144', 'CA (Intermediate)'), ('146', 'M.P.Ed')], null=True),
        # ),
        migrations.AlterField(
            model_name='product',
            name='product_tag',
            field=models.SmallIntegerField(choices=[(0, 'None'), (1, 'Bestseller'), (2, 'Newly Added')], default=0),
        ),
        migrations.AlterField(
            model_name='product',
            name='sub_type_flow',
            field=models.IntegerField(choices=[(501, 'Featured Profile'), (502, 'Jobs on the Move'), (503, 'Priority Applicant'), (1601, 'Free Test'), (1602, 'Paid Test'), (200, 'Default'), (201, 'Certificate Product'), (100, 'Default'), (101, 'Expert Assistance'), (1700, 'Default'), (1701, 'Subscription')], default=-1),
        ),
        migrations.AlterField(
            model_name='productscreen',
            name='sub_type_flow',
            field=models.IntegerField(choices=[(501, 'Featured Profile'), (502, 'Jobs on the Move'), (503, 'Priority Applicant'), (1601, 'Free Test'), (1602, 'Paid Test'), (200, 'Default'), (201, 'Certificate Product'), (100, 'Default'), (101, 'Expert Assistance'), (1700, 'Default'), (1701, 'Subscription')], default=-1),
        ),
        migrations.AlterField(
            model_name='shineprofiledata',
            name='sub_type_flow',
            field=models.IntegerField(choices=[(501, 'Featured Profile'), (502, 'Jobs on the Move'), (503, 'Priority Applicant'), (1601, 'Free Test'), (1602, 'Paid Test'), (200, 'Default'), (201, 'Certificate Product'), (100, 'Default'), (101, 'Expert Assistance'), (1700, 'Default'), (1701, 'Subscription')]),
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(blank=True, default='', max_length=300, null=True)),
                ('priority', models.PositiveSmallIntegerField(default=1)),
                ('image', models.ImageField(blank=True, null=True, upload_to=shop.functions.get_upload_path_product_section_image, verbose_name='subsection image')),
                ('active', models.BooleanField(default=False)),
                ('heading', models.CharField(blank=True, default='', max_length=255, verbose_name='heading')),
                ('section_type', models.PositiveSmallIntegerField(choices=[(1, 'features'), (2, 'why-choose-us'), (3, 'how-it-works'), (4, 'product-banner-widget')], default=0)),
                ('product', models.ManyToManyField(blank=True, null=True, to='shop.Product')),
                ('sub_section', models.ManyToManyField(blank=True, null=True, to='shop.SubSection')),
            ],
            options={
                'ordering': ['-priority'],
            },
        ),
        migrations.CreateModel(
            name='ProductJobTitle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(blank=True, help_text='Job title', max_length=100, null=True, verbose_name='Job Title')),
                ('product', models.ManyToManyField(null=True, related_name='jobtitle', to='shop.Product', verbose_name='Product')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('offers', models.CharField(blank=True, max_length=300, null=True)),
                ('expiry_date', models.DateTimeField(blank=True, null=True)),
                ('max_used', models.PositiveIntegerField(default=100, verbose_name='Maximum number of times this offer can be used')),
                ('active', models.BooleanField(default=False)),
                ('icon', models.ImageField(blank=True, null=True, upload_to=shop.functions.get_upload_path_product_offer_icon, verbose_name='offer icon')),
                ('product', models.ManyToManyField(blank=True, null=True, to='shop.Product')),
            ],
            options={
                'ordering': ['-modified'],
            },
        ),
        migrations.CreateModel(
            name='BlogProductMapping',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_modified_on', models.DateTimeField(auto_now=True, null=True)),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Blog')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shop_blogproductmapping_created_by', related_query_name='shop_blogproductmappings', to=settings.AUTH_USER_MODEL)),
                ('last_modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shop_blogproductmapping_last_modified_by', related_query_name='shop_blogproductmappings', to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Product')),
            ],
            options={
                'ordering': ['-created_on'],
            },
        ),
    ]
