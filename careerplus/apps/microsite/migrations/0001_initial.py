# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-18 10:28
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import filebrowser.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MicroSite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('slug', models.SlugField(blank=True, max_length=255, unique=True)),
                ('active', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='MicrositeBanner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True)),
                ('image', filebrowser.fields.FileBrowseField(max_length=200, verbose_name='Image')),
                ('image_alt', models.CharField(max_length=255, null=True)),
                ('active', models.BooleanField(default=False)),
                ('url', models.URLField(blank=True, help_text='Append http://', null=True)),
                ('position', models.IntegerField(blank=True, default=0)),
            ],
        ),
        migrations.CreateModel(
            name='PartnerFaq',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=1024, null=True)),
                ('answer', models.TextField()),
                ('active', models.BooleanField(default=False)),
                ('microsite', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='microsite.MicroSite')),
            ],
        ),
        migrations.CreateModel(
            name='PartnerPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('slug', models.SlugField(blank=True, max_length=255, unique=True)),
                ('type_of_page', models.PositiveSmallIntegerField(choices=[(1, 'Home Page'), (2, 'Listing Page'), (3, 'Detail Page')])),
                ('banner_image', models.ManyToManyField(blank=True, null=True, to='microsite.MicrositeBanner')),
            ],
        ),
        migrations.CreateModel(
            name='PartnerTestimonial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_of_user', models.CharField(max_length=255, null=True)),
                ('image', filebrowser.fields.FileBrowseField(max_length=200, verbose_name='Image')),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('review', models.TextField(max_length=1024)),
                ('rating', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('added_on', models.DateTimeField(blank=True, null=True)),
                ('active', models.BooleanField(default=False)),
                ('microsite', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='microsite.MicroSite')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User(if any)')),
            ],
        ),
        migrations.AddField(
            model_name='microsite',
            name='detail_page',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='detail_page', to='microsite.PartnerPage'),
        ),
        migrations.AddField(
            model_name='microsite',
            name='home_page',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='home_page', to='microsite.PartnerPage'),
        ),
        migrations.AddField(
            model_name='microsite',
            name='listing_page',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='listing_page', to='microsite.PartnerPage'),
        ),
    ]
