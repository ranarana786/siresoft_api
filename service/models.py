from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User


class TimestampedModel(models.Model):
    """
    Abstract base model that provides self-updating
    'created_at' and 'updated_at' fields.
    """
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created At"),
        help_text=_("Timestamp when the record was created")
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated At"),
        help_text=_("Timestamp when the record was last updated")
    )

    class Meta:
        abstract = True


class ServiceCategory(TimestampedModel):
    """
    Model for categorizing services (e.g., Development, Design, Marketing)
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_("Category Name"),
        help_text=_("Name of the service category")
    )
    slug = models.SlugField(
        max_length=120,
        unique=True,
        blank=True,
        verbose_name=_("URL Slug"),
        help_text=_("Auto-generated URL-friendly version of name")
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("Description"),
        help_text=_("Brief description of this category")
    )
    icon = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name=_("Icon Class"),
        help_text=_("CSS icon class (e.g., 'fa-code', 'bi-palette')")
    )
    display_order = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Display Order"),
        help_text=_("Order in which category appears (lower numbers first)")
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Is Active"),
        help_text=_("Whether this category is currently active")
    )

    class Meta:
        verbose_name = _("Service Category")
        verbose_name_plural = _("Service Categories")
        ordering = ['display_order', 'name']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['is_active', 'display_order']),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Service(TimestampedModel):
    """
    Main Service model representing offerings like Web Development, CRM, SEO, etc.
    """
    
    # Service Type Choices
    SERVICE_TYPE_CHOICES = [
        ('development', _('Development')),
        ('design', _('Design')),
        ('marketing', _('Marketing')),
        ('consulting', _('Consulting')),
        ('support', _('Support')),
        ('custom', _('Custom')),
    ]
    
    # Delivery Timeline Choices
    DELIVERY_UNIT_CHOICES = [
        ('hours', _('Hours')),
        ('days', _('Days')),
        ('weeks', _('Weeks')),
        ('months', _('Months')),
    ]

    # Basic Information
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name=_("Service Name"),
        help_text=_("Name of the service (e.g., 'Web Development', 'Logo Design')")
    )
    slug = models.SlugField(
        max_length=220,
        unique=True,
        blank=True,
        verbose_name=_("URL Slug"),
        help_text=_("Auto-generated URL-friendly version of service name")
    )
    category = models.ForeignKey(
        ServiceCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='services',
        verbose_name=_("Category"),
        help_text=_("Category this service belongs to")
    )
    service_type = models.CharField(
        max_length=20,
        choices=SERVICE_TYPE_CHOICES,
        default='custom',
        verbose_name=_("Service Type"),
        help_text=_("Type of service being offered")
    )

    # Descriptions
    short_description = models.CharField(
        max_length=255,
        verbose_name=_("Short Description"),
        help_text=_("Brief one-line description for listings")
    )
    description = models.TextField(
        verbose_name=_("Full Description"),
        help_text=_("Detailed description of the service")
    )
    features = models.JSONField(
        default=list,
        blank=True,
        verbose_name=_("Features"),
        help_text=_("List of features included in this service (JSON array)")
    )
    requirements = models.JSONField(
        default=list,
        blank=True,
        verbose_name=_("Requirements"),
        help_text=_("Client requirements for this service (JSON array)")
    )

    # Visual Elements
    icon = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name=_("Icon Class"),
        help_text=_("CSS icon class for this service")
    )
    thumbnail = models.ImageField(
        upload_to='services/thumbnails/%Y/%m/',
        blank=True,
        null=True,
        verbose_name=_("Thumbnail Image"),
        help_text=_("Service thumbnail image")
    )
    banner_image = models.ImageField(
        upload_to='services/banners/%Y/%m/',
        blank=True,
        null=True,
        verbose_name=_("Banner Image"),
        help_text=_("Service banner/hero image")
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
        help_text=_("Starting price for this service (0 for custom quote)")
    )
    currency = models.CharField(
        max_length=3,
        default='USD',
        verbose_name=_("Currency"),
        help_text=_("ISO 4217 currency code (e.g., USD, EUR, GBP)")
    )
    pricing_model = models.CharField(
        max_length=20,
        choices=[
            ('fixed', _('Fixed Price')),
            ('hourly', _('Hourly Rate')),
            ('monthly', _('Monthly Subscription')),
            ('project', _('Per Project')),
            ('custom', _('Custom Quote')),
        ],
        default='fixed',
        verbose_name=_("Pricing Model"),
        help_text=_("How this service is priced")
    )

    # Delivery Information
    delivery_time = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name=_("Delivery Time"),
        help_text=_("Estimated delivery time (numeric value)")
    )
    delivery_unit = models.CharField(
        max_length=10,
        choices=DELIVERY_UNIT_CHOICES,
        default='days',
        verbose_name=_("Delivery Unit"),
        help_text=_("Unit for delivery time")
    )
    revisions_included = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Revisions Included"),
        help_text=_("Number of revisions included (0 for unlimited)")
    )

    # Status and Display
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Is Active"),
        help_text=_("Whether this service is currently offered")
    )
    is_featured = models.BooleanField(
        default=False,
        verbose_name=_("Is Featured"),
        help_text=_("Display this service in featured section")
    )
    display_order = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Display Order"),
        help_text=_("Order in which service appears (lower numbers first)")
    )


    class Meta:
        verbose_name = _("Service")
        verbose_name_plural = _("Services")
        ordering = ['display_order', 'name']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['is_active', 'is_featured']),
            models.Index(fields=['category', 'is_active']),
            models.Index(fields=['service_type', 'is_active']),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_delivery_time_display_full(self):
        """Returns formatted delivery time (e.g., '7 Days')"""
        if self.delivery_time:
            return f"{self.delivery_time} {self.get_delivery_unit_display()}"
        return "On Request"
