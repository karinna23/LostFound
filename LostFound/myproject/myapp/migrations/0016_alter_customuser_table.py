# Generated by Django 4.0 on 2023-10-13 11:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0015_alter_customuser_email'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='customuser',
            table='custom_user',
        ),
    ]