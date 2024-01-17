from django.db import models
from  customer.models import MyUser
from product.models import DiscountCode,Product



class Order(models.Model):

    STATUS_CHOICES = [
        ('کارت', 'کارت'),
        ('پرداخت', 'پرداخت'),
        ('تسویه', 'تسویه'),
    ]

    user = models.ForeignKey(MyUser, on_delete=models.CASCADE,related_name="orders")
    discount_code=models.OneToOneField(DiscountCode,on_delete=models.CASCADE,related_name="orders")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='CART')
    created_at = models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):
   
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name="order_items")
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name="order_items")
    quantity=models.IntegerField(default=1)
