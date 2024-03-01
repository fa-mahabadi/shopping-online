from django.test import TestCase
from .models import MyUser, Address
from django.contrib.auth import get_user_model


class UserManagerTest(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(email="test@email.com", password="123")
        self.assertEqual(user.email, "test@email.com")
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            email="admin@email.com", password="12345"
        )
        self.assertEqual(admin_user.email, "admin@email.com")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)


class AddresTest(TestCase):
    def setUp(self):
        self.user = MyUser.objects.create(email="admin@email.com", password="123")

    def test_address_creation(self):
        address = Address.objects.create(
            user=self.user,
            city="Tehran",
            province="Tehran",
            detail=" Detail",
            zipcode="12345",
        )
        self.assertEqual(address.user, self.user)
        self.assertEqual(address.city, "Tehran")
        self.assertEqual(address.province, "Tehran")
        self.assertEqual(address.detail, " Detail")
        self.assertEqual(address.zipcode, "12345")
