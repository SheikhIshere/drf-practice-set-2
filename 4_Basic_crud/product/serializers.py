"""
Docstring for product.serializers
"""
# core imports
from rest_framework import (
    serializers
)

# local import
from .models import (
    Tag,
    Brand,
    Product
)



"""
brand
"""
class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = (
            'id',
            'user' ,
            'title',
            'created_at',
        )
        read_only_fields = ('id', 'created_at',)


"""
tag
"""
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            'id',
            'user',
            'title',
            'slug',
            'created_at',            
        )
        read_only_fields = ('id', 'created_at',)


"""
product list
"""
class AllProductListSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(read_only=True)
    class Meta:
        model = Product
        fields = (
            'id',
            'title',
            'price',
            'image',
            'stock_quantity',
            'brand',
            'warrantee_availability',
        )

"""
product details
"""
class ProductDetailSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(read_only=True)
    tag = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ('created_at',)

