# Generated by Django 4.2 on 2024-02-25 12:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0009_alter_address_zipcode'),
        ('order', '0008_alter_order_discount_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='address',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='customer.address', verbose_name='آدرس '),
        ),
    ]
