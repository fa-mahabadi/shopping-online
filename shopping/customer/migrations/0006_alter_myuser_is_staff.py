# Generated by Django 5.0.1 on 2024-02-01 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0005_alter_myuser_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
    ]
