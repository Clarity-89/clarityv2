# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-02-28 20:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0002_auto_20180228_2055'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='url',
            field=models.URLField(null=True, verbose_name='URL'),
        ),
    ]
