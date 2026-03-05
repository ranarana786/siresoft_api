from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('software', 'Software and Licensing'),
        ('cybersecurity', 'Cybersecurity'),
        ('network', 'Network and Data Center'),
        ('webmail', 'Web Server and Mail Server'),
        ('hardware', 'Hardware Supply'),
        ('vm', 'Virtual Machines'),
    ]

    name = models.CharField(max_length=200)
    slug = models.SlugField(
        max_length=220,
        unique=True,
        blank=True,
        verbose_name=_("URL Slug"),
        help_text=_("Auto-generated URL-friendly version of product name")
    )
    
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    
    short_description = models.CharField(
        max_length=255,
        verbose_name=_("Short Description"),
        help_text=_("Brief one-line description for listings")
    )
    
    description = models.TextField(
        verbose_name=_("Full Description"),
        help_text=_("Detailed description of the products")
    )
    features = models.JSONField(
        default=list,
        blank=True,
        verbose_name=_("Features"),
        help_text=_("List of features included in this Product (JSON array)")
    )
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    banner_image = models.ImageField(
        upload_to='products/banners/%Y/%m/',
        blank=True,
        null=True,
        verbose_name=_("Banner Image"),
        help_text=_("products banner/hero image")
    )
    gallery_images = models.JSONField(
        default=list,
        blank=True,
        verbose_name=_("Gallery Images"),
        help_text=_("Array of image URLs for service gallery")
    )

    # Pricing Information
    base_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        verbose_name=_("Base Price"),
        help_text=_("Starting price for this product (0 for custom quote)")
    )
    currency = models.CharField(
        max_length=3,
        default='USD',
        verbose_name=_("Currency"),
        help_text=_("ISO 4217 currency code (e.g., USD, EUR, GBP)")
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Is Active"),
        help_text=_("Whether this products is currently active")
        
    )
    is_popular = models.BooleanField(
        default=False,
        verbose_name=_("Is Popular"),
        help_text=_("Whether this products is popular"))
    
    is_featured = models.BooleanField(
        default=False,
        verbose_name=_("Is Featured"),
        help_text=_("Whether this products is featured or not"))
    
    display_order = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Display Order"),
        help_text=_("Order in which category appears (lower numbers first)")
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
        ordering = ['display_order', 'name']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['is_active', 'is_featured']),
            models.Index(fields=['category']),
            
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name