# Generated by Django 2.2.4 on 2019-12-17 18:59

from django.db import migrations
import privates.fields
import privates.storages


class Migration(migrations.Migration):

    dependencies = [
        ('deductions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deduction',
            name='receipt',
            field=privates.fields.PrivateMediaFileField(blank=True, storage=privates.storages.PrivateMediaFileSystemStorage(), upload_to='receipts/%Y/%m', verbose_name='receipt'),
        ),
    ]
