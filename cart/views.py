"""
Cart API Views - Add to Cart Functionality
Complete REST API for cart operations
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction

from .models import Cart, CartItem
from .serializers import (
    CartSerializer, CartItemSerializer, AddToCartSerializer,
    CartSummarySerializer
)


def get_or_create_cart(request):
    cart, created = Cart.objects.get_or_create(
        user=request.user,
        is_active=True
    )
    return cart


class CartViewSet(viewsets.ViewSet):
    """
    Complete Cart API
    
    Endpoints:
    - GET    /api/cart/              - Get cart
    - POST   /api/cart/add/          - Add item
    - DELETE /api/cart/remove/{id}/  - Remove item
    - POST   /api/cart/clear/        - Clear cart
    - GET    /api/cart/summary/      - Get summary
    - GET    /api/cart/count/        - Get count
    """
    permission_classes = [IsAuthenticated]
    
    def list(self, request):
        """
        GET /api/cart/
        Get complete cart with all items
        """
        cart = get_or_create_cart(request)
        serializer = CartSerializer(cart)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'], url_path='add')
    def add_item(self, request):
        """
        POST /api/cart/add/
        Add item to cart 
        Request body:
        {
            "item_type": "product" or "service",
            "item_id": 1
        }
        Returns error if item already in cart.
        """
        serializer = AddToCartSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response({
                'success': False,
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data
        item = data['item']
        item_type = data['item_type']
        
        try:
            cart = get_or_create_cart(request)
            
            # Check if item already exists in cart
            filter_kwargs = {'cart': cart}
            if item_type == 'product':
                filter_kwargs['product'] = item
            else:
                filter_kwargs['service'] = item
            
            if CartItem.objects.filter(**filter_kwargs).exists():
                return Response({
                    'success': False,
                    'error': f'{item.name} is already in your cart.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            with transaction.atomic():
                if item_type == 'product':
                    cart_item = CartItem.objects.create(
                        cart=cart,
                        product=item,
                        unit_price=item.base_price,
                    )
                else:  # service
                    cart_item = CartItem.objects.create(
                        cart=cart,
                        service=item,
                        unit_price=item.base_price,
                    )
            
            # Return updated cart
            cart_serializer = CartSerializer(cart)
            return Response({
                'success': True,
                'message': f'{item.name} added to cart',
                'cart': cart_serializer.data
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['delete'], url_path='remove/(?P<item_id>[0-9]+)')
    def remove_item(self, request, item_id=None):
        """
        DELETE /api/cart/remove/{item_id}/      
        Remove item from cart
        """
        cart = get_or_create_cart(request)
        
        try:
            cart_item = CartItem.objects.get(id=item_id, cart=cart)
            item_name = cart_item.get_item_name()
            cart_item.delete()
            
            # Return updated cart
            cart_serializer = CartSerializer(cart)
            return Response({
                'success': True,
                'message': f'{item_name} removed from cart',
                'cart': cart_serializer.data
            }, status=status.HTTP_200_OK)
        
        except CartItem.DoesNotExist:
            return Response({
                'success': False,
                'error': 'Cart item not found'
            }, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['post'], url_path='clear')
    def clear(self, request):
        """
        POST /api/cart/clear/ 
        Clear all items from cart
        """
        cart = get_or_create_cart(request)
        cart.clear()
        
        cart_serializer = CartSerializer(cart)
        return Response({
            'success': True,
            'message': 'Cart cleared',
            'cart': cart_serializer.data
        }, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'], url_path='summary')
    def summary(self, request):
        """
        GET /api/cart/summary/ 
        Get lightweight cart summary for header/badge
        """
        cart = get_or_create_cart(request)
        serializer = CartSummarySerializer(cart)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='count')
    def count(self, request):
        """
        GET /api/cart/count/
        Get just the item count (fastest for badge)
        """
        cart = get_or_create_cart(request)
        return Response({
            'count': cart.get_total_items()
        })