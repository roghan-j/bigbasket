# Generated by Django 3.2.3 on 2021-06-14 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basket_app', '0021_alter_receiver_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='receiver',
            name='address',
            field=models.CharField(blank=True, max_length=256),
        ),
        migrations.AlterField(
            model_name='receiver',
            name='custname',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
