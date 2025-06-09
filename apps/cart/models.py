from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.store.models import Product
from apps.utils.enums import CartStatus, OrderStatus
from apps.utils.models import BaseModel


class Cart(BaseModel):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,
        choices=CartStatus.choices,
        default=CartStatus.PENDING,
    )

    def __str__(self):
        return f"Cart of {self.user.username}"


class CartItem(BaseModel):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Cart"


class Order(BaseModel):
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='orders'
    )
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='order'
    )
    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING,
    )
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=120)
    phone = models.CharField(max_length=120)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return self.city

@receiver(post_save, sender=Order)
def send_order_update(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "order_updates",
        {
            "type": "order_update",
            "message": {
                "id": instance.id,
                "status": instance.status,
                "city": instance.city,
                "address": instance.address,
                "phone": instance.phone
            },
        },
    )
