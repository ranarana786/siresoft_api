# from .serializers import (
#     OrderItemSerializer, OrderSerializer, OrderListSerializer,
#     CreateOrderSerializer, CheckoutSerializer,
#     # ProcessPaymentSerializer, PaymentSerializer  # Commented out payment serializers
# )
# from .models import OrderItem, Order, Payment
# from cart.models import Cart
# from rest_framework import viewsets, status
# from rest_framework.response import Response
# from rest_framework.decorators import action
# from rest_framework.permissions import IsAuthenticated
# from django.db import transaction
# from django.utils import timezone
# from decimal import Decimal


# class OrderViewSet(viewsets.ModelViewSet):
#     serializer_class = OrderSerializer

#     def get_queryset(self):
#         """Get orders for current user"""
#         return Order.objects.filter(user=self.request.user).prefetch_related('items')

#     def get_serializer_class(self):
#         if self.action == 'list':
#             return OrderListSerializer
#         return OrderSerializer

#     def list(self, request):
#         orders = self.get_queryset()
#         status_filter = request.query_params.get('status')
#         if status_filter:
#             orders = orders.filter(status=status_filter)
#         payment_status = request.query_params.get('payment_status')
#         if payment_status:
#             orders = orders.filter(payment_status=payment_status)
#         serializer = self.get_serializer(orders, many=True)
#         return Response(
#             {
#                 "message": "Orders fetched successfully",
#                 "data": serializer.data
#             },
#             status=status.HTTP_200_OK
#         )

#     def retrieve(self, request, pk=None):
#         try:
#             order = self.get_queryset().get(pk=pk)
#             serializer = self.get_serializer(order)
#             return Response(serializer.data)
#         except Order.DoesNotExist:
#             return Response({"error": "Order not found"}, status=404)

#     @action(detail=False, methods=['post'])
#     def create_order(self, request):
#         """
#         POST /api/orders/create/
#         Create order from cart
#         """
#         serializer = CreateOrderSerializer(data=request.data)

#         if not serializer.is_valid():
#             return Response({
#                 'success': False,
#                 'errors': serializer.errors
#             }, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             # Get user's active cart
#             cart = Cart.objects.filter(
#                 user=request.user,
#                 is_active=True
#             ).prefetch_related('items').first()

#             if not cart or not cart.items.exists():
#                 return Response({
#                     'success': False,
#                     'error': 'Cart is empty'
#                 }, status=status.HTTP_400_BAD_REQUEST)

#             with transaction.atomic():
#                 # Calculate subtotal
#                 subtotal = cart.get_total_price()
#                 total = subtotal

#                 # ✅ Sirf order create karo, payment nahi
#                 order = Order.objects.create(
#                     user=request.user,
#                     status='pending',
#                     payment_status='pending',
#                     subtotal=subtotal,
#                     total=total,
#                     payment_method=serializer.validated_data['payment_method'],
#                     customer_notes=serializer.validated_data.get('customer_notes', ''),
#                 )

#                 # Create order items from cart items
#                 for cart_item in cart.items.all():
#                     OrderItem.objects.create(
#                         order=order,
#                         item_name=cart_item.get_item_name(),
#                         item_type='product' if hasattr(cart_item, 'product') and cart_item.product else 'service',
#                         unit_price=cart_item.unit_price,
#                         total_price=cart_item.unit_price,
#                     )

#                 # Clear cart
#                 cart.clear()
#                 cart.is_active = False
#                 cart.save()

#             # Return created order
#             order_serializer = OrderSerializer(order)
#             return Response({
#                 'success': True,
#                 'message': 'Order created successfully',
#                 'order': order_serializer.data
#             }, status=status.HTTP_201_CREATED)

#         except Exception as e:
#             return Response({
#                 'success': False,
#                 'error': str(e)
#             }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#     @action(detail=False, methods=['post'])
#     def checkout(self, request):
#         """
#         POST /api/orders/checkout/
#         Sirf order create karo, payment nahi
#         """
#         serializer = CheckoutSerializer(data=request.data)

