# Generated by Django 2.2.4 on 2019-08-17 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20190717_2245'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='image_credit',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='image_credit'),
        ),
    ]
