from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import MyUser, Address


@admin.register(MyUser)
class MyUserAdmin(UserAdmin):
    list_display = [
        "email",
        "is_supervisor",
        "is_product_manager",
        "is_operator",
        "is_staff",
        "is_active",
        "is_deleted",
    ]
    search_fields = ("email",)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    ordering = ("email",)

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
                    "is_active",
                    "is_deleted",
                ),
            },
        ),
    )


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ["user", "city", "province", "detail", "zipcode","is_active",
                    "is_deleted",]
    search_fields = ("user", "city")
    list_filter = ("user",)