#         if not serializer.is_valid():
#             return Response({
#                 'success': False,
#                 'errors': serializer.errors
#             }, status=status.HTTP_400_BAD_REQUEST)

#         # Sirf order create karo
#         create_order_data = {
#             'payment_method': serializer.validated_data['payment_method'],
#             'customer_notes': serializer.validated_data.get('customer_notes', ''),
#         }

#         create_response = self.create_order(
#             type('Request', (), {'user': request.user, 'data': create_order_data})()
#         )

#         return create_response


# # class PaymentViewSet(viewsets.ViewSet):
# #     """
# #     Payment Processing API - Currently Disabled
# #     """
# #     permission_classes = [IsAuthenticated]
# #
# #     @action(detail=False, methods=['post'])
# #     def process_payment(self, request):
# #         """
# #         POST /api/payments/process/
# #         Yahan payment create karo aur order confirm karo
# #         """
# #         serializer = ProcessPaymentSerializer(data=request.data)
# #
# #         if not serializer.is_valid():
# #             return Response({
# #                 'success': False,
# #                 'errors': serializer.errors
# #             }, status=status.HTTP_400_BAD_REQUEST)
# #
# #         order_id = serializer.validated_data['order_id']
# #         payment_method = serializer.validated_data['payment_method']
# #
# #         try:
# #             order = Order.objects.get(id=order_id, user=request.user)
# #         except Order.DoesNotExist:
# #             return Response({
# #                 'success': False,
# #                 'error': 'Order not found'
# #             }, status=status.HTTP_404_NOT_FOUND)
# #
# #         # ✅ Check if payment already exists
# #         existing_payment = Payment.objects.filter(order=order).first()
# #         if existing_payment:
# #             return Response({
# #                 'success': False,
# #                 'error': 'Payment already processed for this order'
# #             }, status=status.HTTP_400_BAD_REQUEST)
# #
# #         # Process based on payment method
# #         if payment_method == 'stripe':
# #             return self._process_stripe_payment(order, serializer.validated_data)
# #         elif payment_method == 'card':
# #             return self._process_card_payment(order, serializer.validated_data)
# #         elif payment_method == 'bank_transfer':
# #             return self._process_bank_transfer(order, serializer.validated_data)
# #         else:
# #             return Response({
# #                 'success': False,
# #                 'error': 'Payment method not supported'
# #             }, status=status.HTTP_400_BAD_REQUEST)
# #
# #     def _process_stripe_payment(self, order, payment_data):
# #         """Process Stripe payment"""
# #         try:
# #             import stripe
# #             from django.conf import settings
# #
# #             stripe.api_key = settings.STRIPE_SECRET_KEY
# #             payment_method_id = payment_data.get('stripe_payment_method_id')
# #
# #             with transaction.atomic():
# #                 intent = stripe.PaymentIntent.create(
# #                     amount=int(order.total * 100),
# #                     currency='usd',
# #                     payment_method=payment_method_id,
# #                     confirm=True,
# #                     automatic_payment_methods={
# #                         'enabled': True,
# #                         'allow_redirects': 'never'
# #                     },
# #                     metadata={
# #                         'order_id': order.id,
# #                         'order_number': order.order_number,
# #                     }
# #                 )
# #
# #                 # ✅ Payment create
# #                 payment = Payment.objects.create(
# #                     order=order,
# #                     payment_id=intent.id,
# #                     amount=order.total,
# #                     currency='usd',
# #                     payment_method='stripe',
# #                     status='completed' if intent.status == 'succeeded' else 'failed',
# #                     transaction_id=intent.id,
# #                     payment_gateway='stripe',
# #                     gateway_response=intent,
# #                     completed_at=timezone.now() if intent.status == 'succeeded' else None
# #                 )
# #
# #                 # ✅ Order confirm
# #                 if intent.status == 'succeeded':
# #                     order.payment_status = 'completed'
# #                     order.status = 'confirmed'
# #                     order.paid_at = timezone.now()
# #                 else:
# #                     order.payment_status = 'failed'
# #                     payment.error_message = intent.get('last_payment_error', {}).get('message', '')
# #
# #                 order.save()
# #                 payment.save()
# #
# #             if intent.status == 'succeeded':
# #                 return Response({
# #                     'success': True,
# #                     'message': 'Payment successful',
# #                     'payment_id': payment.payment_id,
# #                     'order_number': order.order_number
# #                 }, status=status.HTTP_200_OK)
# #             else:
# #                 return Response({
# #                     'success': False,
# #                     'error': 'Payment failed',
# #                     'details': intent.get('last_payment_error', {})
# #                 }, status=status.HTTP_400_BAD_REQUEST)
# #
# #         except stripe.error.CardError as e:
# #             return Response({
# #                 'success': False,
# #                 'error': str(e.user_message)
# #             }, status=status.HTTP_400_BAD_REQUEST)
# #         except Exception as e:
# #             return Response({
# #                 'success': False,
# #                 'error': str(e)
# #             }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
# #
# #     def _process_card_payment(self, order, payment_data):
# #         """Process direct card payment (manual/offline)"""
# #         try:
# #             with transaction.atomic():
# #                 # ✅ Payment create
# #                 payment = Payment.objects.create(
# #                     order=order,
# #                     payment_id=f"CARD-{order.order_number}-{timezone.now().timestamp()}",
# #                     amount=order.total,
# #                     currency='usd',
# #                     payment_method='card',
# #                     status='pending',
# #                     payment_gateway='manual',
# #                     card_last4=payment_data.get('card_last4', ''),
# #                     card_brand=payment_data.get('card_brand', ''),
# #                 )
# #
# #                 # ✅ Order confirm
# #                 order.payment_status = 'processing'
# #                 order.status = 'confirmed'
# #                 order.save()
# #
# #             return Response({
# #                 'success': True,
# #                 'message': 'Card payment initiated. Awaiting confirmation.',
# #                 'payment_id': payment.payment_id,
# #                 'order_number': order.order_number,
# #                 'status': 'processing'
# #             }, status=status.HTTP_200_OK)
# #
# #         except Exception as e:
# #             return Response({
# #                 'success': False,
# #                 'error': str(e)
# #             }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
# #
# #     def _process_bank_transfer(self, order, payment_data):
# #         """Process bank transfer payment"""
# #         try:
# #             with transaction.atomic():
# #                 # ✅ Payment create
# #                 payment = Payment.objects.create(
# #                     order=order,
# #                     payment_id=f"BT-{order.order_number}-{timezone.now().timestamp()}",
# #                     amount=order.total,
# #                     currency='usd',
# #                     payment_method='bank_transfer',
# #                     status='pending',
# #                     payment_gateway='manual',
# #                 )
# #
# #                 # ✅ Order confirm
# #                 order.payment_status = 'processing'
# #                 order.status = 'confirmed'
# #                 order.save()
# #
# #             bank_details = {
# #                 'bank_name': 'Example Bank',
# #                 'account_name': 'SireSoft LLC',
# #                 'account_number': '1234567890',
# #                 'routing_number': '021000021',
# #                 'swift_code': 'EXMPUS33',
# #                 'reference': order.order_number
# #             }
# #
# #             return Response({
# #                 'success': True,
# #                 'message': 'Bank transfer instructions',
# #                 'bank_details': bank_details,
# #                 'payment_id': payment.payment_id,
# #                 'order_number': order.order_number,
# #                 'status': 'processing'
# #             }, status=status.HTTP_200_OK)
# #
# #         except Exception as e:
# #             return Response({
# #                 'success': False,
# #                 'error': str(e)
# #             }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
# #
# #     @action(detail=False, methods=['get'], url_path='order/(?P<order_id>[0-9]+)')
# #     def get_order_payments(self, request, order_id=None):
# #         """
# #         GET /api/payments/order/{order_id}/
# #         Get all payments for an order
# #         """
# #         try:
# #             order = Order.objects.get(id=order_id, user=request.user)
# #             payments = order.payments.all()
# #             serializer = PaymentSerializer(payments, many=True)
# #             return Response(serializer.data)
# #         except Order.DoesNotExist:
# #             return Response({
# #                 'error': 'Order not found'
# #             }, status=status.HTTP_404_NOT_FOUND)


