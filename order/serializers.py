from rest_framework import serializers
from .models import OrderItem, Order,Payment, OrderStatusHistory

class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer for order items"""
    
    class Meta:
        model = OrderItem
        fields = [
            'id', 'order', 'product', 'service', 'item_name', 'item_type',
            'unit_price', 'total_price','created_at'
        ]
        read_only_fields = ['total_price']

#------------------------OrderSerializer-------------------------
class OrderSerializer(serializers.ModelSerializer):
    """Complete order serializer"""
    items = OrderItemSerializer(many=True, read_only=True)
    items_count = serializers.IntegerField(source='items.count', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'user', 'status', 'payment_status',
            'subtotal', 'total',
            'payment_method', 'customer_notes', 'admin_notes',
            'items', 'items_count',
            'created_at', 'updated_at', 'paid_at', 'delivered_at'
        ]
        read_only_fields = [
            'order_number', 'user', 'subtotal', 'total',
            'created_at', 'updated_at', 'paid_at', 'delivered_at'
        ]
class OrderListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for order lists"""
    items_count = serializers.IntegerField(source='items.count', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'status', 'payment_status',
            'total', 'items_count', 'created_at'
        ]

#---------------------- createorderserializer---------------------
class CreateOrderSerializer(serializers.Serializer):
    """
    Serializer for creating an order
    """
    payment_method = serializers.ChoiceField(
        choices=['stripe', 'card', 'bank_transfer']
    )
    customer_notes = serializers.CharField(required=False, allow_blank=True)
    # discount_code = serializers.CharField(required=False, allow_blank=True)

#---------------------------PaymentSerializer---------------------
class PaymentSerializer(serializers.ModelSerializer):
    """Payment transaction serializer"""
    order_number = serializers.CharField(source='order.order_number', read_only=True)

    class Meta:
        model = Payment
        fields = [
            'id', 'order', 'order_number', 'payment_id', 'amount', 'currency',
            'payment_method', 'status', 'transaction_id', 'payment_gateway',
            'card_last4', 'card_brand', 'error_message',
            'created_at', 'updated_at', 'completed_at'
        ]
        read_only_fields = [
            'payment_id', 'status', 'transaction_id', 'card_last4', 'card_brand',
            'created_at', 'updated_at', 'completed_at'
        ]


class ProcessPaymentSerializer(serializers.Serializer):
    """
    Serializer for processing payment
    """
    order_id = serializers.IntegerField()
    payment_method = serializers.ChoiceField(
        choices=['stripe', 'bank_transfer', 'card']
    )

    # For Stripe
    stripe_token = serializers.CharField(required=False, allow_blank=True)
    stripe_payment_method_id = serializers.CharField(required=False, allow_blank=True)

    # # For PayPal
    # paypal_order_id = serializers.CharField(required=False, allow_blank=True)

    # For card (if not using Stripe)
    card_number = serializers.CharField(required=False, allow_blank=True)
    card_expiry = serializers.CharField(required=False, allow_blank=True)
    card_cvv = serializers.CharField(required=False, allow_blank=True)

    def validate(self, data):
        payment_method = data['payment_method']
        if payment_method == 'stripe':
            if not data.get('stripe_token') and not data.get('stripe_payment_method_id'):
                raise serializers.ValidationError(
                    'Stripe token or payment method ID is required'
                )
        # elif payment_method == 'paypal':
        #     if not data.get('paypal_order_id'):
        #         raise serializers.ValidationError(
        #             'PayPal order ID is required'
        #         )
        return data


class OrderStatusHistorySerializer(serializers.ModelSerializer):
    """Order status history serializer"""
    changed_by_username = serializers.CharField(
        source='changed_by.username', 
        read_only=True
    )

    class Meta:
        model = OrderStatusHistory
        fields = [
            'id', 'old_status', 'new_status', 'changed_by',
            'changed_by_username', 'notes', 'created_at'
        ]


class UpdateOrderStatusSerializer(serializers.Serializer):
    """Serializer for updating order status – 'shipped' removed"""
    status = serializers.ChoiceField(
        choices=[
            'pending', 'confirmed', 'processing',
            'delivered', 'cancelled', 'refunded'
        ]
    )
    notes = serializers.CharField(required=False, allow_blank=True)


class OrderSummarySerializer(serializers.ModelSerializer):
    """Quick order summary"""
    class Meta:
        model = Order
        fields = ['id', 'order_number', 'total', 'status', 'created_at']


class CheckoutSerializer(serializers.Serializer):
    """
    Combined serializer for complete checkout – only payment method and notes
    """
    payment_method = serializers.ChoiceField(
        choices=['stripe', 'card', 'bank_transfer'],
        required=False,
        allow_blank=True
    )
    stripe_payment_method_id = serializers.CharField(
        required=False, 
        allow_blank=True
    )
    customer_notes = serializers.CharField(required=False, allow_blank=True)
    
    card_last4 = serializers.CharField(required=False, allow_blank=True)
    card_brand = serializers.CharField(required=False, allow_blank=True)                    