from .models import Category, Product, Discount, DiscountCode, Comment, Image
from django.contrib import admin
from .models import Image


# Register your models here.
@admin.register(Category)
class MyCategory(admin.ModelAdmin):
    list_display = ["name", "parent_category", "discount"]
    list_filter = ["name"]
    search_fields = ["name"]


@admin.register(Product)
class MyProduct(admin.ModelAdmin):
    list_display = [
        "category",
        "discount",
        "total_count",
        "name",
        "brand",
        "price",
        "color",
        "size",
    ]
    list_filter = ["category"]
    search_fields = ["name"]


@admin.register(Discount)
class MyDiscount(admin.ModelAdmin):
    list_display = ["name", "percentage", "code", "cash_amount", "expire", "maximum"]
    list_filter = ["percentage"]
    search_fields = ["name"]


@admin.register(DiscountCode)
class MyDiscountCode(admin.ModelAdmin):
    list_display = ["name", "percentage", "code", "cash_amount", "expire", "maximum"]
    list_filter = ["percentage"]
    search_fields = ["name"]


@admin.register(Comment)
class MyComment(admin.ModelAdmin):
    list_display = ["product", "reply_to", "content", "email"]
    list_filter = ["product"]
    search_fields = ["product"]


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    readonly_fields = ["thumbnail_preview"]
    list_display = ["thumbnail_preview"]

    def thumbnail_preview(self, obj):
        return obj.thumbnail_preview

    thumbnail_preview.short_description = "پیش نمایش"
    thumbnail_preview.allow_tags = True

    def image_preview(self, obj):
        return obj.image_preview()

    image_preview.short_description = "Image Preview"
    image_preview.allow_tags = True
