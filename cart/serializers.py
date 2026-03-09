"""
Cart Serializers - Add to Cart Functionality
Uses your existing Product and Service serializers
"""
from rest_framework import serializers
from .models import Cart, CartItem

# Import your existing serializers (adjust import path)
# from products.serializers import ProductSerializer
# from services.serializers import ServiceSerializer


class CartItemSerializer(serializers.ModelSerializer):
    """
    Cart item serializer
    Uses your existing Product/Service serializers
    """
    item_name = serializers.SerializerMethodField()
    item_type = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()
    
    # If you have existing serializers, uncomment and use them:
    # product = ProductSerializer(read_only=True)
    # service = ServiceSerializer(read_only=True)
    
    class Meta:
        model = CartItem
        fields = [
            'id', 'cart',
            'product', 'service',
            'item_name', 'item_type',
            'unit_price', 'total_price',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['unit_price', 'created_at', 'updated_at']
    
    def get_item_name(self, obj):
        return obj.get_item_name()
    
    def get_item_type(self, obj):
        return 'product' if obj.is_product() else 'service'
    
    def get_total_price(self, obj):
        return str(obj.get_total_price())


class CartSerializer(serializers.ModelSerializer):
    """
    Complete cart serializer with all items
    """
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    total_items = serializers.SerializerMethodField()
    
    class Meta:
        model = Cart
        fields = [
            'id', 'user', 'is_active',
            'items', 'total_price', 'total_items',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['user', 'created_at', 'updated_at']
    
    def get_total_price(self, obj):
        return str(obj.get_total_price())
    
    def get_total_items(self, obj):
        return obj.get_total_items()


class CartSummarySerializer(serializers.ModelSerializer):
    """
    Lightweight cart summary for header/badge
    """
    count = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()
    
    class Meta:
        model = Cart
        fields = ['id', 'count', 'total']
    
    def get_count(self, obj):
        return obj.get_total_items()
    
    def get_total(self, obj):
        return str(obj.get_total_price())


class AddToCartSerializer(serializers.Serializer):
    """
    Serializer for adding items to cart
    Validates product/service exists
    """
    item_type = serializers.ChoiceField(
        choices=['product', 'service'],
        error_messages={
            'invalid_choice': 'Item type must be "product" or "service"'
        }
    )
    item_id = serializers.IntegerField(
        min_value=1,
        error_messages={
            'min_value': 'Item ID must be positive'
        }
    )
    
    def validate(self, data):
        """Validate that product/service exists"""
        item_type = data['item_type']
        item_id = data['item_id']
        
        # Import your models here (adjust import path)
        from products.models import Product
        from service.models import Service
        
        if item_type == 'product':
            try:
                product = Product.objects.get(id=item_id)
                data['item'] = product
            except Product.DoesNotExist:
                raise serializers.ValidationError({
                    'item_id': 'Product not found'
                })
        else:  # service
            try:
                service = Service.objects.get(id=item_id)
                data['item'] = service
            except Service.DoesNotExist:
                raise serializers.ValidationError({
                    'item_id': 'Service not found'
                })
        
        return data


# UpdateCartItemSerializer has been removed – quantity is no longer editable.