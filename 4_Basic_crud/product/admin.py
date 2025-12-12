"""
Docstring for product.admin
"""

# core import
from django.contrib import admin

# local imports
from .models import (
    Tag,
    Brand,
    Product,
)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = [
        'user_email',
        'title',
        'created_at',
    ]

    def user_email(self, obj):
        return obj.user.email


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = [
        'user_email',
        'title',
        'created_at',
    ]

    def user_email(self, obj):
        return obj.user.email

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'user_email',
        
        'title',
        'price',
        'stock_quantity',
        
        'brand',
        
        'is_returnable',        
        'warrantee_availability',
        
        'created_at',
    ]

    def user_email(self, obj):
        return obj.user.email
