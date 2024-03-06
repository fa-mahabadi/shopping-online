from .models import Order, OrderItem
from rest_framework import serializers


class OrderItemSerializer(serializers.ModelSerializer):
    product_image = serializers.CharField(source="get_product_image", read_only=True)

    class Meta:
        model = OrderItem
        fields = ["id", "product", "order", "quantity", "product_image"]


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
