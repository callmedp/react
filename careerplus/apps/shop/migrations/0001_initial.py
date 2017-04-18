# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-18 06:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import meta.models
import shop.functions


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('faq', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(editable=False)),
                ('modified', models.DateTimeField()),
                ('name', models.CharField(help_text='Unique name going to decide the slug', max_length=100, verbose_name='Name')),
                ('display_name', models.CharField(help_text='Unique name going to decide the slug', max_length=100, verbose_name='Display Name')),
                ('type_attribute', models.PositiveSmallIntegerField(choices=[(0, 'Text'), (1, 'Integer'), (2, 'True / False'), (3, 'Float'), (4, 'Rich Text'), (5, 'Date'), (6, 'Option'), (7, 'Entity'), (8, 'File'), (9, 'Image')], default=0, verbose_name='Type')),
                ('required', models.BooleanField(default=False, verbose_name='Required')),
                ('is_visible', models.BooleanField(default=True)),
                ('is_multiple', models.BooleanField(default=True)),
                ('is_searchable', models.BooleanField(default=True)),
                ('is_indexable', models.BooleanField(default=True)),
                ('is_comparable', models.BooleanField(default=True)),
                ('is_filterable', models.BooleanField(default=True)),
                ('is_sortable', models.BooleanField(default=True)),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AttributeOption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option', models.CharField(max_length=255, verbose_name='Option')),
            ],
            options={
                'verbose_name': 'Attribute option',
                'verbose_name_plural': 'Attribute options',
            },
        ),
        migrations.CreateModel(
            name='AttributeOptionGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'Attribute option group',
                'verbose_name_plural': 'Attribute option groups',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(editable=False)),
                ('modified', models.DateTimeField()),
                ('url', models.CharField(blank=True, max_length=255, verbose_name='Url')),
                ('title', models.CharField(blank=True, max_length=255, verbose_name='Title')),
                ('meta_desc', models.TextField(blank=True, default='', verbose_name='Meta Description')),
                ('meta_keywords', models.TextField(blank=True, default='', verbose_name='Keywords')),
                ('heading', models.CharField(blank=True, max_length=255, verbose_name='H1')),
                ('image_alt', models.CharField(blank=True, max_length=255, verbose_name='Image Alt')),
                ('name', models.CharField(help_text='Unique name going to decide the slug', max_length=100, verbose_name='Name')),
                ('slug', models.CharField(help_text='Unique slug', max_length=100, unique=True, verbose_name='Slug')),
                ('type_service', models.PositiveSmallIntegerField(choices=[(0, 'Default'), (1, 'Writing Services'), (2, 'Job Assistance Services'), (3, 'Courses'), (4, 'Other Services'), (5, 'Test Preparation'), (6, 'Blog'), (7, 'CMS')], default=0, verbose_name='Entity')),
                ('type_level', models.PositiveSmallIntegerField(choices=[(0, 'Default'), (1, 'Level 1'), (2, 'Level 2'), (3, 'Level 3'), (3, 'Level 4')], default=0, verbose_name='Level')),
                ('description', models.TextField(blank=True, default='', verbose_name='Description')),
                ('banner', models.ImageField(blank=True, null=True, upload_to=shop.functions.get_upload_path_category, verbose_name='Banner')),
                ('image', models.ImageField(blank=True, null=True, upload_to=shop.functions.get_upload_path_category, verbose_name='Image')),
                ('icon', models.ImageField(blank=True, null=True, upload_to=shop.functions.get_upload_path_category, verbose_name='Icon')),
                ('active', models.BooleanField(default=False)),
                ('display_order', models.IntegerField(default=1)),
            ],
            options={
                'verbose_name': 'Catalog Category',
                'verbose_name_plural': 'Catalog Categories',
                'get_latest_by': 'created',
                'ordering': ('-modified', '-created'),
            },
            bases=(models.Model, meta.models.ModelMeta),
        ),
        migrations.CreateModel(
            name='CategoryRelationship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(editable=False)),
                ('modified', models.DateTimeField()),
                ('relation', models.PositiveSmallIntegerField(choices=[(0, 'Active'), (1, 'Inactive')], default=0)),
                ('sort_order', models.PositiveIntegerField(default=1, verbose_name='Sort Order')),
                ('is_main_parent', models.BooleanField(default=False)),
                ('related_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_category', to='shop.Category', verbose_name='From')),
                ('related_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_category', to='shop.Category', verbose_name='To')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ChildProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(editable=False)),
                ('modified', models.DateTimeField()),
                ('sort_order', models.PositiveIntegerField(default=1, verbose_name='Sort Order')),
                ('price_offset', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, verbose_name='Price Offset')),
                ('price_offset_percent', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, verbose_name='% Offset')),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(editable=False)),
                ('modified', models.DateTimeField()),
                ('name', models.CharField(help_text='Name of Currency', max_length=100, verbose_name='Name')),
                ('value', models.PositiveIntegerField(help_text='Integer Value', verbose_name='Value')),
                ('exchange_rate', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, verbose_name='Exchange')),
                ('offset', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, verbose_name='Offset')),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Entity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(editable=False)),
                ('modified', models.DateTimeField()),
                ('url', models.CharField(blank=True, max_length=255, verbose_name='Url')),
                ('title', models.CharField(blank=True, max_length=255, verbose_name='Title')),
                ('meta_desc', models.TextField(blank=True, default='', verbose_name='Meta Description')),
                ('meta_keywords', models.TextField(blank=True, default='', verbose_name='Keywords')),
                ('heading', models.CharField(blank=True, max_length=255, verbose_name='H1')),
                ('image_alt', models.CharField(blank=True, max_length=255, verbose_name='Image Alt')),
                ('name', models.CharField(help_text='Unique name going to decide the slug', max_length=100, verbose_name='Name')),
                ('slug', models.CharField(help_text='Unique slug', max_length=100, unique=True, verbose_name='Slug')),
            ],
            options={
                'verbose_name': 'Product class',
                'verbose_name_plural': 'Product classes',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='FAQProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(editable=False)),
                ('modified', models.DateTimeField()),
                ('active', models.BooleanField(default=True)),
                ('question_order', models.PositiveIntegerField(default=1, verbose_name='Question Order')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(editable=False)),
                ('modified', models.DateTimeField()),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Name')),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(editable=False)),
                ('modified', models.DateTimeField()),
                ('url', models.CharField(blank=True, max_length=255, verbose_name='Url')),
                ('title', models.CharField(blank=True, max_length=255, verbose_name='Title')),
                ('meta_desc', models.TextField(blank=True, default='', verbose_name='Meta Description')),
                ('meta_keywords', models.TextField(blank=True, default='', verbose_name='Keywords')),
                ('heading', models.CharField(blank=True, max_length=255, verbose_name='H1')),
                ('name', models.CharField(help_text='Unique name going to decide the slug', max_length=100, verbose_name='Name')),
                ('slug', models.CharField(help_text='Unique slug', max_length=100, unique=True, verbose_name='Slug')),
                ('type_service', models.PositiveSmallIntegerField(choices=[(0, 'Default'), (1, 'Writing Services'), (2, 'Job Assistance Services'), (3, 'Courses'), (4, 'Other Services'), (5, 'Test Preparation'), (6, 'Blog'), (7, 'CMS')], default=0, verbose_name='Entity')),
                ('type_product', models.PositiveSmallIntegerField(choices=[(0, 'Simple'), (1, 'Configurable'), (2, 'Combo'), (3, 'Virtual/Services'), (4, 'Bundle'), (5, 'Downloadable')], default=0, verbose_name='Type')),
                ('type_flow', models.PositiveSmallIntegerField(choices=[(0, 'Default'), (1, 'Flow 1'), (2, 'Flow 2'), (3, 'Flow 3'), (4, 'Flow 4'), (5, 'Flow 5'), (6, 'Flow 6'), (7, 'Flow 7'), (8, 'Flow 8'), (9, 'Flow 9'), (10, 'Flow 10'), (11, 'Flow 11'), (12, 'Flow 12')], default=0, verbose_name='Flow')),
                ('upc', models.CharField(help_text='To be filled by vendor', max_length=100, verbose_name='Universal Product Code')),
                ('banner', models.ImageField(blank=True, null=True, upload_to=shop.functions.get_upload_path_product_banner, verbose_name='Banner')),
                ('icon', models.ImageField(blank=True, null=True, upload_to=shop.functions.get_upload_path_product_icon, verbose_name='Icon')),
                ('image', models.ImageField(blank=True, null=True, upload_to=shop.functions.get_upload_path_product_image, verbose_name='Image')),
                ('image_alt', models.CharField(blank=True, max_length=100, verbose_name='Image Alt')),
                ('video_url', models.CharField(blank=True, max_length=200, verbose_name='Video Url')),
                ('flow_image', models.ImageField(blank=True, null=True, upload_to=shop.functions.get_upload_path_product_image, verbose_name='Delivery Flow Image')),
                ('email_cc', models.TextField(blank=True, default='', verbose_name='Email_CC ID')),
                ('about', models.TextField(blank=True, default='', verbose_name='About Product')),
                ('description', models.TextField(blank=True, default='', verbose_name='Description Product')),
                ('buy_shine', models.TextField(blank=True, default='', verbose_name='Why Buy From Shine')),
                ('mail_desc', models.TextField(blank=True, default='', verbose_name='Welcome Mail Description')),
                ('duration_months', models.IntegerField(default=0, verbose_name='Duration In Months')),
                ('duration_days', models.IntegerField(default=0, verbose_name='Duration In Days')),
                ('experience', models.PositiveSmallIntegerField(choices=[(0, 'Default'), (1, 'Exp 1-4 Yrs'), (2, 'Exp 1-4 Yrs'), (3, 'Flow 3'), (4, 'Flow 4'), (5, 'Flow 5'), (6, 'Flow 6'), (7, 'Flow 7'), (8, 'Flow 8'), (9, 'Flow 9'), (10, 'Flow 10'), (11, 'Flow 11'), (12, 'Flow 12')], default=0, verbose_name='Experience')),
                ('requires_delivery', models.BooleanField(default=True, verbose_name='Requires delivery?')),
                ('avg_rating', models.DecimalField(decimal_places=2, default=2.5, max_digits=8, verbose_name='Average Rating')),
                ('no_review', models.PositiveIntegerField(default=0, verbose_name='No. Of Review')),
                ('buy_count', models.PositiveIntegerField(default=0, verbose_name='Buy Count')),
                ('search_keywords', models.TextField(blank=True, default='', verbose_name='Search Keywords')),
                ('active', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
                'get_latest_by': 'created',
                'ordering': ('-modified', '-created'),
            },
            bases=(models.Model, meta.models.ModelMeta),
        ),
        migrations.CreateModel(
            name='ProductArchive',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(editable=False)),
                ('modified', models.DateTimeField()),
                ('url', models.CharField(blank=True, max_length=255, verbose_name='Url')),
                ('title', models.CharField(blank=True, max_length=255, verbose_name='Title')),
                ('meta_desc', models.TextField(blank=True, default='', verbose_name='Meta Description')),
                ('meta_keywords', models.TextField(blank=True, default='', verbose_name='Keywords')),
                ('heading', models.CharField(blank=True, max_length=255, verbose_name='H1')),
                ('name', models.CharField(help_text='Unique name going to decide the slug', max_length=100, verbose_name='Name')),
                ('slug', models.CharField(help_text='Unique slug', max_length=100, unique=True, verbose_name='Slug')),
                ('type_service', models.PositiveSmallIntegerField(choices=[(0, 'Default'), (1, 'Writing Services'), (2, 'Job Assistance Services'), (3, 'Courses'), (4, 'Other Services'), (5, 'Test Preparation'), (6, 'Blog'), (7, 'CMS')], default=0, verbose_name='Entity')),
                ('type_product', models.PositiveSmallIntegerField(choices=[(0, 'Simple'), (1, 'Configurable'), (2, 'Combo'), (3, 'Virtual/Services'), (4, 'Bundle'), (5, 'Downloadable')], default=0, verbose_name='Type')),
                ('type_flow', models.PositiveSmallIntegerField(choices=[(0, 'Default'), (1, 'Flow 1'), (2, 'Flow 2'), (3, 'Flow 3'), (4, 'Flow 4'), (5, 'Flow 5'), (6, 'Flow 6'), (7, 'Flow 7'), (8, 'Flow 8'), (9, 'Flow 9'), (10, 'Flow 10'), (11, 'Flow 11'), (12, 'Flow 12')], default=0, verbose_name='Flow')),
                ('upc', models.CharField(help_text='To be filled by vendor', max_length=100, verbose_name='Universal Product Code')),
                ('banner', models.ImageField(blank=True, null=True, upload_to=shop.functions.get_upload_path_product_banner, verbose_name='Banner')),
                ('icon', models.ImageField(blank=True, null=True, upload_to=shop.functions.get_upload_path_product_icon, verbose_name='Icon')),
                ('image', models.ImageField(blank=True, null=True, upload_to=shop.functions.get_upload_path_product_image, verbose_name='Image')),
                ('image_alt', models.CharField(blank=True, max_length=100, verbose_name='Image Alt')),
                ('video_url', models.CharField(blank=True, max_length=200, verbose_name='Video Url')),
                ('flow_image', models.ImageField(blank=True, null=True, upload_to=shop.functions.get_upload_path_product_image, verbose_name='Delivery Flow Image')),
                ('email_cc', models.TextField(blank=True, default='', verbose_name='Email_CC ID')),
                ('about', models.TextField(blank=True, default='', verbose_name='About Product')),
                ('description', models.TextField(blank=True, default='', verbose_name='Description Product')),
                ('buy_shine', models.TextField(blank=True, default='', verbose_name='Why Buy From Shine')),
                ('mail_desc', models.TextField(blank=True, default='', verbose_name='Welcome Mail Description')),
                ('duration_months', models.IntegerField(default=0, verbose_name='Duration In Months')),
                ('duration_days', models.IntegerField(default=0, verbose_name='Duration In Days')),
                ('experience', models.PositiveSmallIntegerField(choices=[(0, 'Default'), (1, 'Exp 1-4 Yrs'), (2, 'Exp 1-4 Yrs'), (3, 'Flow 3'), (4, 'Flow 4'), (5, 'Flow 5'), (6, 'Flow 6'), (7, 'Flow 7'), (8, 'Flow 8'), (9, 'Flow 9'), (10, 'Flow 10'), (11, 'Flow 11'), (12, 'Flow 12')], default=0, verbose_name='Experience')),
                ('requires_delivery', models.BooleanField(default=True, verbose_name='Requires delivery?')),
                ('entity', models.CharField(blank=True, max_length=20, verbose_name='Product Entity')),
                ('siblings', models.CharField(blank=True, max_length=100, verbose_name='Siblings Product')),
                ('related', models.CharField(blank=True, max_length=100, verbose_name='Related Product')),
                ('combo', models.CharField(blank=True, max_length=100, verbose_name='Child Product')),
                ('categories', models.CharField(blank=True, max_length=100, verbose_name='Product Category')),
                ('keywords', models.CharField(blank=True, max_length=100, verbose_name='Product Keyword')),
                ('offers', models.CharField(blank=True, max_length=100, verbose_name='Product Offer')),
                ('faqs', models.CharField(blank=True, max_length=100, verbose_name='Product Structure')),
                ('attributes', models.CharField(blank=True, max_length=100, verbose_name='Product Attributes')),
                ('prices', models.CharField(blank=True, max_length=100, verbose_name='Product Prices')),
                ('originalproduct', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='originalproduct', to='shop.Product', verbose_name='Original Product')),
            ],
            options={
                'verbose_name': 'Product Archive',
                'verbose_name_plural': 'Product Archives ',
                'get_latest_by': 'created',
                'ordering': ('-modified', '-created'),
            },
        ),
        migrations.CreateModel(
            name='ProductAttribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(editable=False)),
                ('modified', models.DateTimeField()),
                ('value_text', models.CharField(blank=True, max_length=100, verbose_name='Value Text')),
                ('value_integer', models.PositiveSmallIntegerField(default=0, verbose_name='Value Integer')),
                ('value_date', models.DateTimeField(blank=True, null=True, verbose_name='Value Date')),
                ('value_decimal', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, verbose_name='Value Date')),
                ('value_ltext', models.TextField(blank=True, default='', verbose_name='Value Large Text')),
                ('value_file', models.FileField(blank=True, max_length=255, null=True, upload_to=shop.functions.get_upload_path_product_file)),
                ('value_image', models.ImageField(blank=True, max_length=255, null=True, upload_to=shop.functions.get_upload_path_product_image)),
                ('entity_object_id', models.PositiveIntegerField(blank=True, editable=False, null=True)),
                ('active', models.BooleanField(default=True)),
                ('attribute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attributes', to='shop.Attribute', verbose_name='Attribute')),
                ('entity_content_type', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attributeproducts', to='shop.Product', verbose_name='Product')),
                ('value_option', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.AttributeOption', verbose_name='Value option')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(editable=False)),
                ('modified', models.DateTimeField()),
                ('is_main', models.BooleanField(default=True)),
                ('active', models.BooleanField(default=True)),
                ('prd_order', models.PositiveIntegerField(default=1, verbose_name='Product Order')),
                ('cat_order', models.PositiveIntegerField(default=1, verbose_name='Category Order')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='shop.Category', verbose_name='Category')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categoryproducts', to='shop.Product', verbose_name='Product')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProductExtraInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('info_type', models.CharField(max_length=256, verbose_name='Type')),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Product', verbose_name='Product')),
            ],
            options={
                'ordering': ['info_type'],
            },
        ),
        migrations.CreateModel(
            name='ProductKeyword',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(editable=False)),
                ('modified', models.DateTimeField()),
                ('active', models.BooleanField(default=True)),
                ('weight', models.PositiveIntegerField(default=1, verbose_name='Weight')),
                ('keyword', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='keywords', to='shop.Keyword', verbose_name='Keyword')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='keywordproducts', to='shop.Product', verbose_name='Product')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProductPrice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(editable=False)),
                ('modified', models.DateTimeField()),
                ('value', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, verbose_name='Value Price')),
                ('fake_value', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, verbose_name='Value Fake Price')),
                ('active', models.BooleanField(default=True)),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prices', to='shop.Currency', verbose_name='Currency')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='priceproducts', to='shop.Product', verbose_name='Product')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProductScreen',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(editable=False)),
                ('modified', models.DateTimeField()),
                ('url', models.CharField(blank=True, max_length=255, verbose_name='Url')),
                ('title', models.CharField(blank=True, max_length=255, verbose_name='Title')),
                ('meta_desc', models.TextField(blank=True, default='', verbose_name='Meta Description')),
                ('meta_keywords', models.TextField(blank=True, default='', verbose_name='Keywords')),
                ('heading', models.CharField(blank=True, max_length=255, verbose_name='H1')),
                ('name', models.CharField(help_text='Unique name going to decide the slug', max_length=100, verbose_name='Name')),
                ('slug', models.CharField(help_text='Unique slug', max_length=100, unique=True, verbose_name='Slug')),
                ('type_service', models.PositiveSmallIntegerField(choices=[(0, 'Default'), (1, 'Writing Services'), (2, 'Job Assistance Services'), (3, 'Courses'), (4, 'Other Services'), (5, 'Test Preparation'), (6, 'Blog'), (7, 'CMS')], default=0, verbose_name='Entity')),
                ('type_product', models.PositiveSmallIntegerField(choices=[(0, 'Simple'), (1, 'Configurable'), (2, 'Combo'), (3, 'Virtual/Services'), (4, 'Bundle'), (5, 'Downloadable')], default=0, verbose_name='Type')),
                ('type_flow', models.PositiveSmallIntegerField(choices=[(0, 'Default'), (1, 'Flow 1'), (2, 'Flow 2'), (3, 'Flow 3'), (4, 'Flow 4'), (5, 'Flow 5'), (6, 'Flow 6'), (7, 'Flow 7'), (8, 'Flow 8'), (9, 'Flow 9'), (10, 'Flow 10'), (11, 'Flow 11'), (12, 'Flow 12')], default=0, verbose_name='Flow')),
                ('upc', models.CharField(help_text='To be filled by vendor', max_length=100, verbose_name='Universal Product Code')),
                ('banner', models.ImageField(blank=True, null=True, upload_to=shop.functions.get_upload_path_product_banner, verbose_name='Banner')),
                ('icon', models.ImageField(blank=True, null=True, upload_to=shop.functions.get_upload_path_product_icon, verbose_name='Icon')),
                ('image', models.ImageField(blank=True, null=True, upload_to=shop.functions.get_upload_path_product_image, verbose_name='Image')),
                ('image_alt', models.CharField(blank=True, max_length=100, verbose_name='Image Alt')),
                ('video_url', models.CharField(blank=True, max_length=200, verbose_name='Video Url')),
                ('flow_image', models.ImageField(blank=True, null=True, upload_to=shop.functions.get_upload_path_product_image, verbose_name='Delivery Flow Image')),
                ('email_cc', models.TextField(blank=True, default='', verbose_name='Email_CC ID')),
                ('about', models.TextField(blank=True, default='', verbose_name='About Product')),
                ('description', models.TextField(blank=True, default='', verbose_name='Description Product')),
                ('buy_shine', models.TextField(blank=True, default='', verbose_name='Why Buy From Shine')),
                ('mail_desc', models.TextField(blank=True, default='', verbose_name='Welcome Mail Description')),
                ('duration_months', models.IntegerField(default=0, verbose_name='Duration In Months')),
                ('duration_days', models.IntegerField(default=0, verbose_name='Duration In Days')),
                ('experience', models.PositiveSmallIntegerField(choices=[(0, 'Default'), (1, 'Exp 1-4 Yrs'), (2, 'Exp 1-4 Yrs'), (3, 'Flow 3'), (4, 'Flow 4'), (5, 'Flow 5'), (6, 'Flow 6'), (7, 'Flow 7'), (8, 'Flow 8'), (9, 'Flow 9'), (10, 'Flow 10'), (11, 'Flow 11'), (12, 'Flow 12')], default=0, verbose_name='Experience')),
                ('requires_delivery', models.BooleanField(default=True, verbose_name='Requires delivery?')),
                ('entity', models.CharField(blank=True, max_length=20, verbose_name='Product Entity')),
                ('siblings', models.CharField(blank=True, max_length=100, verbose_name='Siblings Product')),
                ('related', models.CharField(blank=True, max_length=100, verbose_name='Related Product')),
                ('combo', models.CharField(blank=True, max_length=100, verbose_name='Child Product')),
                ('categories', models.CharField(blank=True, max_length=100, verbose_name='Product Category')),
                ('keywords', models.CharField(blank=True, max_length=100, verbose_name='Product Keyword')),
                ('offers', models.CharField(blank=True, max_length=100, verbose_name='Product Offer')),
                ('faqs', models.CharField(blank=True, max_length=100, verbose_name='Product Structure')),
                ('attributes', models.CharField(blank=True, max_length=100, verbose_name='Product Attributes')),
                ('prices', models.CharField(blank=True, max_length=100, verbose_name='Product Prices')),
                ('originalproduct', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='linkedproduct', to='shop.Product', verbose_name='Linked Product')),
            ],
            options={
                'verbose_name': 'Product Screen',
                'verbose_name_plural': 'Product Screens ',
                'get_latest_by': 'created',
                'ordering': ('-modified', '-created'),
            },
        ),
        migrations.CreateModel(
            name='RelatedProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(editable=False)),
                ('modified', models.DateTimeField()),
                ('sort_order', models.PositiveIntegerField(default=1, verbose_name='Sort Order')),
                ('price_offset', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, verbose_name='Price Offset')),
                ('price_offset_percent', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, verbose_name='% Offset')),
                ('active', models.BooleanField(default=True)),
                ('type_relation', models.PositiveSmallIntegerField(choices=[(0, 'Default'), (1, 'UpSell'), (2, 'Recommendation'), (3, 'CrossSell')], default=0, verbose_name='Relation')),
                ('ranking', models.PositiveSmallIntegerField(default=0, help_text='Determines order of the products. A product with a higher value will appear before one with a lower ranking.', verbose_name='Ranking')),
                ('primary', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='primaryproduct', to='shop.Product')),
                ('secondary', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='secondaryproduct', to='shop.Product')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='product',
            name='attributes',
            field=models.ManyToManyField(blank=True, through='shop.ProductAttribute', to='shop.Attribute', verbose_name='Product Attribute'),
        ),
        migrations.AddField(
            model_name='product',
            name='categories',
            field=models.ManyToManyField(blank=True, through='shop.ProductCategory', to='shop.Category', verbose_name='Product Category'),
        ),
        migrations.AddField(
            model_name='product',
            name='combo',
            field=models.ManyToManyField(blank=True, related_name='_product_combo_+', through='shop.ChildProduct', to='shop.Product', verbose_name='Child Product'),
        ),
        migrations.AddField(
            model_name='product',
            name='entity',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='entityproducts', to='shop.Entity', verbose_name='Product Entity'),
        ),
        migrations.AddField(
            model_name='product',
            name='faqs',
            field=models.ManyToManyField(blank=True, through='shop.FAQProduct', to='faq.FAQuestion', verbose_name='Product FAQ'),
        ),
        migrations.AddField(
            model_name='product',
            name='keywords',
            field=models.ManyToManyField(blank=True, through='shop.ProductKeyword', to='shop.Keyword', verbose_name='Product Keyword'),
        ),
        migrations.AddField(
            model_name='product',
            name='prices',
            field=models.ManyToManyField(blank=True, through='shop.ProductPrice', to='shop.Currency', verbose_name='Product Price'),
        ),
        migrations.AddField(
            model_name='product',
            name='related',
            field=models.ManyToManyField(blank=True, related_name='_product_related_+', through='shop.RelatedProduct', to='shop.Product', verbose_name='Related Product'),
        ),
        migrations.AddField(
            model_name='product',
            name='siblings',
            field=models.ManyToManyField(blank=True, related_name='_product_siblings_+', to='shop.Product', verbose_name='Sibling Products'),
        ),
        migrations.AddField(
            model_name='product',
            name='structure',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='topicproducts', to='faq.Topic', verbose_name='Product Structure'),
        ),
        migrations.AddField(
            model_name='keyword',
            name='keyproducts',
            field=models.ManyToManyField(blank=True, through='shop.ProductKeyword', to='shop.Product', verbose_name='Keyword Product'),
        ),
        migrations.AddField(
            model_name='faqproduct',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questionproducts', to='shop.Product', verbose_name='Product'),
        ),
        migrations.AddField(
            model_name='faqproduct',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='faquestions', to='faq.FAQuestion', verbose_name='FAQuestion'),
        ),
        migrations.AddField(
            model_name='childproduct',
            name='children',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='childrenproduct', to='shop.Product'),
        ),
        migrations.AddField(
            model_name='childproduct',
            name='father',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parentproduct', to='shop.Product'),
        ),
        migrations.AddField(
            model_name='category',
            name='categoryproducts',
            field=models.ManyToManyField(blank=True, through='shop.ProductCategory', to='shop.Product', verbose_name='Category Product'),
        ),
        migrations.AddField(
            model_name='category',
            name='related_to',
            field=models.ManyToManyField(blank=True, through='shop.CategoryRelationship', to='shop.Category', verbose_name='Related Category'),
        ),
        migrations.AddField(
            model_name='attributeoption',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='shop.AttributeOptionGroup', verbose_name='Group'),
        ),
        migrations.AddField(
            model_name='attribute',
            name='attributeproducts',
            field=models.ManyToManyField(blank=True, through='shop.ProductAttribute', to='shop.Product', verbose_name='Attribute Product'),
        ),
        migrations.AddField(
            model_name='attribute',
            name='entity',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attributes', to='shop.Entity', verbose_name='Entity'),
        ),
        migrations.AddField(
            model_name='attribute',
            name='option_group',
            field=models.ForeignKey(blank=True, help_text='Select an option group if using type "Option"', null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.AttributeOptionGroup', verbose_name='Option Group'),
        ),
        migrations.AlterUniqueTogether(
            name='attributeoption',
            unique_together=set([('group', 'option')]),
        ),
    ]
