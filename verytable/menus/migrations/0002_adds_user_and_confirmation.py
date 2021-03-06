# Generated by Django 3.1.13 on 2021-09-03 18:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('menus', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='menu',
            options={'ordering': ['date'], 'verbose_name': 'menus', 'verbose_name_plural': 'menus'},
        ),
        migrations.AddField(
            model_name='reservation',
            name='confirmed',
            field=models.BooleanField(default=False, verbose_name='confirmed'),
        ),
        migrations.AddField(
            model_name='reservation',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
        migrations.AddField(
            model_name='reservation',
            name='validated',
            field=models.BooleanField(default=False, verbose_name='validated'),
        ),
    ]
