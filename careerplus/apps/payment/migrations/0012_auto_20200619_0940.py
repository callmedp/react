# Generated by Django 2.2.10 on 2020-06-19 04:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0011_auto_20190821_1848'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymenttxn',
            name='payment_mode',
            field=models.IntegerField(choices=[(0, 'Not Paid'), (1, 'Cash'), (2, 'Citrus Pay'), (3, 'EMI'), (4, 'Cheque or Draft'), (5, 'CC-Avenue'), (6, 'Mobikwik'), (7, 'CC-Avenue-International'), (8, 'Debit Card'), (9, 'Credit Card'), (10, 'Net Banking'), (11, 'Paid Free'), (12, 'EPAYLATER'), (13, 'PAYU'), (14, 'Zest Money'), (15, 'RazorPay')], default=0),
        ),
    ]
