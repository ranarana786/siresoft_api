from rest_framework import viewsets, permissions
from .models import Product
from .serializers import ProductSerializer

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows products to be viewed (list and detail).
    No create/update/delete actions.
    """
    queryset = Product.objects.filter(is_active=True)   # only active products
    serializer_class = ProductSerializer
         