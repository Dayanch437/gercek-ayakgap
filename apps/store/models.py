from django.db import models
from django.db.models import Avg, Count
from apps.utils.models import BaseModel
from apps.utils.fields import CompressedImageField

class Category(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    image = CompressedImageField(upload_to="product/images", null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Product(BaseModel):
    name = models.CharField(max_length=25, unique=True)
    image = CompressedImageField(upload_to="products/images", blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    stock = models.IntegerField()
    is_available = models.BooleanField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')

    @property
    def average_rating(self):
        """Calculate average rating from related ratings"""
        result = self.ratings.aggregate(
            average=Avg('stars'),
            count=Count('id')
        )
        return {
            'average': result['average'] or 0,
            'count': result['count']
        }

    @property
    def stars(self):
        """Backward compatibility - returns just the average"""
        return int(round(self.average_rating['average'] or 0))

    def __str__(self):
        return self.name


class Rating(BaseModel):
    """New model to store individual ratings"""
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='ratings'
    )
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='product_ratings',
        blank=True,
        null=True
    )
    stars = models.PositiveSmallIntegerField(
        choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]
    )
    comment = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('product', 'user')  # Prevent multiple ratings

    def __str__(self):
        return f"{self.stars} stars by {self.user} for {self.product}"


class Comment(BaseModel):  # Changed from Comments to Comment (Django convention)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    def __str__(self):
        return f"{self.text}, by {self.user}"


class Image(BaseModel):
    image = CompressedImageField(upload_to="products/images", blank=True)
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='pictures',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name_plural = 'images'
        db_table = 'products_images'

    def __str__(self):
        return self.image.name