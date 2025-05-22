from .models import Comments, Product,Image,Category

from django.contrib import admin

# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Comments)
admin.site.register(Image)