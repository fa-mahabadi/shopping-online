from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.apps import apps
from django.conf import settings

MyUser = apps.get_model(settings.AUTH_USER_MODEL)


@receiver(post_save, sender=MyUser)
def add_user_to_special_group(sender, instance, created, **kwargs):
    if created:
        if instance.is_supervisor:
            instance.is_staff=True
            Supervisors, created = Group.objects.get_or_create(name="Supervisors")
            permissions = [
                "view_product",
                "view_group",
                "view_permission",
                "view_category",
                "view_discount",
                "view_image",
                "view_myuser",
                "view_address",
                "view_order",
                "view_discountcode",
                "view_comment",
                "view_orderitem",
            ]
            for permission_codename in permissions:
                permission = Permission.objects.get(codename=permission_codename)
                Supervisors.permissions.add(permission)
            instance.groups.add(Supervisors)
        elif instance.is_product_manager:
            instance.is_staff=True
            ProductManagers, created = Group.objects.get_or_create(
                name="ProductManagers"
            )
            permissions = [
                "view_product",
                "add_product",
                "change_product",
                "delete_product",
                "view_category",
                "add_category",
                "change_category",
                "delete_category",
                "view_discount",
                "add_discount",
                "change_discount",
                "delete_discount",
            ]

            for permission_codename in permissions:
                permission = Permission.objects.get(codename=permission_codename)
                ProductManagers.permissions.add(permission)
            instance.groups.add(ProductManagers)
        elif instance.is_operator:
            instance.is_staff=True
            Operators, created = Group.objects.get_or_create(name="Operators")
            permissions = [
                "view_myuser",
                "add_myuser",
                "change_myuser",
                "delete_myuser",
                "view_address",
                "add_address",
                "change_address",
                "delete_address",
                "view_order",
                "add_order",
                "change_order",
                "delete_order",
            ]

            for permission_codename in permissions:
                permission = Permission.objects.get(codename=permission_codename)
                Operators.permissions.add(permission)
            instance.groups.add(Operators)


# Connect the signal
post_save.connect(add_user_to_special_group, sender=MyUser)


