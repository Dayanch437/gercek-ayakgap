from django.db import models


class CartStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    CANCELLED = "CANCELLED", "Cancelled"
    COMPLETED = "COMPLETED", "Completed"
    DELIVERED = "DELIVERED", "Delivered"

class OrderStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    DELIVERED = "DELIVERED", "Delivered"