"""
Order API Views
Handles both Anonymous and Authenticated users
- Anonymous: orders tracked via session_key
- Authenticated: orders tracked via user FK
"""

from .serializers import (
    OrderItemSerializer, OrderSerializer, OrderListSerializer,
    CreateOrderSerializer, CheckoutSerializer,
)
from .models import OrderItem, Order
from cart.models import Cart
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from django.db import transaction
from users.models import User
import string, random
from .utility.helpers import send_order_confirmation_email

def ensure_session(request):
    """
    Ensure session exists and session_key is never None.
    Same logic as cart's get_or_create_cart.
    """
    if not request.session.session_key:
        return None
    return request.session.session_key


def get_cart_for_request(request):
    """
    Get active cart for both anonymous and authenticated users.
    Returns None if no cart found.
    Does NOT create a new cart.
    """
    if request.user.is_authenticated:
        return (
            Cart.objects
            .filter(user=request.user, is_active=True)
            .prefetch_related('items')
            .first()
        )

    session_key = request.session.session_key
    if not session_key:
        return None

    return (
        Cart.objects
        .filter(session_key=session_key, user=None, is_active=True)
        .prefetch_related('items')
        .first()
    )


def get_orders_for_request(request):
    """
    Get orders queryset for both anonymous and authenticated users.

    - Authenticated  → filter by user
    - Anonymous      → filter by session_key
    """
    if request.user.is_authenticated:
        return (
            Order.objects
            .filter(user=request.user)
            .prefetch_related('items')
            .order_by('-created_at')
        )

    session_key = request.session.session_key
    if not session_key:
        return Order.objects.none()

    return (
        Order.objects
        .filter(session_key=session_key, user=None)
        .prefetch_related('items')
        .order_by('-created_at')
    )


