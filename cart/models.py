"""
Cart Models - Add to Cart Functionality Only
Works with your existing Product and Service models
"""
from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from decimal import Decimal

User = get_user_model()

class Cart(models.Model):
    """
    Shopping cart for authenticated and anonymous users
    """
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='carts'
    )
    session_key = models.CharField(max_length=255, null=True, blank=True)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['user', 'is_active']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        if self.user:
            return f"Cart for {self.user.get_full_name()}"
        return f"Cart (id={self.id})"

    def get_total_price(self):
        """Calculate total cart price (sum of unit prices)"""
        total = Decimal('0.00')
        for item in self.items.all():
            total += item.get_total_price()
        return total

    def get_total_items(self):
        """Get total number of items in cart"""
        return self.items.count()

    def clear(self):
        """Remove all items from cart"""
        self.items.all().delete()


class CartItem(models.Model):
    """
    Individual items in a cart
    Links to your existing Product and Service models
    """
    cart = models.ForeignKey(
        Cart, 
        on_delete=models.CASCADE, 
        related_name='items'
    )
    
    # Reference to your Product model (adjust app name as needed)
    product = models.ForeignKey(
        'products.Product',  # Change 'products' to your actual app name
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='cart_items'
    )
    
    # Reference to your Service model (adjust app name as needed)
    service = models.ForeignKey(
        'service.Service',  # Change 'service' to your actual app name
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='cart_items'
    )
    
    # Store price at time of adding (price may change later)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['cart', 'product']),
            models.Index(fields=['cart', 'service']),
        ]

    def __str__(self):
        return self.get_item_name()

    def clean(self):
        """Validate that item is either a product or service, not both"""
        if self.product and self.service:
            raise ValidationError("Cart item cannot be both a product and service")
        if not self.product and not self.service:
            raise ValidationError("Cart item must be either a product or service")

    def save(self, *args, **kwargs):
        """Set unit price on first save"""
        if not self.pk:  # Only on creation
            if self.product:
                # Assuming your Product has a 'base_price' field
                self.unit_price = self.product.base_price
            elif self.service:
                # Assuming your Service has a 'base_price' field
                self.unit_price = self.service.base_price
        
        self.full_clean()
        super().save(*args, **kwargs)

    def get_item_name(self):
        """Get the name of the product or service"""
        if self.product:
            return self.product.name
        elif self.service:
            return self.service.name
        return "Unknown Item"

    def get_total_price(self):
        """Calculate total price for this cart item (always unit_price)"""
        return self.unit_price

    def is_product(self):
        """Check if this is a product item"""
        return self.product is not None

    def is_service(self):
        """Check if this is a service item"""
        return self.service is not None