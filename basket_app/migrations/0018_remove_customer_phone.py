# Generated by Django 3.2.3 on 2021-06-14 06:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basket_app', '0017_auto_20210614_1217'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='phone',
        ),
    ]
