from django.db import models
from customer.models import MyUser
from product.models import DiscountCode, Product


class Order(models.Model):
    STATUS_CHOICES = [
        ("کارت", "کارت"),
        ("پرداخت", "پرداخت"),
        ("تسویه", "تسویه"),
    ]

    user = models.ForeignKey(
        MyUser, on_delete=models.CASCADE, related_name="orders", verbose_name="کاربر"
    )
    discount_code = models.OneToOneField(
        DiscountCode,
        on_delete=models.CASCADE,
        related_name="orders",
        verbose_name="کدتخفیف",
    )
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="CART", verbose_name="وضعیت"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")

    class Meta:
        verbose_name_plural = "سفارشات"
        verbose_name = "سفارش"


class OrderItem(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="order_items",
        verbose_name="محصول",
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="order_items",
        verbose_name="سفارش",
    )
    quantity = models.IntegerField(default=1, verbose_name="تعداد")

    class Meta:
        verbose_name_plural = "آیتم های سفارش"
        verbose_name = "آیتم سفارش"
