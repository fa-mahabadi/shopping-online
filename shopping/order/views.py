from django.shortcuts import render
from .serializers import OrderItemSerializer, OrderSerializer
from .models import Order, OrderItem
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.signals import user_logged_in
import json
from product.models import Product, Image
from django.http import JsonResponse
from customer.models import Address


class OrderAPIView(APIView):
    """create order after user login"""

    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):

        shopping_cart_cookie = request.COOKIES.get("shopping_cart")
        if not shopping_cart_cookie:
            return JsonResponse(
                {"error": "Shopping cart data not found in cookie"}, status=400
            )
        try:
            shopping_cart_data = json.loads(shopping_cart_cookie)
        except json.JSONDecodeError as e:
            return JsonResponse(
                {"error": "Error decoding shopping cart data: " + str(e)}, status=400
            )

        order_data = {
            "user": request.user.id,
            "status": "پرداخت",
        }
        order_serializer = OrderSerializer(data=order_data, partial=True)

        if order_serializer.is_valid():
            order = order_serializer.save()

            order_items_data = []
            for product_id, value in shopping_cart_data.items():

                order_items_data.append(
                    {
                        "order": order.id,
                        "product": product_id,
                        "quantity": value["quantity"],
                    }
                )

            order_item_serializer = OrderItemSerializer(
                data=order_items_data, many=True
            )
            if order_item_serializer.is_valid():
                order_item_serializer.save()
                return JsonResponse(order_serializer.data, status=201)
            else:
                return JsonResponse(
                    order_item_serializer.errors, status=400, safe=False
                )
        else:
            return JsonResponse(order_serializer.errors, status=400)

    def put(self, request):
        order_id = Order.objects.filter(status="پرداخت", user=request.user)
        address_id = request.data.get("address_id")
        try:
            address_instance = Address.objects.get(pk=address_id)
        except Address.DoesNotExist:
            return JsonResponse({"error": "Address not found"}, status=400)

        for order in order_id:
            order.address = address_instance
            order.save()

        return JsonResponse({"message": "Addresses updated successfully"})

    def get(self, request):
        user = request.user
        orders = Order.objects.filter(user=user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


def history_order(request):
    """render history order"""
    return render(request, "order/order_history.html")


class OrderItemAPIView(APIView):
    """order item get"""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        order_item = OrderItem.objects.filter(order__user=request.user)
        serializer = OrderItemSerializer(order_item, many=True)
        return Response(serializer.data)


class OrderItemDetailAPIView(APIView):
    """order item put and delete"""

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return OrderItem.objects.get(pk=pk)
        except OrderItem.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        order_item = get_object_or_404(OrderItem, pk=pk)
        serializer = OrderItemSerializer(order_item)
        return Response(serializer.data)

    def put(self, request, pk):
        order_item = self.get_object(pk)
        serializer = OrderItemSerializer(order_item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self, request, pk):
        order_item = self.get_object(pk)
        order_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
