from django.contrib import admin

from .models import Category, Comments, Image, Product

# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Comments)
admin.site.register(Image)