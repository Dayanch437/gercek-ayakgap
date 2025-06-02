from django.contrib import admin

from .models import Category, Comment, Image, Product

# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Comment)
admin.site.register(Image)