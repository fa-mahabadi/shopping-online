from django.contrib import admin
from .models import Category, Product, Discount, DiscountCode, Comment, Image


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "parent_category", "discount"]
    search_fields = ("name",)
    list_filter = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
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
    search_fields = ("name", "description")
    list_filter = ("price",)


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ["name", "percentage", "code", "cash_amount", "expire", "maximum"]
    search_fields = ("name",)
    list_filter = ("expire",)


@admin.register(DiscountCode)
class DiscountCodeAdmin(admin.ModelAdmin):
    list_display = ["name", "percentage", "code", "cash_amount", "expire", "maximum"]
    search_fields = ("name",)
    list_filter = ("expire",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["product", "reply_to", "content", "email"]
    search_fields = ("email",)
    list_filter = ("product",)


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
