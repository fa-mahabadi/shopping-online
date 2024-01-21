from django.db import models
from django.utils.html import mark_safe


class Discount(models.Model):
    name = models.CharField(null=True, blank=True, max_length=100, verbose_name="نام")
    percentage = models.PositiveIntegerField(
        null=True, blank=True, verbose_name="درصدی"
    )
    code = models.CharField(
        null=True, max_length=100, blank=True, verbose_name="کد تخفیف"
    )
    cash_amount = models.FloatField(null=True, blank=True, verbose_name="نقدی")
    expire = models.DateTimeField(null=True, blank=True, verbose_name="تاریخ انقضاء")
    maximum = models.FloatField(default=0, verbose_name="مقدار بیشینه")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name_plural = "  تخفیف ها"
        verbose_name = " تخفیف"


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="نام")
    parent_category = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="دسته بندی",
    )
    discount = models.OneToOneField(
        Discount, on_delete=models.CASCADE, verbose_name="تخفیف"
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name_plural = "دسته بندی ها"
        verbose_name = "دسته بندی"


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="دسته بندی",
    )
    discount = models.ForeignKey(
        Discount,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="تخفیف",
    )
    total_count = models.PositiveIntegerField(verbose_name="تعداد کل")
    name = models.CharField(max_length=100, verbose_name="نام")
    brand = models.CharField(max_length=100, verbose_name="برند")
    price = models.FloatField(verbose_name="قیمت")
    colors = [
        ("سفید", "سفید"),
        ("مشکی", "مشکی"),
        ("آبی", "آبی"),
        ("قرمز", "قرمز"),
        ("سبز", "سبز"),
    ]
    color = models.CharField(choices=colors, max_length=10, verbose_name="رنگ")
    sizes = [("M", "M"), ("L", "L"), ("XL", "XL"), ("XXL", "XXL")]
    size = models.CharField(choices=sizes, max_length=10, verbose_name="سایز")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name_plural = "محصولات"
        verbose_name = "محصول"


class Image(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images", verbose_name="محصول"
    )
    image = models.ImageField(
        verbose_name="عکس", upload_to="images/product", null=True, blank=True
    )

    # def image_preview(self):
    #      return mark_safe('<img src="/../../media/%s" width="150" height="150" />' % (self.image))
    @property
    def thumbnail_preview(self):
        if self.image:
            return mark_safe(
                '<img src= "{}" width="200" height="200" />'.format(self.image.url)
            )

    class Meta:
        verbose_name_plural = "تصاویر"
        verbose_name = "تصویر"


class DiscountCode(models.Model):
    name = models.CharField(null=True, blank=True, max_length=100, verbose_name="نام")
    percentage = models.PositiveIntegerField(
        null=True, blank=True, verbose_name="درصدی"
    )
    code = models.CharField(null=True, max_length=100, blank=True, verbose_name="کد")
    cash_amount = models.FloatField(null=True, blank=True, verbose_name="نقدی")
    expire = models.DateTimeField(null=True, blank=True, verbose_name="انقضاء")
    maximum = models.FloatField(default=0, verbose_name="مقدار بیشینه")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name_plural = "کدهای تخفیف"
        verbose_name = "کد تخفیف"


class Comment(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="comments", verbose_name="محصول"
    )
    reply_to = models.ForeignKey(
        "self",
        null=True,
        on_delete=models.SET_NULL,
        related_name="comments",
        verbose_name="پاسخ به",
    )
    content = models.CharField(max_length=200, verbose_name="متن")
    email = models.EmailField(verbose_name="ایمیل")

    def __str__(self):
        return f"{self.product.name}"

    class Meta:
        verbose_name_plural = "نظرات"
        verbose_name = "نظر"
