from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from decimal import Decimal

User = get_user_model()

class Order(models.Model):
    """
    Order placed by a user – for services/digital products.
    No shipping or quantity fields.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('processing', 'Processing'),
        # 'shipped' removed – not applicable
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('stripe', 'Stripe'),
        ('card', 'Credit/Debit Card'),
        ('bank_transfer', 'Bank Transfer'),
    ]

    order_number = models.CharField(
        max_length=50,
        unique=True,
        editable=False
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders',
        null=True,
        blank=True
    )
    
    # for anonymou user session id will use same as session key
    session_key = models.CharField(
    max_length=40,
    null=True,
    blank=True,
    db_index=True, 
    help_text="Anonymous user ka session key — login hone ke baad NULL ho jata hai"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    # discount = models.DecimalField(
    #     max_digits=10,
    #     decimal_places=2,
    #     default=0,
    #     validators=[MinValueValidator(Decimal('0.00'))]
    # )
    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        blank='True',
        default='None'
    )
    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='pending'
    )

    customer_notes = models.TextField(blank=True)
    admin_notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['order_number']),
            models.Index(fields=['status']),
            models.Index(fields=['payment_status']),
        ]

    def __str__(self):
        if self.user:
            return f"Order {self.order_number} - {self.user.get_full_name()}"
        else:
            return f"Order {self.order_number} Guest"

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self.generate_order_number()
        self.total = self.calculate_total()
        super().save(*args, **kwargs)

    def generate_order_number(self):
        """Generate unique order number (timestamp + random hex)"""
        from django.utils import timezone
        import secrets
        date_part = timezone.now().strftime('%Y%m%d')
        rand_part = secrets.token_hex(3).upper() 
        return f"ORD-{date_part}-{rand_part}"

    def calculate_total(self):
        """Calculate order total (no shipping cost)"""
        return self.subtotal

    def can_cancel(self):
        """Check if order can be cancelled"""
        return self.status in ['pending', 'confirmed']

    def can_refund(self):
        """Check if order can be refunded"""
        return self.payment_status == 'completed' and self.status != 'refunded'

# ------------------------------- OrderItem Model ------------------
class OrderItem(models.Model):
    """
    Individual items in an order – for services (quantity = 1).
    """
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )
    
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='order_items'
    )
    service = models.ForeignKey(
        'service.Service',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='order_items'
    )

    item_name = models.CharField(max_length=255)
    item_type = models.CharField(max_length=20)  # 'product' or 'service'
    
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    # For services
    custom_requirements = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.item_name   

    def save(self, *args, **kwargs):
        self.total_price = self.unit_price
        super().save(*args, **kwargs)

# ------------------------------- Payment Model ------------------
class Payment(models.Model):
    """
    Payment transactions for orders
    """
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]

    order = models.ForeignKey(
        Order, 
        on_delete=models.CASCADE, 
        related_name='payments'
    )

    payment_id = models.CharField(
        max_length=255, 
        unique=True
    )  # External payment ID (Stripe, PayPal, etc.)
    
    amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2
    )
    currency = models.CharField(
        max_length=3, 
        default='USD'
    )
    
    payment_method = models.CharField(max_length=50)
    status = models.CharField(
        max_length=20, 
        choices=PAYMENT_STATUS_CHOICES, 
        default='pending'
    )

    # Transaction details
    transaction_id = models.CharField(
        max_length=255, 
        blank=True
    )
    payment_gateway = models.CharField(
        max_length=50
    )  # stripe, paypal, etc.
    
    # Card details (last 4 digits only)
    card_last4 = models.CharField(
        max_length=4, 
        blank=True
    )
    card_brand = models.CharField(
        max_length=20, 
        blank=True
    )

    # Additional data (store JSON from payment gateway)
    gateway_response = models.JSONField(
        blank=True, 
        null=True
    )
    
    error_message = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['order']),
            models.Index(fields=['payment_id']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"Payment {self.payment_id} for Order {self.order.order_number}"   
    
# -------------------OrderStatusHistory---------------------------------
class OrderStatusHistory(models.Model):
    """
    Track order status changes
    """
    order = models.ForeignKey(
        Order, 
        on_delete=models.CASCADE, 
        related_name='status_history'
    )
    
    old_status = models.CharField(max_length=20)
    new_status = models.CharField(max_length=20)
    
    changed_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='order_status_changes'
    )
    
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Order status histories"

    def __str__(self):
        return f"{self.order.order_number}: {self.old_status} → {self.new_status}"         