# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-08 21:18
from __future__ import unicode_literals

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0006_auto_20161219_1914'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoiceitem',
            name='tax_rate',
            field=models.DecimalField(choices=[(Decimal('0.00'), 'no vat'), (Decimal('0.20'), 'standard vat rate')], decimal_places=2, default=Decimal('0.00'), max_digits=4, verbose_name='tax rate'),
        ),
    ]