# ─────────────────────────────────────────────
# ORDER VIEWSET
# ─────────────────────────────────────────────

class OrderViewSet(viewsets.ViewSet):
    """
    Complete Order API — works for both Anonymous and Authenticated users

    Endpoints:
    - GET    /api/orders/               → list orders
    - GET    /api/orders/{id}/          → retrieve single order
    - POST   /api/orders/create-order/  → create order from cart
    - POST   /api/orders/checkout/      → checkout (validate + create order)
    """
    permission_classes = [AllowAny]
    
    def list(self, request):
        """
        GET /api/orders/
        List all orders for current user or session.
        Supports optional query filters: ?status=pending&payment_status=pending
        """
        ensure_session(request)
        orders = get_orders_for_request(request)

        order_status = request.query_params.get('status')
        if order_status:
            orders = orders.filter(status=order_status)

        payment_status = request.query_params.get('payment_status')
        if payment_status:
            orders = orders.filter(payment_status=payment_status)

        serializer = OrderListSerializer(orders, many=True)
        return Response(
            {
                "success": True,
                "message": "Orders fetched successfully",
                "count": orders.count(),
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def retrieve(self, request, pk=None):
        """
        GET /api/orders/{id}/
        Get single order — only if it belongs to current user or session.
        """
        ensure_session(request)

        try:
            order = get_orders_for_request(request).get(pk=pk)
            serializer = OrderSerializer(order)
            return Response(
                {"success": True, "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        except Order.DoesNotExist:
            return Response(
                {"success": False, "error": "Order not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

    def _create_order_logic(self, request, validated_data):
        """
        Core logic to create order from active cart.
        Called by both create_order and checkout.
        Works for both anonymous and authenticated users.

        Fixes:
          - No fake Request object (was bug in checkout)
          - product_id check instead of hasattr (was bug in item_type)
          - select_for_update to prevent race conditions
        """
        session_key = ensure_session(request)

        try:
            cart = get_cart_for_request(request)
            
            if not cart:
                return Response(
                    {"success": False, "error": "No active cart found"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if not cart.items.exists():
                return Response(
                    {"success": False, "error": "Cart is empty"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            with transaction.atomic():
                # Lock cart row to prevent race condition
                cart = Cart.objects.select_for_update().get(pk=cart.pk)

                subtotal = cart.get_total_price()
                total = subtotal

                order = Order.objects.create(
                    user=request.user if request.user.is_authenticated else None,
                    session_key=None if request.user.is_authenticated else session_key,
                    status='pending',
                    payment_status='pending',
                    subtotal=subtotal,
                    total=total,
                    # payment_method=validated_data['payment_method'],
                    customer_notes=validated_data.get('customer_notes', ''),
                )

                for cart_item in cart.items.select_related('product', 'service').all():
                    item_type = 'product' if cart_item.product else 'service'

                    OrderItem.objects.create(
                        order=order,
                        item_name=cart_item.get_item_name(),
                        item_type=item_type,
                        unit_price=cart_item.unit_price,
                        total_price=cart_item.unit_price,
                    )

                cart.clear()
                cart.is_active = False
                cart.save()

            order_serializer = OrderSerializer(order)
            
              # ── Send Order Confirmation Email ──
            try:
                if request.user.is_authenticated:
                    user_email = request.user.email
                    user_name = request.user.get_full_name() or request.user.email
                else:
                    billing_data = request.data.get('billing', {})
                    user_email = billing_data.get('email')
                    user_name = billing_data.get('first_name', 'Customer')
                
                if user_email:
                    send_order_confirmation_email(order, user_email, user_name)
                    
            except Exception as email_error:
                print(f"Email sending failed: {str(email_error)}")
                
            return Response(
                {
                    "success": True,
                    "message": "Order created successfully",
                    "order": order_serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            return Response(
                {"success": False, "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=False, methods=['post'], url_path='create-order')
    def create_order(self, request):
        """
        POST /api/orders/create-order/
        Create order from cart.

        Request body:
        {
            "payment_method": "cash_on_delivery" | "bank_transfer" | "card",
            "customer_notes": "optional note"
        }
        """
        print(request.data)
        serializer = CreateOrderSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {"success": False, "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return self._create_order_logic(request, serializer.validated_data)

    @action(detail=False, methods=['post'])
    def checkout(self, request):
        """
        POST /api/orders/checkout/
        Validate checkout data then create order from cart.

        Request body:
        {
            "payment_method": "cash_on_delivery" | "bank_transfer" | "card",
            "customer_notes": "optional note"
        }
        """
        serializer = CheckoutSerializer(data=request.data)
        
        if not request.user.is_authenticated:
            billing_data = request.data.get('billing')
            email = billing_data.get('email')
            first_name = billing_data.get('first_name', '')
            last_name = billing_data.get('last_name', '')
        
            if not email:
                return Response(
                    {"success": False, "error": "Email is required for guest checkout"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        
            try:
                with transaction.atomic():
                    user = User.objects.filter(email=email).first() 
                    
                    if not user: 
                        dummy_password = ''.join(random.choices(
                            string.ascii_letters + string.digits, 
                            k=12
                        ))
    
                        user = User.objects.create_user(
                            email=email,
                            password=dummy_password,
                            first_name=first_name,
                            last_name=last_name,
                            is_active=False  # Account inactive until email verification
                        )
            except Exception as e:
                return Response(
                    {"success": False, "error": f"Failed to create user: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        if not serializer.is_valid():
            return Response(
                {"success": False, "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # FIX: Directly call shared logic — no fake Request object
        return self._create_order_logic(request, serializer.validated_data)