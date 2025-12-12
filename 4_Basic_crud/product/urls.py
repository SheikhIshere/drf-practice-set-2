"""
Docstring for product.urls
"""

# core import
from django.urls import path, include

# local imports
from .views import (
    BrandViewSet,
    TagViewSet,
    ProductListView,
    ProductDetailView,
)

# model set
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('brand', BrandViewSet, basename='brand'),
router.register('tag', TagViewSet, basename='tag'),
router.register('product-detail', ProductDetailView, basename='product_detail'),

urlpatterns = [
    path('', include(router.urls)), 
    path('product-list/', ProductListView.as_view(), name='product-list')
]