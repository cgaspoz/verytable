# Generated by Django 3.1.13 on 2021-09-06 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0005_reservation_reservation_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='reservation_code',
            field=models.CharField(default='abcd', max_length=25, verbose_name='reservation code'),
            preserve_default=False,
        ),
    ]
