# Generated by Django 3.2.3 on 2021-06-14 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basket_app', '0023_alter_receiver_phone'),
    ]

    operations = [
        migrations.RenameField(
            model_name='receiver',
            old_name='custname',
            new_name='recname',
        ),
        migrations.AlterField(
            model_name='receiver',
            name='phone',
            field=models.CharField(blank=True, max_length=10),
        ),
    ]