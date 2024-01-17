from django.test import TestCase
from .models import Order, OrderItem
from customer.models import MyUser
from product.models import DiscountCode,Discount,Category,Product
from django.utils import timezone


class OrderTest(TestCase):
    def setUp(self):
        self.user = MyUser.objects.create_user(email="test@email.com", password="123")
        self.discountcode = DiscountCode.objects.create(
            percentage=10,
            code="test",
            cash_amount=2.0,
            expire=timezone.now() + timezone.timedelta(days=10),
            maximum=30.0,
        )

    def test_order(self):
        order = Order.objects.create(
            user=self.user, discount_code=self.discountcode, status="کارت"
        )
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.discount_code, self.discountcode)
        self.assertEqual(order.status, "کارت")


class OrderItemTest(TestCase):
    def setUp(self):
        self.discount = Discount.objects.create(
            percentage=5,
            code="test",
            cash_amount=2.0,
            expire=timezone.now() + timezone.timedelta(days=10),
            maximum=10.0,
        )
        self.category = Category.objects.create(
            name="category", parent_category=None, discount=self.discount
        )
        self.product = Product.objects.create(
            category=self.category,
            discount=self.discount,
            total_count=100,
            name="product",
            brand="brand",
            price=100.0,
            color="مشکی",
            size="M",
        )
        self.user = MyUser.objects.create_user(email="test@email.com", password="123")
        self.discountcode = DiscountCode.objects.create(
            percentage=10,
            code="test",
            cash_amount=2.0,
            expire=timezone.now() + timezone.timedelta(days=10),
            maximum=30.0,
        )
        self.order = Order.objects.create(
            user=self.user, discount_code=self.discountcode, status="کارت"
        )

    def test_orderitem(self):
        orderitem = OrderItem.objects.create(
            product=self.product, order=self.order, quantity=10
        )
        self.assertEqual(orderitem.product,self.product)
        self.assertEqual(orderitem.order,self.order)
        self.assertEqual(orderitem.quantity,10)
