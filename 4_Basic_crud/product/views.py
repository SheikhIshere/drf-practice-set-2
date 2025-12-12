"""
Docstring for product.views
"""

# core import
from rest_framework import (
    generics,
    viewsets,
    permissions,
    status
)
from rest_framework.response import Response

# local imports
from .models import (
    Tag,
    Brand,
    Product
)
from .serializers import (
    BrandSerializer,
    TagSerializer,
    AllProductListSerializer,
    ProductDetailSerializer
)

# user
from django.contrib.auth import get_user_model
User = get_user_model()



"""
custom permission
"""
class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user

"""
base view
"""
class BaseView(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)



"""
brand crud
"""
class BrandViewSet(BaseView):
    serializer_class = BrandSerializer
    queryset = Brand.objects.all()


"""
tag crud
"""
class TagViewSet(BaseView):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


"""
showing product list
"""
class ProductListView(generics.ListAPIView):
    serializer_class = AllProductListSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        return Product.objects.order_by('-created_at')


"""
retrieve update and delete owner version
"""
class ProductDetailView(BaseView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer