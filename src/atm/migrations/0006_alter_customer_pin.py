# Generated by Django 5.0 on 2024-08-22 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('atm', '0005_alter_user_options_remove_customer_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='pin',
            field=models.IntegerField(max_length=5, unique=True),
        ),
    ]