# Generated by Django 2.2.10 on 2020-06-11 19:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0098_merge_20200609_0209'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='ref_order',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='order.Order'),
        ),
    ]
