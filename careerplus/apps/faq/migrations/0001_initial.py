# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-07 12:34
from __future__ import unicode_literals

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('heading', models.CharField(max_length=255, verbose_name='chapter')),
                ('answer', ckeditor.fields.RichTextField(blank=True, help_text='The answer text.', verbose_name='answer')),
                ('ordering', models.PositiveSmallIntegerField(default=1, help_text='An integer used to order the chapter             amongst others related to the same chapter. If not given this             chapter will be last in the list.', verbose_name='ordering')),
                ('status', models.IntegerField(choices=[(2, 'Active'), (1, 'Inactive'), (0, 'Moderation')], default=0, help_text="Only questions with their status set to 'Active' will be displayed.", verbose_name='status')),
            ],
            options={
                'ordering': ('heading',),
                'verbose_name': 'chapter',
                'verbose_name_plural': 'chapters',
            },
        ),
        migrations.CreateModel(
            name='FAQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('text', models.TextField(help_text='The actual question itself.', verbose_name='question')),
                ('answer', ckeditor.fields.RichTextField(blank=True, help_text='The answer text.', verbose_name='answer')),
                ('status', models.IntegerField(choices=[(2, 'Active'), (1, 'Inactive'), (0, 'Moderation')], default=0, help_text="Only questions with their status set to 'Active' will be displayed.", verbose_name='status')),
                ('sort_order', models.IntegerField(default=0, help_text='The order you would like the question to be displayed.', verbose_name='sort order')),
            ],
            options={
                'ordering': ['sort_order', 'created'],
                'verbose_name': 'Frequent asked question',
                'verbose_name_plural': 'Frequently asked questions',
            },
        ),
    ]
