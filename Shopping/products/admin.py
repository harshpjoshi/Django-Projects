from django.contrib import admin
from .models import Product,MainCategory,SubCategory,Cart,Order
# Register your models here.

admin.site.register(Product)
admin.site.register(SubCategory)
admin.site.register(MainCategory)
admin.site.register(Cart)
admin.site.register(Order)
