# Generated by Django 4.0 on 2023-10-13 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0014_remove_customuser_profile_picture_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(max_length=200),
        ),
    ]
