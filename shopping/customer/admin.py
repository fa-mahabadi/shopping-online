from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import MyUser, Address


@admin.register(MyUser)
class MyUserAdmin(UserAdmin):
    model = MyUser
    list_display = ["email", "is_supervisor", "is_product_manager", "is_operator"]

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            "Custom Fields",
            {"fields": ("is_supervisor", "is_product_manager", "is_operator")},
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_supervisor",
                    "is_product_manager",
                    "is_operator",
                ),
            },
        ),
    )


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ["user", "city", "province", "detail", "zipcode"]
    search_fields = ("user", "city")
    list_filter = ("user",)
