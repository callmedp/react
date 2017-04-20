# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-19 06:34
from __future__ import unicode_literals

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('faq', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chapter',
            name='answer',
            field=ckeditor.fields.RichTextField(blank=True, help_text='The answer text.', verbose_name='answer'),
        ),
        migrations.AlterField(
            model_name='faquestion',
            name='answer',
            field=ckeditor.fields.RichTextField(blank=True, help_text='The answer text.', verbose_name='answer'),
        ),
        migrations.AlterField(
            model_name='topic',
            name='description',
            field=ckeditor.fields.RichTextField(blank=True, help_text='A short description of this topic.', verbose_name='description'),
        ),
    ]
