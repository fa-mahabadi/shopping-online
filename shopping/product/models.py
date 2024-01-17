from django.db import models
from django.utils.html import mark_safe


class Discount(models.Model):
    name=models.CharField(null=True,blank=True, max_length=100)
    percentage = models.PositiveIntegerField(null=True,blank=True)
    code = models.CharField(null=True, max_length=100,blank=True)
    cash_amount = models.FloatField(null=True,blank=True)
    expire = models.DateTimeField(null=True,blank=True)
    maximum = models.FloatField(default=0)

    def __str__(self):
        return f"{self.name}"


class Category(models.Model):
    name = models.CharField(max_length=100)
    parent_category = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.SET_NULL
    )
    discount = models.OneToOneField(Discount, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"


class Product(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products"
    )
    discount = models.ForeignKey(
        Discount, on_delete=models.CASCADE, related_name="products"
    )
    total_count = models.PositiveIntegerField()
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    price = models.FloatField()
    colors = [
        ("سفید", "سفید"),
        ("مشکی", "مشکی"),
        ("آبی", "آبی"),
        ("قرمز", "قرمز"),
        ("سبز", "سبز"),
    ]
    color = models.CharField(choices=colors, max_length=10)
    sizes = [("M", "M"), ("L", "L"), ("XL", "XL"), ("XXL", "XXL")]
    size = models.CharField(choices=sizes, max_length=10)

    def __str__(self):
        return f"{self.name}"


class Image(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(
        verbose_name="ItemImage", upload_to="images/product", null=True, blank=True
    )

    # def image_preview(self):
    #      return mark_safe('<img src="/../../media/%s" width="150" height="150" />' % (self.image))
    @property
    def thumbnail_preview(self):
        if self.image:
            return mark_safe(
                '<img src= "{}" width="200" height="200" />'.format(self.image.url)
            )


class DiscountCode(models.Model):
    name=models.CharField(null=True,blank=True, max_length=100)
    percentage = models.PositiveIntegerField(null=True,blank=True)
    code = models.CharField(null=True, max_length=100,blank=True)
    cash_amount = models.FloatField(null=True,blank=True)
    expire = models.DateTimeField(null=True,blank=True)
    maximum = models.FloatField(default=0)

    def __str__(self):
        return f"{self.name}"


class Comment(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="comments"
    )
    reply_to = models.ForeignKey(
        "self", null=True, on_delete=models.SET_NULL, related_name="comments"
    )
    content = models.CharField(max_length=200)
    email = models.EmailField()

    def __str__(self):
        return f"{self.product.name}"
