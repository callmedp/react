# Generated by Django 2.2.10 on 2020-06-05 04:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coupon', '0006_auto_20180207_1043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='site',
            field=models.PositiveIntegerField(choices=[(0, 'ALL SITE'), (1, 'Learning'), (2, 'CRM'), (3, 'Resume Shine')], default=0, verbose_name='Site'),
        ),
    ]
