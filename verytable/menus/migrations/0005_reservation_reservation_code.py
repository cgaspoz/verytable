# Generated by Django 3.1.13 on 2021-09-06 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0004_rename_code_uuid'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='reservation_code',
            field=models.CharField(blank=True, max_length=25, null=True, verbose_name='reservation code'),
        ),
    ]
