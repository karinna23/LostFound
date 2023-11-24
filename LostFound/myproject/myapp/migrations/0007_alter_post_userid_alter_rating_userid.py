# Generated by Django 4.0 on 2023-10-11 13:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_alter_customuser_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='userID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.customuser'),
        ),
        migrations.AlterField(
            model_name='rating',
            name='userID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.customuser'),
        ),
    ]