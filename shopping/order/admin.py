from django.contrib import admin
from .models import Order, OrderItem


# Register your models here.
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["user", "discount_code", "status", "created_at"]
    search_fields = ("user",)
    list_filter = ("status",)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ["product", "order", "quantity"]
    search_fields = ("product",)
    list_filter = ("product",)
