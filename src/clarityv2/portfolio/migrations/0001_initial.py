# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-02-27 19:20
from __future__ import unicode_literals

import autoslug.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='name', unique=True, verbose_name='slug')),
                ('image', models.ImageField(blank=True, upload_to='portfolio', verbose_name='image')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('order', models.PositiveIntegerField(default=0)),
                ('published', models.BooleanField(default=True, verbose_name='published')),
            ],
            options={
                'ordering': ['order'],
                'verbose_name_plural': 'portfolio entries',
                'verbose_name': 'portfolio entry',
            },
        ),
    ]