from django.db import models
from apps.cart.models import User

class Category(models.Model):
    name = models.CharField(max_length=100,unique=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="product/images",null=True, blank=True)

    def __str__(self):
        return self.name


    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Product(models.Model):
    name = models.CharField(max_length=25, unique=True)
    image = models.ImageField(upload_to="products/images",blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    stock = models.IntegerField()
    is_available = models.BooleanField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    stars = models.IntegerField(default=0)
    def __str__(self):
        return self.name

class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='comments')

    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.text},by {self.user}"


class Image(models.Model):
    image = models.ImageField(upload_to="products/images", blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='pictures',blank=True, null=True)
    class Meta:
        verbose_name_plural = 'images'
        db_table = 'products_images'

    def __str__(self):
        return self.image.name

