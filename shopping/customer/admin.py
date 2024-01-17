from django.contrib.auth.models import Group
from django.contrib import admin
from .models import MyUser,Address
# Register your models here.
# admin.site.register(MyUser)
admin.site.register(Address)
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MyUser


class MyUserAdmin(UserAdmin):
    model = MyUser
    list_display = ['email', 'is_supervisor', 'is_product_manager', 'is_operator']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                    'groups', 'user_permissions')}),
        ('Custom Fields', {'fields': ('is_supervisor', 'is_product_manager', 'is_operator')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_supervisor', 'is_product_manager', 'is_operator'),
        }),
    )

admin.site.register(MyUser, MyUserAdmin)







