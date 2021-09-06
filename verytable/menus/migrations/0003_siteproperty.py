# Generated by Django 3.1.13 on 2021-09-05 10:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0004_alter_options_ordering_domain'),
        ('menus', '0002_adds_user_and_confirmation'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteProperty',
            fields=[
                ('site_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='sites.site')),
                ('reservation_code', models.CharField(blank=True, max_length=25, null=True, verbose_name='reservation code')),
            ],
            bases=('sites.site',),
        ),
    ]
