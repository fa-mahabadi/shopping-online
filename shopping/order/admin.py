from django.contrib import admin
from .models import Order, OrderItem


# Register your models here.
@admin.register(Order)
class MyOrder(admin.ModelAdmin):
    list_display = ["user", "discount_code", "status"]
    readonly_fields = ["created_at"]
    list_filter = ["created_at"]
    search_fields = ["status"]


@admin.register(OrderItem)
class MyOrderItem(admin.ModelAdmin):
    list_display = ["product", "order", "quantity"]
    list_filter = ["product"]
    search_fields = ["product"]
