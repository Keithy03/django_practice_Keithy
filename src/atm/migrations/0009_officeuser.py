# Generated by Django 5.0 on 2024-08-22 15:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('atm', '0008_alter_customer_pin'),
    ]

    operations = [
        migrations.CreateModel(
            name='OfficeUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='atm.user')),
            ],
            options={
                'permissions': [('can_manage_client', 'Can manage client')],
            },
        ),
    ]
