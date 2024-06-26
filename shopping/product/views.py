from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, TemplateView
from .models import Product, Image, Category
from django.http import JsonResponse, HttpResponse
import json
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
from order.models import OrderItem
from django.contrib.auth.decorators import login_required
from rest_framework import status


def home(request):
    """show home page"""
    newest_products = Product.objects.order_by('-created_at')[:3]
    images = Image.objects.all()
    return render(request, "index.html",{'newest_products': newest_products,"images":images})


class ProductListView(ListView):
    """product list view"""

    model = Product
    template_name = "product/product_list.html"
    context_object_name = "products"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(*kwargs)
        context["images"] = Image.objects.all()
        return context


class ProductDetailView(DetailView):
    """product detail view"""

    model = Product
    template_name = "product/product_detail.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["images"] = Image.objects.all()
        return context


class WomanCategoryListView(ListView):
    """woman category footer"""

    model = Product
    template_name = "category/woman_list.html"
    context_object_name = "products"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(*kwargs)
        context["images"] = Image.objects.all()
        return context

    def get_queryset(self):
        return Product.objects.filter(category__name__icontains="زنانه")


class ManCategoryListView(ListView):
    """man category footer"""

    model = Product
    template_name = "category/man_list.html"
    context_object_name = "products"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(*kwargs)
        context["images"] = Image.objects.all()
        return context

    def get_queryset(self):
        return Product.objects.filter(category__name__icontains="مردانه")


class ChildrenCategoryListView(ListView):
    """child category footer"""

    model = Product
    template_name = "category/child_list.html"
    context_object_name = "products"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(*kwargs)
        context["images"] = Image.objects.all()

        return context

    def get_queryset(self):
        return Product.objects.filter(category__name__icontains="بچه گانه")


class CategoryDetailView(DetailView):
    """category detail that use in navbar"""

    model = Category
    template_name = "product/category_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.object
        context["products"] = Product.objects.filter(category=category)
        context["images"] = Image.objects.all()
        return context


class AddToCartView(View):
    """create cookie based product detail"""

    def post(self, request):
        product_id = request.POST.get("product_id")
        product_name = request.POST.get("product_name")
        product_price = request.POST.get("product_price")
        product_color = request.POST.get("product_color")
        product_size = request.POST.get("product_size")
        try:
            product_image = Image.objects.get(product_id=product_id).image.url
        except ProductImage.DoesNotExist:
            product_image = None
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            raise Http404("Product does not exist.")

        cart = request.COOKIES.get("shopping_cart")
        cart = json.loads(cart) if cart else {}

        cart_item = {
            "id": product_id,
            "name": product_name,
            "price": product_price,
            "color": product_color,
            "size": product_size,
            "quantity": 1,
            "image": product_image,
        }
        cart[str(product_id)] = cart_item
        # cart.update(cart_item)
        response = redirect("home")
        response.set_cookie("shopping_cart", json.dumps(cart))
        return response


class ProductAPIView(APIView):
    """api that display cookie get and update"""

    def get(self, request, format=None):
        shopping_cart_cookie = request.COOKIES.get("shopping_cart")
        if shopping_cart_cookie:
            shopping_cart_data = json.loads(shopping_cart_cookie)
        else:
            shopping_cart_data = {}
        return Response({"shopping_cart": shopping_cart_data})

    def post(self, request, format=None):
        shopping_cart_data = request.data.get("shopping_cart")
        if shopping_cart_data:
            response = Response({"success": True})
            response.set_cookie("shopping_cart", json.dumps(shopping_cart_data))
            # create_order_item(request.user, shopping_cart_data)
            return response
        else:
            return Response(
                {"success": False, "error": "No shopping cart data provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ProductTemplateView(TemplateView):
    """template that dispaly content api"""

    template_name = "product/product_template.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class UpdateQuantityView(View):
    """upadte quantity cookie"""

    def post(self, request):
        product_id = request.POST.get("product_id")
        new_quantity = int(request.POST.get("quantity"))
        cart = request.COOKIES.get("shopping_cart")
        cart = json.loads(cart) if cart else {}

        if product_id in cart:
            cart[product_id]["quantity"] = new_quantity

            response = JsonResponse({"success": True})
            response.set_cookie("shopping_cart", json.dumps(cart))
            return response
        else:
            return JsonResponse(
                {"success": False, "error": "Product not found in cart"}
            )


def product_search(request):
    """search product based name"""
    query = request.GET.get("q")
    products = Product.objects.filter(name__icontains=query) if query else []
    images = Image.objects.all()
    return render(
        request, "product/search_results.html", {"products": products, "images": images}
    )
