from django.db import models
from customer.models import MyUser, Address
from product.models import DiscountCode, Product, Image
from core.models import TimeStampModel, LogicalBaseModel, LogicalManager


class Order(TimeStampModel, LogicalBaseModel):
    STATUS_CHOICES = [
        ("کارت", "کارت"),
        ("پرداخت", "پرداخت"),
        ("تسویه", "تسویه"),
    ]

    user = models.ForeignKey(
        MyUser, on_delete=models.CASCADE, related_name="orders", verbose_name="کاربر"
    )
    address = models.ForeignKey(
        Address,
        on_delete=models.CASCADE,
        null=True,
        related_name="orders",
        verbose_name="آدرس ",
    )
    discount_code = models.OneToOneField(
        DiscountCode,
        on_delete=models.SET_NULL,
        null=True,
        related_name="orders",
        verbose_name="کدتخفیف",
    )
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="CART", verbose_name="وضعیت"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    objects = LogicalManager()

    class Meta:
        verbose_name_plural = " سفارشات  "
        verbose_name = " سفارش"


class OrderItem(LogicalBaseModel, TimeStampModel):
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
    quantity = models.IntegerField(default=1, verbose_name="تعداد سفارش")
    objects = LogicalManager()

    def get_product_image(self):
        try:
            product_image = Image.objects.get(
                product_id=self.product.id
            ).get_image_url()
        except Image.DoesNotExist:
            product_image = None
        return product_image

    class Meta:
        verbose_name_plural = "آیتم های سفارش  "
        verbose_name = "آیتم سفارش"
