# Generated by Django 5.0 on 2024-08-22 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('atm', '0006_alter_customer_pin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='pin',
            field=models.IntegerField(max_length=5),
        ),
    ]
