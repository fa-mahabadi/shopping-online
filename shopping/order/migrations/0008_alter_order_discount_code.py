# Generated by Django 4.2 on 2024-02-25 12:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0010_remove_image_is_primary_alter_comment_is_active_and_more'),
        ('order', '0007_order_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='discount_code',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='product.discountcode', verbose_name='کدتخفیف'),
        ),
    ]
