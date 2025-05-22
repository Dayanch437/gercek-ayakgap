from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
from apps.store.models import Product
from apps.utils.enums import CartStatus


class OrderStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    DELIVERED = "DELIVERED", "Delivered"

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,
        choices=CartStatus.choices,
        default=CartStatus.PENDING,
    )
    def __str__(self):
        return f"Cart of {self.user.username}"



class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Cart"



class Order(models.Model):
    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING,
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True,related_name='orders')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE,null=True, blank=True, related_name='order')
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=120)
    phone = models.CharField(max_length=120)

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return self.city