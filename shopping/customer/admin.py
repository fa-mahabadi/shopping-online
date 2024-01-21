from .models import MyUser, Address


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MyUser


@admin.register(MyUser)
class MyUserAdmin(UserAdmin):
    list_display = ["email", "is_supervisor", "is_product_manager", "is_operator"]
    search_fields = ("email",)
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
class MyAddress(admin.ModelAdmin):
    list_display = ["user", "city", "province", "detail", "zipcode"]
    list_filter = ["city"]
    search_fields = ["city", "user"]
