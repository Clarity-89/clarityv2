# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-15 20:54
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work_entries', '0002_auto_20161219_1914'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='workentry',
            options={'ordering': ('-date',), 'verbose_name': 'work entry', 'verbose_name_plural': 'work entries'},
        ),
        migrations.RemoveField(
            model_name='workentry',
            name='end',
        ),
        migrations.RemoveField(
            model_name='workentry',
            name='start',
        ),
        migrations.AddField(
            model_name='workentry',
            name='date',
            field=models.DateField(default=datetime.date.today, verbose_name='date'),
        ),
        migrations.AddField(
            model_name='workentry',
            name='duration',
            field=models.DurationField(default=datetime.timedelta, verbose_name='duration'),
            preserve_default=False,
        ),
    ]
