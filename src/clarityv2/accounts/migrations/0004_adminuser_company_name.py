# Generated by Django 2.2.9 on 2020-01-29 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20190930_2103'),
    ]

    operations = [
        migrations.AddField(
            model_name='adminuser',
            name='company_name',
            field=models.CharField(blank=True, max_length=255, verbose_name='company name'),
        ),
    ]
