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
        # if user.is_supervisor:
        #     supervisor_group, created = Group.objects.get_or_create(name='SUPERVISOR')
        #     user.groups.add(supervisor_group)

        # if user.is_product_manager:
        #     product_manager_group, created = Group.objects.get_or_create(name='PRODUCT_MANAGER')
        #     user.groups.add(product_manager_group)

        # if user.is_operator:
        #     operator_group, created = Group.objects.get_or_create(name='OPERATOR')
        #     user.groups.add(operator_group)
        # return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self.create_user(email, password, **extra_fields)


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
