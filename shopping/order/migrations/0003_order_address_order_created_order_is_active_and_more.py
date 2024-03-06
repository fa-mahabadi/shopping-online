# Generated by Django 4.2 on 2024-02-15 10:51

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0008_alter_address_is_active_alter_address_is_deleted_and_more'),
        ('order', '0002_alter_order_options_alter_orderitem_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='address',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='customer.address', verbose_name='آدرس '),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='فعال'),
        ),
        migrations.AddField(
            model_name='order',
            name='is_deleted',
            field=models.BooleanField(default=False, verbose_name='حذف'),
        ),
        migrations.AddField(
            model_name='order',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orderitem',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='فعال'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='is_deleted',
            field=models.BooleanField(default=False, verbose_name='حذف'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]