from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.models import Group
from core.models import TimeStampModel, LogicalBaseModel, LogicalManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        extra_fields.setdefault("is_staff", True)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self.create_user(email, password, **extra_fields)

    # def create_supervisor(self, email, password=None, **extra_fields):
    #     user = self.create_user( email=email, password=password)
    #     supervisor_permissions = ["view_product",
    #             "view_group",
    #             "view_permission",
    #             "view_category",
    #             "view_discount",
    #             "view_image",
    #             "view_myuser",
    #             "view_address",
    #             "view_order",
    #             "view_discountcode",
    #             "view_comment",
    #             "view_orderitem",]
    #     self._add_permissions_to_user(user, supervisor_permissions)
    #     self._add_user_to_group(user, "Supervisors")
    #     return user

    # def create_product_manager(self, email, password=None, **extra_fields):
    #     user = self.create_user( email=email, password=password)
    #     product_manager_permissions = ["view_product",
    #             "add_product",
    #             "change_product",
    #             "delete_product",
    #             "view_category",
    #             "add_category",
    #             "change_category",
    #             "delete_category",
    #             "view_discount",
    #             "add_discount",
    #             "change_discount",
    #             "delete_discount",]
    #     self._add_permissions_to_user(user, product_manager_permissions)
    #     self._add_user_to_group(user, "ProductManagers")
    #     return user

    # def create_operator(self, email, password=None, **extra_fields):
    #     user = self.create_user( email=email, password=password)
    #     operator_permissions = ["view_myuser",
    #             "add_myuser",
    #             "change_myuser",
    #             "delete_myuser",
    #             "view_address",
    #             "add_address",
    #             "change_address",
    #             "delete_address",
    #             "view_order",
    #             "add_order",
    #             "change_order",
    #             "delete_order",]
    #     self._add_permissions_to_user(user, operator_permissions)
    #     self._add_user_to_group(user, "Operators")
    #     return user

    # def _add_permissions_to_user(self, user, permissions):
    #     for permission_codename in permissions:
    #         permission = Permission.objects.get(codename=permission_codename)
    #         user.user_permissions.add(permission)

    # def _add_user_to_group(self, user, group_name):
    #     group, created = Group.objects.get_or_create(name=group_name)
    #     user.groups.add(group)


class MyUser(AbstractUser, TimeStampModel,LogicalBaseModel):
    email = models.EmailField(unique=True, verbose_name="ایمیل")
    is_staff = models.BooleanField(default=True, verbose_name="کارمند")
    is_supervisor = models.BooleanField(default=False, verbose_name="ناظر")
    is_product_manager = models.BooleanField(default=False, verbose_name="مدیر محصول")
    is_operator = models.BooleanField(default=False, verbose_name="اپراتور")
    username = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
    logical_manager = LogicalManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name_plural = "  کاربران  "
        verbose_name = " کاربر"


class Address(LogicalBaseModel):
    user = models.ForeignKey(
        MyUser, on_delete=models.CASCADE, related_name="addresses", verbose_name="کاربر"
    )
    city = models.CharField(max_length=100, verbose_name="شهر")
    province = models.CharField(max_length=100, verbose_name="استان")
    detail = models.CharField(max_length=100, verbose_name="آدرس تکمیلی")
    zipcode = models.CharField(max_length=100, verbose_name="کدپستی")
    objects = LogicalManager()

    class Meta:
        verbose_name_plural = "آدرس ها  "
        verbose_name = " آدرس"
    def __str__(self):
        return self.city
