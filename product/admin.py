from django.contrib import admin
from product.models import Product, Category, ProductComment


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug','description', 'price',
                     'discount', 'status', 'created']
    

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug','description', 'created', 'status']


@admin.register(ProductComment)
class ProductCommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'created', 'updated', 'status']