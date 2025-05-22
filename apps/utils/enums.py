from django.db import models


class CartStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    CANCELLED = "CANCELLED", "Cancelled"
    COMPLETED = "COMPLETED", "Completed"
    DELIVERED = "DELIVERED", "Delivered"

