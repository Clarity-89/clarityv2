# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-02-28 18:55
from __future__ import unicode_literals

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='description',
            field=ckeditor.fields.RichTextField(blank=True),
        ),
    ]
