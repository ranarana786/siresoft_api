# pricing/models.py
"""
Simple Pricing Plans Models for Website Subscriptions
Based on Business Basic, Pro, Enterprice, Ultimate
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
from decimal import Decimal
from service.models import Service


class PricingPlan(models.Model):
    """
    Website Pricing Plans (like Business Basic, Pro, Enterprise, Ultimate)
    """
    BILLING_CHOICES = [
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ]

    PLAN_TYPE_CHOICES = [
        ('basic', 'Basic'),
        ('pro', 'Pro'),
        ('enterprise', 'Enterprise'),
        ('ultimate', 'Ultimate')
    ]

    # Basic Info
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    plan_type = models.CharField(max_length=20, choices=PLAN_TYPE_CHOICES)
    tagline = models.CharField(max_length=300)
    
    # Pricing
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    billing_period = models.CharField(max_length=20, choices=BILLING_CHOICES, default='monthly')
    
    # Display
    is_featured = models.BooleanField(default=False)
    is_popular = models.BooleanField(default=False)
    badge_text = models.CharField(max_length=50, blank=True)
    button_text = models.CharField(max_length=100, default='Add to Cart')
    
    # Status
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'price']
        verbose_name = 'Pricing Plan'
        verbose_name_plural = 'Pricing Plans'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - ${self.price}/{self.billing_period}"


class PlanFeature(models.Model):
    """
    Features included or excluded in plans
    """
    plan = models.ForeignKey(
        PricingPlan, 
        on_delete=models.CASCADE, 
        related_name='features'
    )
    name = models.CharField(max_length=200)
    is_included = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']
        unique_together = ['plan', 'name']

    def __str__(self):
        status = "✓" if self.is_included else "✗"
        return f"{status} {self.name} ({self.plan.name})"
    
class PlanComparison(models.Model):
    """
    Store comparison features for displaying plan comparison tables
    """
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="comparison_features",
        null=True,
        blank=True
)
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Plan Comparison Feature"
        verbose_name_plural = "Plan Comparison Features"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class PlanComparisonValue(models.Model):
    """
    Values for comparison features across different plans
    """
    comparison_feature = models.ForeignKey(
        PlanComparison,
        on_delete=models.CASCADE,
        related_name='values'
    )
    plan = models.ForeignKey(
        PricingPlan,
        on_delete=models.CASCADE,
        related_name='comparison_values'
    )
    value = models.CharField(max_length=200)
    is_available = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Plan Comparison Value"
        verbose_name_plural = "Plan Comparison Values"
        unique_together = [['comparison_feature', 'plan']]

    def __str__(self):
        return f"{self.plan.name} - {self.comparison_feature.name}: {self.value}"
    