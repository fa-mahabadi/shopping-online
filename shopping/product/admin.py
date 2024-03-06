from django.contrib import admin
from .models import Category , Product ,Discount, DiscountCode, Comment, Image
# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Discount)
admin.site.register(DiscountCode)
admin.site.register(Comment)

from django.contrib import admin
from .models import Image

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
