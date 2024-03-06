from django.test import TestCase
from .models import Discount, DiscountCode, Category, Product, Image, Comment
from django.utils import timezone


class DiscountTest(TestCase):
    def test_discount(self):
        discount = Discount.objects.create(
            percentage=10,
            code="Test Code",
            cash_amount=5.0,
            expire=timezone.now() + timezone.timedelta(days=7),
            maximum=30.0,
        )

        self.assertEqual(discount.percentage, 10)
        self.assertEqual(discount.code, "Test Code")
        self.assertEqual(discount.cash_amount, 5.0)
        self.assertLessEqual(
            discount.expire, timezone.now() + timezone.timedelta(days=7)
        )
        self.assertEqual(discount.maximum, 30.0)


class DiscountCodeTest(TestCase):
    def test_discountcode(self):
        discountcode = DiscountCode.objects.create(
            percentage=10,
            code="test",
            cash_amount=2.0,
            expire=timezone.now() + timezone.timedelta(days=10),
            maximum=30.0,
        )
        self.assertEqual(discountcode.percentage, 10)
        self.assertEqual(discountcode.code, "test")
        self.assertEqual(discountcode.cash_amount, 2.0)
        self.assertEqual(discountcode.maximum, 30.0)

    def test_discountcode_expire(self):
        discountcode = DiscountCode.objects.create(
            percentage=10,
            code="test",
            cash_amount=2.0,
            expire=timezone.now() + timezone.timedelta(days=1),
            maximum=30.0,
        )
        self.assertEqual(discountcode.percentage, 10)
        self.assertEqual(discountcode.code, "test")
        self.assertEqual(discountcode.cash_amount, 2.0)
        self.assertNotEqual(
            discountcode.expire, timezone.now() + timezone.timedelta(days=10)
        )
        self.assertEqual(discountcode.maximum, 30.0)


class CategoryTest(TestCase):
    def setUp(self):
        self.discount = Discount.objects.create(
            percentage=5,
            code="test",
            cash_amount=2.0,
            expire=timezone.now() + timezone.timedelta(days=7),
            maximum=10.0,
        )

    def test_category(self):
        category = Category.objects.create(
            name="category", parent_category=None, discount=self.discount
        )
        self.assertEqual(category.name, "category")
        self.assertEqual(category.parent_category, None)
        self.assertEqual(category.discount, self.discount)


class ProductTest(TestCase):
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

    def test_product(self):
        product = Product.objects.create(
            category=self.category,
            discount=self.discount,
            total_count=100,
            name="product",
            brand="brand",
            price=100.0,
            color="مشکی",
            size="M",
        )
        self.assertEqual(product.category, self.category)
        self.assertEqual(product.discount, self.discount)
        self.assertNotEqual(product.total_count, 50)
        self.assertEqual(product.name, "product")
        self.assertEqual(product.brand, "brand")
        self.assertNotEqual(product.price, 200.0)
        self.assertNotEqual(product.color, "سفید")
        self.assertNotEqual(product.size, "L")

    class ImageTest(TestCase):
        def setUp(self):
            self.discount = Discount.objects.create(
                percentage=5,
                code="test",
                cash_amount=2.0,
                expire=timezone.now() + timezone.timedelta(days=12),
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

        def test_image(TestCase):
            my_image = Image.create.objects(
                product=self.product, image="images/product/test_image.jpg"
            )
            self.assertEqual(my_image.image, "images/product/test_image.jpg")
            self.assertEqual(product, self.product)


class CommentTest(TestCase):
    def setUp(self):
        self.discount = Discount.objects.create(
            percentage=5,
            code="test",
            cash_amount=2.0,
            expire=timezone.now() + timezone.timedelta(days=12),
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

    def test_comment(self):
        comment = Comment.objects.create(
            product=self.product,
            reply_to=None,
            content="this is test comment",
            email="user@email.com",
        )
        self.assertEqual(comment.product, self.product)
        self.assertIsNone(comment.reply_to, None)
        self.assertEqual(comment.content, "this is test comment")
        self.assertEqual(comment.email, "user@email.com")
